# -*- coding: utf-8 -*-
"""`GoodsReceiptLine` — a position on a `GoodsReceipt` (ADR-0017, incl.
Nachtrag 2026-07-04: `variant` is a mandatory FK to `ProductVariant`, not
`Product` — the receiving line always names the concrete variant it
received). `target_location` carries the (possibly heuristic) put-away
destination; `services/putaway.py` fills it with a minimal suggestion
(OQ-0015 stays open for the actual put-away *strategy*)."""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import GoodsReceiptLineStatus


class GoodsReceiptLine(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    goods_receipt = models.ForeignKey("GoodsReceipt",
                                      on_delete=models.CASCADE,
                                      verbose_name=_("Goods Receipt"),
                                      related_name="lines")
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="goods_receipt_lines")
    expected_qty = models.DecimalField(verbose_name=_("Expected Quantity"),
                                       max_digits=18,
                                       decimal_places=4,
                                       validators=[MinValueValidator(Decimal("0"))])
    received_qty = models.DecimalField(verbose_name=_("Received Quantity"),
                                       max_digits=18,
                                       decimal_places=4,
                                       default=Decimal("0"),
                                       validators=[MinValueValidator(Decimal("0"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"),
                            null=True,
                            blank=True)
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="goods_receipt_lines",
                              null=True,
                              blank=True)
    serial_unit = models.ForeignKey("SerialUnit",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Serial Unit"),
                                    related_name="goods_receipt_lines",
                                    null=True,
                                    blank=True,
                                    help_text=_("Minimal serial-capture field for "
                                                "tracking_mode = SERIAL lines."))
    target_location = models.ForeignKey("Location",
                                        on_delete=models.PROTECT,
                                        verbose_name=_("Target Location"),
                                        related_name="goods_receipt_lines",
                                        null=True,
                                        blank=True,
                                        help_text=_("Put-away destination; may be filled by the "
                                                    "OQ-0015 heuristic suggestion or set manually."))
    line_status = models.CharField(verbose_name=_("Line Status"),
                                   max_length=16,
                                   choices=GoodsReceiptLineStatus.choices,
                                   default=GoodsReceiptLineStatus.PENDING)
    notes = models.TextField(verbose_name=_("Notes"), null=True, blank=True)
    posted_movement = models.ForeignKey("StockMovement",
                                        on_delete=models.PROTECT,
                                        verbose_name=_("Posted Movement"),
                                        related_name="goods_receipt_lines",
                                        null=True,
                                        blank=True,
                                        help_text=_("The receiving StockMovement posted for this "
                                                    "line when the parent GoodsReceipt completed."))

    def clean(self) -> None:
        super().clean()
        if self.batch_id is not None and self.variant_id is not None:
            if self.batch.variant_id != self.variant_id:
                raise ValidationError(
                    _("GoodsReceiptLine.batch must belong to the same ProductVariant as "
                      "GoodsReceiptLine.variant.")
                )
        if self.serial_unit_id is not None and self.variant_id is not None:
            if self.serial_unit.variant_id != self.variant_id:
                raise ValidationError(
                    _("GoodsReceiptLine.serial_unit must belong to the same ProductVariant as "
                      "GoodsReceiptLine.variant.")
                )

    def __str__(self) -> str:
        return f"{self.goods_receipt_id}: {self.variant_id} x {self.received_qty}/{self.expected_qty}"

    class Meta:
        app_label = "stock"
        db_table = "stock_goodsreceiptline"
        verbose_name = _("Goods Receipt Line")
        verbose_name_plural = _("Goods Receipt Lines")
        ordering = ["goods_receipt_id", "id"]
        indexes = [
            models.Index(fields=["workspace", "variant"], name="idx_goodsreceiptline_variant"),
            models.Index(fields=["workspace", "line_status"], name="idx_goodsreceiptline_status"),
        ]
