# -*- coding: utf-8 -*-
"""`StockBalance` — denormalized six-segment aggregate per
`(workspace, variant, location)` (ADR-0010; Amendment 2026-07-04 rekeys the
FK from `Product` to `ProductVariant` per ADR-0021 — the product is
reachable only via `variant.product`).

`StockBalance` rows are kept current exclusively by
`services/movement_posting.py` (ADR-0011: synchronous, same-transaction
`StockMovement` posting) and `services/reservation_lifecycle.py` (for the
`booked`/`reserved_for_document` segments, which are not physical
movements). Direct mutation outside those services bypasses the audit
trail and must not be used; the Django admin registers this model
read-only for that reason.

ATP formula (REQ-0020 / ADR-0010):
    ATP = qty_on_hand - qty_booked - qty_reserved_for_document + qty_ordered
`qty_in_transit` and `qty_quarantine` are excluded from ATP (not
disponible)."""
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class StockBalance(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="stock_balances")
    location = models.ForeignKey("Location",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("Location"),
                                 related_name="stock_balances")
    qty_on_hand = models.DecimalField(verbose_name=_("Qty On Hand"),
                                      max_digits=18, decimal_places=4,
                                      default=Decimal("0"),
                                      validators=[MinValueValidator(Decimal("0"))])
    qty_booked = models.DecimalField(verbose_name=_("Qty Booked"),
                                     max_digits=18, decimal_places=4,
                                     default=Decimal("0"),
                                     validators=[MinValueValidator(Decimal("0"))])
    qty_reserved_for_document = models.DecimalField(verbose_name=_("Qty Reserved For Document"),
                                                     max_digits=18, decimal_places=4,
                                                     default=Decimal("0"),
                                                     validators=[MinValueValidator(Decimal("0"))])
    qty_ordered = models.DecimalField(verbose_name=_("Qty Ordered"),
                                      max_digits=18, decimal_places=4,
                                      default=Decimal("0"),
                                      validators=[MinValueValidator(Decimal("0"))])
    qty_in_transit = models.DecimalField(verbose_name=_("Qty In Transit"),
                                         max_digits=18, decimal_places=4,
                                         default=Decimal("0"),
                                         validators=[MinValueValidator(Decimal("0"))])
    qty_quarantine = models.DecimalField(verbose_name=_("Qty Quarantine"),
                                         max_digits=18, decimal_places=4,
                                         default=Decimal("0"),
                                         validators=[MinValueValidator(Decimal("0"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"))
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    @property
    def atp(self) -> Decimal:
        return self.qty_on_hand - self.qty_booked - self.qty_reserved_for_document + self.qty_ordered

    def __str__(self) -> str:
        return f"{self.variant_id}@{self.location_id}: on_hand={self.qty_on_hand} atp={self.atp}"

    class Meta:
        app_label = "stock"
        db_table = "stock_stockbalance"
        verbose_name = _("Stock Balance")
        verbose_name_plural = _("Stock Balances")
        ordering = ["variant", "location"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "variant", "location"],
                name="uniq_stockbalance_key",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "variant", "location"], name="idx_stockbalance_var_loc"),
        ]
