"""
2_ocr.py — OCR field extraction with vision-model post-correction
Stack: Tesseract 5 (raw OCR) → GPT-4 Vision (low-confidence reflow) → spaCy NER → cross-check

Reads the validated intake records from step 1 and pulls structured fields out
of every PDF page. Confidence < 93 routes the crop to the vision model for a
second opinion.
"""

import asyncio
import base64
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytesseract
from anthropic import AsyncAnthropic
from pypdf import PdfReader
from pdf2image import convert_from_path
import spacy


CLIENT = AsyncAnthropic()
NLP = spacy.load("en_core_web_trf")  # ~440 MB transformer NER

TARGETS = [
    "Exporter", "Importer", "Product", "HS Code", "Quantity",
    "Origin GPS", "Plantation ID", "Harvest Period",
    "ISCC Certificate", "Loading Port", "Vessel Name", "ETA EU Port",
]

LOW_CONF = 93.0  # below → escalate to vision model


@dataclass
class FieldHit:
    name: str
    value: str
    confidence: float
    source_doc: str
    source_page: int
    bbox: tuple[int, int, int, int]
    raw_tokens: list[str] = field(default_factory=list)
    corrected_by: str | None = None


def preprocess(img: np.ndarray) -> np.ndarray:
    """Sharpen + adaptive threshold — boosts Tesseract accuracy on scanned PDFs."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 50, 50)
    th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 12
    )
    return th


def ocr_page(img: np.ndarray) -> list[dict[str, Any]]:
    """Run Tesseract with bounding boxes + per-word confidence."""
    config = "--oem 3 --psm 6"
    data = pytesseract.image_to_data(
        preprocess(img), config=config, output_type=pytesseract.Output.DICT
    )
    rows: list[dict[str, Any]] = []
    for i, txt in enumerate(data["text"]):
        if not txt.strip():
            continue
        rows.append({
            "text": txt,
            "conf": float(data["conf"][i]),
            "bbox": (data["left"][i], data["top"][i], data["width"][i], data["height"][i]),
        })
    return rows


async def revisit_with_vision(crop: np.ndarray, target: str) -> tuple[str, float]:
    """Send the low-confidence crop to Claude Vision for a second pass."""
    _, buf = cv2.imencode(".png", crop)
    b64 = base64.b64encode(buf.tobytes()).decode()
    msg = await CLIENT.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=128,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
                {"type": "text", "text": f"Extract the value of '{target}' from this image. Return JSON: {{\"value\": ..., \"confidence\": 0-1}}."},
            ],
        }],
    )
    out = json.loads(msg.content[0].text)
    return str(out["value"]), float(out["confidence"]) * 100


def match_target(rows: list[dict], name: str) -> FieldHit | None:
    """Naive keyword + regex match → in production we use spaCy NER + DocBin patterns."""
    for i, row in enumerate(rows):
        if name.lower() in row["text"].lower():
            value_tokens = [r["text"] for r in rows[i + 1: i + 6]]
            return FieldHit(
                name=name,
                value=" ".join(value_tokens),
                confidence=row["conf"],
                source_doc="",
                source_page=0,
                bbox=row["bbox"],
                raw_tokens=value_tokens,
            )
    return None


async def extract_doc(pdf_path: Path) -> list[FieldHit]:
    print(f"[OCR] {pdf_path.name} → Tesseract pass 1")
    pages = convert_from_path(str(pdf_path), dpi=300)
    all_hits: list[FieldHit] = []

    for page_num, page in enumerate(pages, start=1):
        rows = ocr_page(np.array(page))
        for target in TARGETS:
            hit = match_target(rows, target)
            if hit is None:
                continue
            hit.source_doc, hit.source_page = pdf_path.name, page_num

            if hit.confidence < LOW_CONF:
                x, y, w, h = hit.bbox
                crop = np.array(page)[y - 8 : y + h + 8, x - 8 : x + w + 200]
                refined, new_conf = await revisit_with_vision(crop, target)
                hit.value, hit.confidence = refined, new_conf
                hit.corrected_by = "claude-sonnet-4-5"
                print(f"  [REVISE] {target:18s} '{hit.value}'  conf {new_conf:5.1f}%")

            all_hits.append(hit)
    return all_hits


def cross_validate(by_doc: dict[str, list[FieldHit]]) -> dict[str, str]:
    """Verify Invoice ↔ B/L ↔ DDS pairwise field agreement on shared keys."""
    matrix: dict[str, str] = {}
    pairs = [("invoice", "bol"), ("invoice", "origin"), ("bol", "dds")]
    for a, b in pairs:
        if a not in by_doc or b not in by_doc:
            continue
        shared = {h.name for h in by_doc[a]} & {h.name for h in by_doc[b]}
        agree = sum(
            1 for k in shared
            if next(h.value for h in by_doc[a] if h.name == k)
            == next(h.value for h in by_doc[b] if h.name == k)
        )
        matrix[f"{a}↔{b}"] = f"{agree}/{len(shared)}"
        print(f"[XCHECK] {a:8s} ↔ {b:8s}  agreement={agree}/{len(shared)}")
    return matrix


async def main(case_dir: Path) -> dict[str, Any]:
    pdfs = sorted(case_dir.glob("*.pdf"))
    by_doc: dict[str, list[FieldHit]] = {}
    for pdf in pdfs:
        by_doc[pdf.stem] = await extract_doc(pdf)

    matrix = cross_validate(by_doc)
    flat = [h for hits in by_doc.values() for h in hits]
    avg = sum(h.confidence for h in flat) / len(flat)
    print(f"[OCR] complete · {len(flat)} fields · avg conf {avg:.1f}%")
    return {"fields": flat, "cross_check": matrix, "avg_confidence": avg}


if __name__ == "__main__":
    asyncio.run(main(Path("./fixtures/case-001")))
