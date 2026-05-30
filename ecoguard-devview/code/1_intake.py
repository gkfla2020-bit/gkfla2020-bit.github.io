"""
1_intake.py — Document intake & integrity validation
EUDR Reg. 2023/1115 Art.4 — Operator submission requirements

Pipeline: PDF parse → magic-byte verify → metadata extract → SHA-256 → schema check
"""

from pathlib import Path
import hashlib
import mimetypes
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
import pypdf


REQUIRED_DOCS = {
    "invoice":  {"label": "Commercial Invoice",        "accept": [".pdf", ".png", ".jpg"]},
    "bol":      {"label": "Bill of Lading",            "accept": [".pdf"]},
    "origin":   {"label": "Certificate of Origin",     "accept": [".pdf", ".png"]},
    "phyto":    {"label": "Phytosanitary Certificate", "accept": [".pdf"]},
    "dds":      {"label": "Self-Declared DDS",         "accept": [".pdf"]},
    "gps":      {"label": "GPS Polygon (GeoJSON)",     "accept": [".geojson", ".json"]},
}

PDF_MAGIC = b"%PDF-"
MAX_BYTES = 50 * 1024 * 1024  # 50 MB ceiling


class IntakeRecord(BaseModel):
    slot: str
    filename: str
    mime: str
    bytes: int = Field(gt=0, le=MAX_BYTES)
    sha256: str = Field(min_length=64, max_length=64)
    page_count: int | None = None
    valid: bool
    issues: list[str] = []
    received_at: datetime


def sha256_file(path: Path) -> str:
    """Stream the file in 1 MiB chunks — avoids loading full PDF into memory."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_pdf_magic(path: Path) -> bool:
    with path.open("rb") as f:
        head = f.read(5)
    return head == PDF_MAGIC


def parse_pdf_metadata(path: Path) -> tuple[int, dict]:
    reader = pypdf.PdfReader(str(path))
    if reader.is_encrypted:
        raise ValueError(f"Encrypted PDF rejected: {path.name}")
    n_pages = len(reader.pages)
    meta = dict(reader.metadata or {})
    return n_pages, meta


def validate_slot(slot: str, path: Path) -> IntakeRecord:
    issues: list[str] = []

    size = path.stat().st_size
    if size > MAX_BYTES:
        issues.append(f"file_too_large: {size} > {MAX_BYTES}")

    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "application/octet-stream"
    accept = REQUIRED_DOCS[slot]["accept"]
    if path.suffix.lower() not in accept:
        issues.append(f"bad_extension: {path.suffix} not in {accept}")

    if path.suffix.lower() == ".pdf" and not verify_pdf_magic(path):
        issues.append("magic_byte_mismatch: not a real PDF")

    page_count = None
    if path.suffix.lower() == ".pdf":
        try:
            page_count, _meta = parse_pdf_metadata(path)
        except Exception as e:
            issues.append(f"pdf_parse_error: {e}")

    digest = sha256_file(path)

    return IntakeRecord(
        slot=slot,
        filename=path.name,
        mime=mime,
        bytes=size,
        sha256=digest,
        page_count=page_count,
        valid=(len(issues) == 0),
        issues=issues,
        received_at=datetime.now(timezone.utc),
    )


def run(case_dir: Path) -> list[IntakeRecord]:
    print(f"[INTAKE] scanning {case_dir} for {len(REQUIRED_DOCS)} required slots")
    records: list[IntakeRecord] = []
    for slot, spec in REQUIRED_DOCS.items():
        match = next(
            (p for p in case_dir.iterdir() if p.stem.lower().startswith(slot.lower())),
            None,
        )
        if match is None:
            print(f"  [WARN]  slot={slot:8s} status=MISSING  ({spec['label']})")
            continue
        rec = validate_slot(slot, match)
        flag = "OK  " if rec.valid else "FAIL"
        print(f"  [{flag}]  slot={slot:8s} bytes={rec.bytes:>8,d}  pages={rec.page_count}  sha={rec.sha256[:12]}…")
        records.append(rec)
    print(f"[INTAKE] complete · {sum(r.valid for r in records)}/{len(records)} valid")
    return records


if __name__ == "__main__":
    case = Path("./fixtures/case-001")
    out = run(case)
    for r in out:
        print(r.model_dump_json(indent=2))
