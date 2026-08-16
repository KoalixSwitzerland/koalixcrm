# -*- coding: utf-8 -*-
"""ADR-0017: `GoodsReceipt` DRAFT -> IN_PROGRESS -> COMPLETED/CANCELLED
state machine. The `COMPLETED` transition posts exactly one `receiving`
`StockMovement` per `GoodsReceiptLine` with `received_qty > 0`, synchronously
in the same DB transaction (via `services/movement_posting.post_movement`),
consistent with the ADR-0011 invariant. `CANCELLED` never posts a movement
(ADR-0017 §Consequences/Negative: a partially-booked-then-cancelled receipt
needs a manual adjustment).

Justification: transactional integrity — complete() posts the receiving StockMovement via movement_posting.post_movement in the same DB transaction as the state transition (ADR-0011 synchronous-posting invariant); still needed with the microservice fleet deleted. (Tier-2 GRANTED by architect.)"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.stock.models.choices import GoodsReceiptLineStatus, GoodsReceiptStatus

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from koalixcrm.stock.models.goods_receipt import GoodsReceipt
    from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine


def start(goods_receipt: "GoodsReceipt") -> "GoodsReceipt":
    if goods_receipt.status != GoodsReceiptStatus.DRAFT:
        raise ValidationError(
            _("Only a DRAFT GoodsReceipt can transition to IN_PROGRESS.")
        )
    goods_receipt.status = GoodsReceiptStatus.IN_PROGRESS
    goods_receipt.full_clean()
    goods_receipt.save()
    return goods_receipt


def confirm_line(line: "GoodsReceiptLine", *, received_qty=None) -> "GoodsReceiptLine":
    """Records a scanned/counted quantity for one line and derives its
    `line_status`: `CONFIRMED` when `received_qty == expected_qty`,
    `MISMATCHED` otherwise (UC-0010 discrepancy identification)."""
    if line.goods_receipt.status not in (GoodsReceiptStatus.DRAFT, GoodsReceiptStatus.IN_PROGRESS):
        raise ValidationError(
            _("Cannot confirm a line of a GoodsReceipt that is not DRAFT or IN_PROGRESS.")
        )
    if received_qty is not None:
        line.received_qty = received_qty
    line.line_status = (
        GoodsReceiptLineStatus.CONFIRMED
        if line.received_qty == line.expected_qty
        else GoodsReceiptLineStatus.MISMATCHED
    )
    line.full_clean()
    line.save()
    return line


@transaction.atomic
def complete(goods_receipt: "GoodsReceipt", *, occurred_at=None, created_by: "User | None" = None,
            auto_suggest_location: bool = True) -> "GoodsReceipt":
    """IN_PROGRESS -> COMPLETED: posts one `receiving` StockMovement per
    line with `received_qty > 0`, synchronously in one transaction."""
    from koalixcrm.stock.models.choices import BusinessStep, EventType
    from koalixcrm.stock.services import putaway
    from koalixcrm.stock.services.movement_posting import post_movement

    if goods_receipt.status != GoodsReceiptStatus.IN_PROGRESS:
        raise ValidationError(
            _("Only an IN_PROGRESS GoodsReceipt can be completed.")
        )

    occurred_at = occurred_at or timezone.now()

    for line in goods_receipt.lines.select_related("variant", "target_location", "batch", "uom").all():
        if line.received_qty <= 0:
            continue

        target_location = line.target_location
        if target_location is None and auto_suggest_location:
            target_location = putaway.suggest_location(workspace=goods_receipt.workspace, variant=line.variant)
        if target_location is None:
            raise ValidationError(
                _("GoodsReceiptLine %(line)s has no target_location and no put-away "
                  "suggestion could be derived; set one before completing.")
                % {"line": line.pk}
            )

        movement = post_movement(
            workspace=goods_receipt.workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RECEIVING,
            occurred_at=occurred_at,
            variant=line.variant,
            destination_location=target_location,
            batch=line.batch,
            serial_unit=line.serial_unit,
            qty=line.received_qty,
            uom=line.uom,
            document=goods_receipt,
            created_by=created_by,
        )
        line.target_location = target_location
        line.posted_movement = movement
        line.save(update_fields=["target_location", "posted_movement"])

    goods_receipt.status = GoodsReceiptStatus.COMPLETED
    goods_receipt.full_clean()
    goods_receipt.save()
    return goods_receipt


def cancel(goods_receipt: "GoodsReceipt") -> "GoodsReceipt":
    if goods_receipt.status not in (GoodsReceiptStatus.DRAFT, GoodsReceiptStatus.IN_PROGRESS):
        raise ValidationError(
            _("Only a DRAFT or IN_PROGRESS GoodsReceipt can be cancelled.")
        )
    goods_receipt.status = GoodsReceiptStatus.CANCELLED
    goods_receipt.full_clean()
    goods_receipt.save()
    return goods_receipt


@transaction.atomic
def ingest(*, workspace, supplier_party, lines: list[dict], external_doc_ref=None, received_at=None,
          notes=None, created_by: "User | None" = None) -> "GoodsReceipt":
    """`POST /api/.../goods-receipts/ingest/`: builds a DRAFT `GoodsReceipt`
    with its lines from a structured JSON payload (delivery-note shaped;
    OCR/EDI adapters produce this payload externally, ADR-0017). Each
    `lines` dict accepts: `variant` (ProductVariant instance or id),
    `expected_qty`, `uom` (optional), `batch` (optional), `target_location`
    (optional)."""
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.goods_receipt import GoodsReceipt
    from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine

    goods_receipt = GoodsReceipt(
        workspace=workspace,
        supplier_party=supplier_party,
        external_doc_ref=external_doc_ref,
        received_at=received_at or timezone.now(),
        notes=notes,
        created_by=created_by,
        status=GoodsReceiptStatus.DRAFT,
    )
    goods_receipt.full_clean()
    goods_receipt.save()

    for raw_line in lines:
        variant = raw_line["variant"]
        if not hasattr(variant, "pk"):
            variant = ProductVariant.objects.get(pk=variant)
        line = GoodsReceiptLine(
            workspace=workspace,
            goods_receipt=goods_receipt,
            variant=variant,
            expected_qty=raw_line["expected_qty"],
            uom=raw_line.get("uom"),
            batch=raw_line.get("batch"),
            target_location=raw_line.get("target_location"),
        )
        line.full_clean()
        line.save()

    return goods_receipt
