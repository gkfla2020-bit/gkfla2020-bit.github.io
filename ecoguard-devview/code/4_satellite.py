"""
4_satellite.py — Sentinel-2 acquisition → U-Net inference → NDVI → Grad-CAM
EUDR Reg. 2023/1115 Art.10 — Forest cover before/after cutoff (2020-12-31)

Pipeline:
  1. Query Copernicus catalog for cloud-free tiles 2019…2024
  2. Pull B02 / B03 / B04 / B08 raw bands (10 m GSD)
  3. Atmospheric correction (Sen2Cor L2A)
  4. RGB composite + NDVI
  5. U-Net (ResNet34 encoder, 4-class) semantic segmentation
  6. Grad-CAM saliency map for forest class
  7. Per-year stats + change detection
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
import rasterio
import torch
import torch.nn.functional as F
from rasterio.warp import reproject, Resampling
from sentinelhub import (
    SHConfig, SentinelHubCatalog, SentinelHubRequest,
    DataCollection, MimeType, BBox, CRS, bbox_to_dimensions,
)
import segmentation_models_pytorch as smp


# --- AOI: PT. Sawit Kalimantan Utama plantation, Central Kalimantan --------
AOI = BBox(bbox=[111.74, -2.55, 111.84, -2.45], crs=CRS.WGS84)
RES_M = 10
DIMS = bbox_to_dimensions(AOI, resolution=RES_M)  # → (1024, 1024)
YEARS = (2019, 2020, 2021, 2022, 2023, 2024)

CLASSES = {0: "forest", 1: "farmland", 2: "bare", 3: "urban"}
NDVI_FOREST_THRESHOLD = 0.6


@dataclass
class YearlyResult:
    year: int
    rgb: np.ndarray            # uint8 (1024, 1024, 3)
    ndvi: np.ndarray           # float32 (1024, 1024)
    segmap: np.ndarray         # int8 (1024, 1024)
    cam: np.ndarray            # float32 (1024, 1024) — forest class saliency
    forest_pct: float
    farmland_pct: float
    bare_pct: float
    urban_pct: float
    ndvi_mean: float
    inference_ms: float


# ---------------------------------------------------------------------------
def cuda_device() -> torch.device:
    if torch.cuda.is_available():
        d = torch.device("cuda:0")
        print(f"[GPU] {torch.cuda.get_device_name(0)}  vram={torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
        return d
    print("[GPU] CUDA unavailable → CPU fallback (slow)")
    return torch.device("cpu")


def load_unet(ckpt: Path, device: torch.device) -> torch.nn.Module:
    print(f"[MODEL] loading checkpoint  path={ckpt.name}  size={ckpt.stat().st_size / 1e6:.1f}MB")
    model = smp.Unet(
        encoder_name="resnet34",
        encoder_weights=None,
        in_channels=4,            # R, G, B, NIR
        classes=len(CLASSES),
    )
    state = torch.load(ckpt, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval().to(device)
    n_params = sum(p.numel() for p in model.parameters()) / 1e6
    print(f"[MODEL] U-Net  encoder=ResNet34  classes={len(CLASSES)}  params={n_params:.1f}M  fp16=on")
    return model


# ---------------------------------------------------------------------------
async def fetch_year(year: int, config: SHConfig) -> dict[str, np.ndarray]:
    """Pull B02/B03/B04/B08 bands for a target year (mid-July, <10% cloud)."""
    catalog = SentinelHubCatalog(config=config)
    search = catalog.search(
        DataCollection.SENTINEL2_L2A,
        bbox=AOI,
        time=(f"{year}-07-01", f"{year}-07-22"),
        filter="eo:cloud_cover < 10",
        fields={"include": ["id", "properties.eo:cloud_cover"], "exclude": []},
    )
    scenes = list(search)
    print(f"  [CAT] {year}  hits={len(scenes)}  best={scenes[0]['id'][-12:]}  cc={scenes[0]['properties']['eo:cloud_cover']:.1f}%")

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: [{ bands: ["B02", "B03", "B04", "B08"], units: "REFLECTANCE" }],
        output: { bands: 4, sampleType: "FLOAT32" },
      };
    }
    function evaluatePixel(s) { return [s.B04, s.B03, s.B02, s.B08]; }
    """
    req = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=(f"{year}-07-01", f"{year}-07-22"),
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=AOI, size=DIMS, config=config,
    )
    arr = req.get_data()[0]                  # (H, W, 4) float32 reflectance
    return {"R": arr[..., 0], "G": arr[..., 1], "B": arr[..., 2], "NIR": arr[..., 3]}


def compose_rgb(bands: dict[str, np.ndarray]) -> np.ndarray:
    """Stretch reflectance → 8-bit, light gamma, mild saturation."""
    rgb = np.stack([bands["R"], bands["G"], bands["B"]], axis=-1)
    rgb = np.clip(rgb / 0.30, 0, 1)
    rgb = np.power(rgb, 1 / 1.15)
    return (rgb * 255).astype(np.uint8)


def compute_ndvi(bands: dict[str, np.ndarray]) -> np.ndarray:
    nir, red = bands["NIR"], bands["R"]
    return ((nir - red) / (nir + red + 1e-9)).astype(np.float32)


# ---------------------------------------------------------------------------
@torch.inference_mode()
def infer(model: torch.nn.Module, bands: dict[str, np.ndarray], device: torch.device) -> tuple[np.ndarray, float]:
    x = np.stack([bands["R"], bands["G"], bands["B"], bands["NIR"]], axis=0)
    x = torch.from_numpy(x).unsqueeze(0).to(device).half()
    print(f"  [INF] input  {tuple(x.shape)}  dtype={x.dtype}")

    t0 = torch.cuda.Event(enable_timing=True) if device.type == "cuda" else None
    t1 = torch.cuda.Event(enable_timing=True) if device.type == "cuda" else None
    if t0 is not None: t0.record()

    logits = model(x)                                # (1, 4, 1024, 1024)
    probs = F.softmax(logits, dim=1)
    seg = probs.argmax(dim=1).squeeze(0).cpu().numpy().astype(np.int8)

    if t1 is not None:
        t1.record(); torch.cuda.synchronize()
        ms = t0.elapsed_time(t1)
    else:
        ms = 0.0
    print(f"  [INF] output {tuple(logits.shape)}  argmax→segmap  t={ms:.0f}ms")
    return seg, ms


def gradcam_forest(model: torch.nn.Module, bands: dict[str, np.ndarray], device: torch.device) -> np.ndarray:
    """Class-Activation Map for the 'forest' class via gradients on the last decoder block."""
    x = np.stack([bands["R"], bands["G"], bands["B"], bands["NIR"]], axis=0)
    x = torch.from_numpy(x).unsqueeze(0).to(device).requires_grad_(True)

    activations: list[torch.Tensor] = []
    gradients:   list[torch.Tensor] = []
    target = model.decoder.blocks[-1]
    h1 = target.register_forward_hook(lambda _, __, o: activations.append(o))
    h2 = target.register_full_backward_hook(lambda _, gi, go: gradients.append(go[0]))

    logits = model(x)                                  # (1, 4, H, W)
    score = logits[0, 0].mean()                        # forest class
    score.backward()

    a = activations[0]
    g = gradients[0]
    weights = g.mean(dim=(2, 3), keepdim=True)         # GAP
    cam = (weights * a).sum(dim=1, keepdim=True)
    cam = F.relu(cam)
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)
    cam = cam.squeeze().detach().cpu().numpy()
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-9)

    h1.remove(); h2.remove()
    return cam


# ---------------------------------------------------------------------------
async def run_year(year: int, model, device, config) -> YearlyResult:
    bands = await fetch_year(year, config)
    rgb = compose_rgb(bands)
    ndvi = compute_ndvi(bands)
    seg, ms = infer(model, bands, device)
    cam = gradcam_forest(model, bands, device)

    pct = lambda c: float((seg == c).mean() * 100)
    return YearlyResult(
        year=year,
        rgb=rgb, ndvi=ndvi, segmap=seg, cam=cam,
        forest_pct=pct(0), farmland_pct=pct(1), bare_pct=pct(2), urban_pct=pct(3),
        ndvi_mean=float(ndvi.mean()),
        inference_ms=ms,
    )


async def main():
    config = SHConfig()
    config.sh_client_id = os.environ["SH_CLIENT_ID"]
    config.sh_client_secret = os.environ["SH_CLIENT_SECRET"]

    device = cuda_device()
    model = load_unet(Path("./checkpoints/unet_resnet34_sentinel2.pth"), device)

    results: list[YearlyResult] = []
    for y in YEARS:
        print(f"[YEAR] {y} ────────────────────────────────────────")
        r = await run_year(y, model, device, config)
        print(f"  [STATS] forest={r.forest_pct:5.1f}%  ndvi_mean={r.ndvi_mean:.3f}")
        results.append(r)

    # change detection 2019 → 2024
    delta = results[-1].forest_pct - results[0].forest_pct
    print(f"[CHANGE] forest 2019→2024 Δ = {delta:+.1f}%p  (cutoff 2020-12-31)")
    return results


if __name__ == "__main__":
    asyncio.run(main())
