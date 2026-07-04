# -*- coding: utf-8 -*-
"""ADR-0016: `POST /api/v1/scan/resolve` resolution logic. Two-stage:
GS1 AI parsing first (`services/gs1_parser.py`), then free-text exact
match. GS1 always wins over free text; free text is only attempted when no
GS1 AI prefix was recognized at all.

Workspace-scoping (ADR-0016 §Workspace-Scoping): every identifier type is
workspace-scoped except `ProductVariant.gtin`, which is catalog-wide
(Nachtrag 2026-07-04, OQ-0022) — a GTIN hit is looked up without a
workspace filter. `ProductVariant.sku` free-text matching (Stufe 2, Regel
3) *is* workspace-scoped."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from koalixcrm.stock.services import gs1_parser

if TYPE_CHECKING:
    from koalixcrm.core.models.workspace import Workspace


class ScanNotFound(Exception):
    pass


class ScanMultipleMatches(Exception):
    def __init__(self, candidates: list[dict]):
        super().__init__("Multiple candidates matched.")
        self.candidates = candidates


@dataclass(frozen=True)
class ScanMatch:
    kind: str
    id: Any
    matched_field: str
    instance: Any = field(repr=False, default=None)

    def as_dict(self) -> dict:
        return {"kind": self.kind, "id": self.id, "matched_field": self.matched_field}


def _resolve_gs1(code: str, *, workspace: "Workspace") -> ScanMatch | None:
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.handling_unit import HandlingUnit
    from koalixcrm.stock.models.location import Location
    from koalixcrm.stock.models.serial_unit import SerialUnit

    parsed = gs1_parser.parse(code)
    if not parsed.matched:
        return None

    if parsed.is_sgtin:
        unit = SerialUnit.objects.filter(workspace=workspace, global_uid=parsed.serial).first()
        if unit is not None:
            return ScanMatch("serial_unit", unit.pk, "global_uid", unit)
        return None

    if parsed.giai:
        unit = SerialUnit.objects.filter(workspace=workspace, global_uid=parsed.giai).first()
        if unit is not None:
            return ScanMatch("serial_unit", unit.pk, "global_uid", unit)
        return None

    if parsed.sscc:
        handling_unit = HandlingUnit.objects.filter(workspace=workspace, sscc=parsed.sscc).first()
        if handling_unit is not None:
            return ScanMatch("handling_unit", handling_unit.pk, "sscc", handling_unit)
        return None

    if parsed.gln:
        location = Location.objects.filter(workspace=workspace, external_ref=parsed.gln).first()
        if location is not None:
            return ScanMatch("location", location.pk, "external_ref", location)
        return None

    if parsed.gtin:
        # ADR-0016 Nachtrag 2026-07-04: catalog-wide, no workspace filter.
        variant = ProductVariant.objects.filter(gtin=parsed.gtin).first()
        if variant is not None:
            return ScanMatch("product_variant", variant.pk, "gtin", variant)
        return None

    return None


def _resolve_free_text(code: str, *, workspace: "Workspace") -> list[ScanMatch]:
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.location import Location
    from koalixcrm.stock.models.serial_unit import SerialUnit

    matches: list[ScanMatch] = []

    location = Location.objects.filter(workspace=workspace, external_ref=code).first()
    if location is not None:
        matches.append(ScanMatch("location", location.pk, "external_ref", location))

    unit = SerialUnit.objects.filter(workspace=workspace, global_uid=code).first()
    if unit is not None:
        matches.append(ScanMatch("serial_unit", unit.pk, "global_uid", unit))

    variant = ProductVariant.objects.filter(workspace=workspace, sku=code).first()
    if variant is not None:
        matches.append(ScanMatch("product_variant", variant.pk, "sku", variant))

    return matches


def resolve(code: str, *, workspace: "Workspace") -> ScanMatch:
    gs1_match = _resolve_gs1(code, workspace=workspace)
    if gs1_match is not None:
        return gs1_match

    parsed = gs1_parser.parse(code)
    if parsed.matched:
        # A GS1 AI prefix was recognized but resolved to nothing: per
        # ADR-0016, stage 2 (free text) is not started in that case.
        raise ScanNotFound()

    free_text_matches = _resolve_free_text(code, workspace=workspace)
    if not free_text_matches:
        raise ScanNotFound()
    if len(free_text_matches) > 1:
        raise ScanMultipleMatches([match.as_dict() for match in free_text_matches])
    return free_text_matches[0]
