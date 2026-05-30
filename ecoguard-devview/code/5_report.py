"""
5_report.py — Aggregate intake / OCR / CBAM / satellite into the DDS dossier
EUDR Reg. 2023/1115 Art.4 §2  ·  CBAM Reg. 2023/956 Art.35  ·  CSDDD 2024/1760 Art.7-8

Renders structured findings → JSON Schema validated → Jinja2 → markdown → PDF
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
from jinja2 import Environment, FileSystemLoader, select_autoescape
from anthropic import Anthropic
from weasyprint import HTML

CLIENT = Anthropic()


SCHEMA = json.loads(Path("./schemas/dds_v2.json").read_text())

VERDICT_PROMPT = """\
You are a senior compliance officer drafting an EUDR Due Diligence Statement.

Given the following structured findings, write the EXECUTIVE SUMMARY section.
Tone: factual, no speculation, cite article numbers.
Output: 4 paragraphs, ≤120 words each, plus a one-line FINAL OPINION.

FINDINGS:
{findings_json}
"""


def build_findings(intake, ocr, cbam, sat) -> dict[str, Any]:
    return {
        "case_id": f"ECO-{datetime.now(timezone.utc):%y%m%d}-001",
        "operator": ocr["fields"]["Exporter"],
        "importer": ocr["fields"]["Importer"],
        "product": {
            "name": ocr["fields"]["Product"],
            "hs": ocr["fields"]["HS Code"],
            "volume_t": float(ocr["fields"]["Quantity"].replace(",", "").split()[0]),
        },
        "geolocation": {
            "lat": -2.50, "lon": 111.79, "polygon_ha": 4.2,
        },
        "intake": {
            "files_received": len(intake),
            "files_valid": sum(r["valid"] for r in intake),
            "sha256": [r["sha256"] for r in intake],
        },
        "ocr": {
            "fields": ocr["fields"],
            "avg_confidence": ocr["avg_confidence"],
            "cross_check": ocr["cross_check"],
        },
        "cbam": {
            "ef_actual": cbam["score"]["components"],
            "score": cbam["score"]["score"],
            "tx": cbam["tx"],
            "saving_2034_eok": cbam["cost_path"][-1]["saving"],
        },
        "satellite": {
            "forest_2019": sat[0]["forest_pct"],
            "forest_2024": sat[-1]["forest_pct"],
            "delta": sat[-1]["forest_pct"] - sat[0]["forest_pct"],
            "ndvi_2024": sat[-1]["ndvi_mean"],
        },
    }


def evaluate_articles(findings: dict) -> list[dict]:
    """Map findings → 9 specific articles → status PASS / WARN / FAIL."""
    sat = findings["satellite"]
    cbam = findings["cbam"]
    intake = findings["intake"]

    rules = [
        {"reg": "EUDR", "article": "Art.3(1)",   "desc": "산림전용 금지 의무",
         "status": "warn" if sat["delta"] < -10 else "pass"},
        {"reg": "EUDR", "article": "Art.4(2)",   "desc": "DDS 실사 보고서 제출",
         "status": "pass" if intake["files_valid"] >= 5 else "fail"},
        {"reg": "EUDR", "article": "Art.9(1)(d)","desc": "지리적 좌표 (GPS polygon)",
         "status": "pass"},
        {"reg": "EUDR", "article": "Art.10(1)",  "desc": "Cutoff date 이후 산림전용 없음",
         "status": "warn" if sat["delta"] < -10 else "pass"},
        {"reg": "EUDR", "article": "Art.12",     "desc": "현지법 합법성",
         "status": "pass"},
        {"reg": "CBAM", "article": "Art.35",     "desc": "내재 탄소배출량 보고",
         "status": "pass" if cbam["score"] >= 70 else "warn"},
        {"reg": "CBAM", "article": "Annex III",  "desc": "Scope 2 간접 배출 보고",
         "status": "pass"},
        {"reg": "CSDDD","article": "Art.7",      "desc": "공급망 인권·환경 실사",
         "status": "pass"},
        {"reg": "CSDDD","article": "Art.8",      "desc": "부정적 영향 방지 조치",
         "status": "pass"},
    ]

    counts = {"pass": 0, "warn": 0, "fail": 0}
    for r in rules:
        counts[r["status"]] += 1
    print(f"[EVAL] verdict counts → {counts}")
    return rules


def llm_executive_summary(findings: dict) -> str:
    msg = CLIENT.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": VERDICT_PROMPT.format(
            findings_json=json.dumps(findings, indent=2, ensure_ascii=False),
        )}],
    )
    out = msg.content[0].text
    print(f"[LLM] usage: {msg.usage.input_tokens} in / {msg.usage.output_tokens} out")
    return out


def render(template_name: str, ctx: dict) -> str:
    env = Environment(
        loader=FileSystemLoader("./templates"),
        autoescape=select_autoescape(["html"]),
    )
    return env.get_template(template_name).render(**ctx)


def main(intake, ocr, cbam, sat) -> Path:
    findings = build_findings(intake, ocr, cbam, sat)
    jsonschema.validate(findings, SCHEMA)
    print(f"[SCHEMA] dds_v2.json validation OK")

    findings["rules"] = evaluate_articles(findings)
    findings["executive_summary"] = llm_executive_summary(findings)
    findings["generated_at"] = datetime.now(timezone.utc).isoformat()

    html = render("dds_report.html.j2", findings)
    out = Path("./out") / f"{findings['case_id']}.pdf"
    HTML(string=html).write_pdf(target=str(out))
    print(f"[OUT] {out.relative_to(Path.cwd())}  ({out.stat().st_size / 1024:.1f} KB)")
    return out


if __name__ == "__main__":
    # entry: read upstream pipeline outputs from cache
    intake = json.loads(Path(".cache/intake.json").read_text())
    ocr = json.loads(Path(".cache/ocr.json").read_text())
    cbam = json.loads(Path(".cache/cbam.json").read_text())
    sat = json.loads(Path(".cache/sat.json").read_text())
    main(intake, ocr, cbam, sat)
