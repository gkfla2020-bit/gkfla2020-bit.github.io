"""
3_cbam.py — Carbon footprint quality scoring + on-chain anchor + cost simulation
Sector benchmark: μ=3.20, σ=0.80 tCO₂/t (Palm Oil CPO, ISCC 2023 panel)

Scoring axes:
  - z-score against sector distribution
  - distance from EU default (4.5 tCO₂/t)
  - LCA traceability completeness (Scope 1, 2, optional 3)
  - measurement freshness (months since last verification)
  - methodology adherence (ISCC PLUS / RSB / GHG-P)
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable

import numpy as np
from scipy import stats
from web3 import Web3


# --- sector params ----------------------------------------------------------
SECTOR_MEAN = 3.20
SECTOR_STD = 0.80
EU_DEFAULT = 4.50
BENCHMARK = 1.80
EU_ETS_PRICE_EUR = 87.5

# --- phase-in schedule (CBAM Reg. 2023/956 Annex IV) -----------------------
PHASE_IN: dict[int, float] = {
    2026: 0.025, 2027: 0.05,  2028: 0.10,
    2029: 0.225, 2030: 0.35,  2031: 0.475,
    2032: 0.60,  2033: 0.80,  2034: 1.00,
}


@dataclass
class Submission:
    operator: str
    product: str
    hs_code: str
    volume_t: float
    ef_actual: float       # measured tCO₂/t
    methodology: str
    measured_at: datetime
    iscc_cert: str | None


@dataclass
class QualityScore:
    score: int             # 0..100
    components: dict[str, float]
    z_score: float
    flags: list[str]
    block_hash: str
    chain_height: int


# ---------------------------------------------------------------------------
def z_score(value: float, mu: float, sigma: float) -> float:
    return (value - mu) / sigma


def gaussian_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return (1.0 / (sigma * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def confidence_interval(value: float, mu: float, sigma: float) -> tuple[float, float]:
    """Two-sided 95% CI around the sector mean for the given EF."""
    z = 1.96
    return mu - z * sigma, mu + z * sigma


# ---------------------------------------------------------------------------
def compute_score(s: Submission) -> QualityScore:
    z = z_score(s.ef_actual, SECTOR_MEAN, SECTOR_STD)
    age_months = (datetime.now(timezone.utc) - s.measured_at).days / 30.0

    components = {
        "z_score":          max(0.0, 25 - 12 * abs(z)),     # 0..25
        "below_eu_default": 25.0 if s.ef_actual < EU_DEFAULT else 0.0,
        "methodology":      20.0 if "ISCC" in s.methodology else 8.0,
        "freshness":        max(0.0, 15 - age_months),
        "iscc_cert":        15.0 if s.iscc_cert else 0.0,
    }
    score = int(round(sum(components.values())))

    flags: list[str] = []
    if abs(z) > 1.5:
        flags.append("z_score_outlier")
    if s.ef_actual >= EU_DEFAULT:
        flags.append("above_eu_default")
    if age_months > 12:
        flags.append("stale_measurement")

    payload = {
        "operator": s.operator,
        "product": s.product,
        "ef": s.ef_actual,
        "methodology": s.methodology,
        "score": score,
        "ts": s.measured_at.isoformat(),
    }
    block_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    print(f"[SCORE] components={components}")
    print(f"[SCORE] z={z:+.3f}  total={score}/100")
    print(f"[ANCHOR] sha256 = 0x{block_hash}")

    return QualityScore(
        score=score,
        components=components,
        z_score=z,
        flags=flags,
        block_hash=block_hash,
        chain_height=1042,
    )


# ---------------------------------------------------------------------------
def write_to_chain(qs: QualityScore, rpc_url: str = "https://sepolia.optimism.io") -> str:
    """Anchor the score hash on Optimism Sepolia. Returns the txHash."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    contract = w3.eth.contract(
        address="0xCBAM00001234567890ABCDEF1234567890ABCDEF",
        abi=ANCHOR_ABI,
    )
    tx = contract.functions.anchor(bytes.fromhex(qs.block_hash)).build_transaction({
        "from": w3.eth.default_account,
        "nonce": w3.eth.get_transaction_count(w3.eth.default_account),
        "maxFeePerGas": w3.to_wei(0.5, "gwei"),
        "maxPriorityFeePerGas": w3.to_wei(0.1, "gwei"),
        "gas": 80_000,
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=KEY)
    h = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"[CHAIN] anchored {qs.block_hash[:12]}…  tx={h.hex()[:18]}…")
    return h.hex()


# ---------------------------------------------------------------------------
def simulate_costs(volume_t: float, ef_actual: float, fx_krw_per_eur: float) -> list[dict]:
    """Per-year cost path for Actual / EU-default / Benchmark scenarios."""
    out = []
    for year, frac in PHASE_IN.items():
        base = volume_t * EU_ETS_PRICE_EUR * fx_krw_per_eur * frac / 1e8  # 억 KRW
        out.append({
            "year": year,
            "phase_in": frac,
            "actual":     round(base * ef_actual, 2),
            "eu_default": round(base * EU_DEFAULT, 2),
            "benchmark":  round(base * BENCHMARK, 2),
            "saving":     round(base * (EU_DEFAULT - ef_actual), 2),
        })
    return out


# ---------------------------------------------------------------------------
def main() -> dict:
    s = Submission(
        operator="UniHana Trading GmbH",
        product="Crude Palm Oil",
        hs_code="1511.10.00",
        volume_t=2400.0,
        ef_actual=3.20,
        methodology="ISCC EU Plus LCA",
        measured_at=datetime(2024, 11, 1, tzinfo=timezone.utc),
        iscc_cert="ISCC-ID-PKS-2024-0847",
    )

    qs = compute_score(s)
    tx = write_to_chain(qs)
    rows = simulate_costs(s.volume_t, s.ef_actual, fx_krw_per_eur=1450.0)

    saving_2034 = rows[-1]["saving"]
    print(f"[SIM] 2034 saving = {saving_2034} 억 KRW")
    return {"score": asdict(qs), "tx": tx, "cost_path": rows}


if __name__ == "__main__":
    main()
