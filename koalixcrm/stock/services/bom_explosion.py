# -*- coding: utf-8 -*-
"""ADR-0014: flattened BOM-explosion snapshot computation. Plain,
synchronous service function — the ADR mentions a Celery task for
"recompute on BOM create/change", but that async path is not built: every
write path in this codebase (services, admin actions, the pick-time
staleness check) calls `explode()` directly and synchronously. Celery/SQS
infrastructure exists in this repo (`koalixcrm_microservices/celery_app.py`)
and runs a live SQS poller, so an out-of-band recompute path could be added
later as a Django-free worker that reads/writes via a `stock_api_py` client
(org ADR-0002 §2.4); none exists today.

Depth limits (ADR-0014): soft warning at depth > 10 (`ExplosionDepthWarning`
returned in the result, `PREASSEMBLE` recommended); hard rejection at depth
> 20 (`ExplosionDepthExceeded` raised, `PREASSEMBLE` enforced).

Justification: performance — recursive BOM-tree traversal (bounded depth 20) invoked synchronously mid-request (pick-time staleness check); a REST-mediated microservice would need one round-trip per tree level/branch, turning a bounded local computation into unbounded chatty latency; still needed with the microservice fleet deleted, since the pick-time check must complete inline. (Tier-2 GRANTED by architect.)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.products.models.bill_of_materials import BillOfMaterials

SOFT_DEPTH_LIMIT = 10
HARD_DEPTH_LIMIT = 20


class ExplosionDepthExceeded(ValidationError):
    """Raised when a BOM tree exceeds the hard depth limit (20 levels)."""


@dataclass
class ExplosionResult:
    rows: list = field(default_factory=list)
    max_depth: int = 0
    depth_warning: bool = False


def _explode_recursive(bill_of_materials: "BillOfMaterials", *, multiplier: Decimal, depth: int,
                       result: ExplosionResult) -> None:
    if depth > HARD_DEPTH_LIMIT:
        raise ExplosionDepthExceeded(
            _("BOM explosion for %(bom)s exceeds the hard depth limit of %(limit)s levels; "
              "use kit_mode = PREASSEMBLE instead.")
            % {"bom": bill_of_materials.product_id, "limit": HARD_DEPTH_LIMIT}
        )
    if depth > SOFT_DEPTH_LIMIT:
        result.depth_warning = True

    for bom_item in bill_of_materials.items.select_related(
        "component_product", "unit"
    ).all():
        effective_qty = bom_item.quantity * multiplier
        if bom_item.scrap_pct:
            effective_qty = effective_qty * (Decimal("1") + bom_item.scrap_pct / Decimal("100"))

        child_bom = getattr(bom_item.component_product, "bill_of_materials", None)
        if child_bom is not None:
            _explode_recursive(child_bom, multiplier=effective_qty, depth=depth + 1, result=result)
        else:
            result.rows.append({
                "depth": depth,
                "bom_item": bom_item,
                "effective_qty": effective_qty,
                "uom": bom_item.unit,
            })
        result.max_depth = max(result.max_depth, depth)


def compute_explosion(bill_of_materials: "BillOfMaterials") -> ExplosionResult:
    """Pure computation (no DB writes): returns the flattened leaf-component
    rows for one unit of the finished product."""
    result = ExplosionResult()
    _explode_recursive(bill_of_materials, multiplier=Decimal("1"), depth=1, result=result)
    return result


@transaction.atomic
def explode(bill_of_materials: "BillOfMaterials") -> ExplosionResult:
    """Compute the explosion and persist it to `BillOfMaterialsExplosion`,
    replacing any prior snapshot for this BOM. Returns the `ExplosionResult`
    (rows also reflect what got written, pinned to the BOM's current
    `version`)."""
    from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion

    result = compute_explosion(bill_of_materials)

    BillOfMaterialsExplosion.objects.filter(bill_of_materials=bill_of_materials).delete()
    for row in result.rows:
        BillOfMaterialsExplosion.objects.create(
            workspace=bill_of_materials.workspace,
            bill_of_materials=bill_of_materials,
            bom_version=bill_of_materials.version,
            depth=row["depth"],
            bom_item=row["bom_item"],
            effective_qty=row["effective_qty"],
            uom=row["uom"],
        )
    return result


def get_or_recompute_explosion(bill_of_materials: "BillOfMaterials"):
    """Pick-time read path: returns the current `BillOfMaterialsExplosion`
    queryset for `bill_of_materials`, recomputing synchronously if the
    stored snapshot's `bom_version` is stale or missing (ADR-0014)."""
    from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion

    existing = BillOfMaterialsExplosion.objects.filter(bill_of_materials=bill_of_materials)
    current_version = existing.first().bom_version if existing.exists() else None
    if current_version != bill_of_materials.version:
        explode(bill_of_materials)
        existing = BillOfMaterialsExplosion.objects.filter(bill_of_materials=bill_of_materials)
    return existing
