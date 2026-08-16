# -*- coding: utf-8 -*-
"""`Batch` — a production batch/lot for a `ProductVariant` (ADR-0012;
Amendment 2026-07-04 rekeys the FK from `Product` to `ProductVariant` per
ADR-0021). FEFO index on `(workspace, variant, expiry_date)`."""
from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_kind_policy import check_gate


class Batch(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="batches")
    batch_number = models.CharField(verbose_name=_("Batch Number"), max_length=100)
    supplier_lot_number = models.CharField(verbose_name=_("Supplier Lot Number"),
                                           max_length=100,
                                           null=True,
                                           blank=True)
    production_date = models.DateField(verbose_name=_("Production Date"), null=True, blank=True)
    expiry_date = models.DateField(verbose_name=_("Expiry Date"), null=True, blank=True)
    best_before_date = models.DateField(verbose_name=_("Best Before Date"), null=True, blank=True)
    received_at = models.DateTimeField(verbose_name=_("Received At"), default=timezone.now)
    quarantine = models.BooleanField(verbose_name=_("Quarantine"), default=False)
    notes = models.TextField(verbose_name=_("Notes"), null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.variant_id is not None:
            check_gate("StockFact", self.variant.product.kind)

    def __str__(self) -> str:
        return f"{self.batch_number} ({self.variant_id})"

    class Meta:
        app_label = "stock"
        db_table = "stock_batch"
        verbose_name = _("Batch")
        verbose_name_plural = _("Batches")
        ordering = ["expiry_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "variant", "batch_number"],
                name="uniq_batch_number_per_variant",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "variant", "expiry_date"], name="idx_batch_fefo"),
        ]
