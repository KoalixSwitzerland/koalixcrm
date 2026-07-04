# -*- coding: utf-8 -*-
"""ADR-0017 (§Geltungsbereich, OQ-0015 open): a deliberately minimal
put-away *suggestion* — not the put-away *strategy* the ADR leaves for a
follow-up ADR. Heuristic: suggest the most recently used
`target_location`/`destination_location` for this `ProductVariant` in this
workspace (last-used-location heuristic). Returns `None` if no prior
location is on record; callers must not treat the suggestion as binding."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from koalixcrm.core.models.workspace import Workspace
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.location import Location


def suggest_location(*, workspace: "Workspace", variant: "ProductVariant") -> "Location | None":
    """OQ-0015 heuristic (explicitly non-binding): last-used location this
    variant was put away to, first from `GoodsReceiptLine.target_location`,
    falling back to the most recent `StockMovement.destination_location`
    for a `receiving` event."""
    from koalixcrm.stock.models.choices import BusinessStep
    from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine
    from koalixcrm.stock.models.stock_movement import StockMovement

    last_line = (
        GoodsReceiptLine.objects.filter(
            workspace=workspace, variant=variant, target_location__isnull=False,
        )
        .order_by("-goods_receipt__received_at", "-id")
        .select_related("target_location")
        .first()
    )
    if last_line is not None:
        return last_line.target_location

    last_movement = (
        StockMovement.objects.filter(
            workspace=workspace, variant=variant,
            business_step=BusinessStep.RECEIVING,
            destination_location__isnull=False,
        )
        .order_by("-occurred_at", "-id")
        .select_related("destination_location")
        .first()
    )
    if last_movement is not None:
        return last_movement.destination_location

    return None
