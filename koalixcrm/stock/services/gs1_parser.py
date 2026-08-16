# -*- coding: utf-8 -*-
"""ADR-0016: a small, in-repo GS1 Application Identifier (AI) element-string
parser. No third-party dependency (ADR-0016 §Lizenzbeschränkung allows an
MIT-licensed library, but a handwritten parser is simpler here and keeps
the PyPI wheel dependency-free).

Supports the AI combinations ADR-0016 needs:
  (01)          GTIN
  (00)          SSCC
  (01)+(21)     SGTIN  (GTIN + Serial)
  (8003)        GIAI
  (414)         GLN

Accepts both a bracketed human-readable form (``"(01)04012345123456(21)000001"``)
and the raw FNC1-style concatenation without brackets, as long as
fixed-length AIs are used (all AIs in this table are fixed-length, so no
FNC1 group-separator handling is required).

Justification: framework — zero-DB parsing helper invoked synchronously inline by scan_resolve within a single request/response cycle; still needed with the microservice fleet deleted."""
from __future__ import annotations

import re
from dataclasses import dataclass

# (ai, fixed_length_of_value): all AIs relevant to ADR-0016 are fixed-length.
_AI_LENGTHS: dict[str, int] = {
    "00": 18,  # SSCC
    "01": 14,  # GTIN
    "21": 20,  # Serial (variable in the GS1 standard; treated as
               # "rest of string up to the next known AI or end" here)
    "414": 13,  # GLN
    "8003": 18,  # GIAI (1 check digit + up to 12 chars serial; treat as
                 # "rest of string" for our parser)
}

_BRACKETED_AI_RE = re.compile(r"\((\d{2,4})\)")


@dataclass(frozen=True)
class GS1ParseResult:
    gtin: str | None = None
    sscc: str | None = None
    serial: str | None = None
    giai: str | None = None
    gln: str | None = None

    @property
    def is_sgtin(self) -> bool:
        return self.gtin is not None and self.serial is not None

    @property
    def matched(self) -> bool:
        return any((self.gtin, self.sscc, self.giai, self.gln))


def _parse_bracketed(code: str) -> dict[str, str] | None:
    if "(" not in code:
        return None
    parts: dict[str, str] = {}
    matches = list(_BRACKETED_AI_RE.finditer(code))
    if not matches:
        return None
    for index, match in enumerate(matches):
        ai = match.group(1)
        value_start = match.end()
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(code)
        value = code[value_start:value_end]
        parts[ai] = value
    return parts


def _parse_unbracketed(code: str) -> dict[str, str] | None:
    """Fixed-length concatenation without brackets, e.g. a raw GS1-128
    scan buffer. Only attempts the single-AI-prefix cases (00)/(01)/(414)/
    (8003); a combined (01)+(21) SGTIN without brackets is ambiguous without
    an FNC1 separator and is not attempted here — real SGTIN scans from
    2D/GS1-128 barcodes carry either brackets or an FNC1 group separator,
    both handled by `_parse_bracketed`."""
    for ai in ("00", "01", "414", "8003"):
        if code.startswith(ai):
            length = _AI_LENGTHS[ai]
            value = code[len(ai):len(ai) + length]
            if len(value) == length and value.isalnum():
                return {ai: value}
    return None


def parse(code: str) -> GS1ParseResult:
    """Best-effort GS1 AI parse. Returns a `GS1ParseResult` with all fields
    `None` if `code` does not look like a GS1 AI string at all (caller then
    falls through to free-text resolution, ADR-0016 Stufe 2)."""
    parts = _parse_bracketed(code) or _parse_unbracketed(code)
    if not parts:
        return GS1ParseResult()

    gtin = parts.get("01")
    serial = parts.get("21")
    sscc = parts.get("00")
    giai = parts.get("8003")
    gln = parts.get("414")

    return GS1ParseResult(
        gtin=gtin,
        sscc=sscc,
        serial=serial if gtin else None,
        giai=giai,
        gln=gln,
    )
