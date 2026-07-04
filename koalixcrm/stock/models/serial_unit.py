# -*- coding: utf-8 -*-
"""`SerialUnit` — an individually tracked physical unit of a
`ProductVariant` (ADR-0012; Amendment 2026-07-04 rekeys the FK from
`Product` to `ProductVariant` per ADR-0021). Soft-delete-forever:
decommissioned rows (`decommissioned_at` set) are never hard-deleted by
default; `delete()` enforces the ADR-0012 retention floor via
`serial_unit_retention.assert_deletable`."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_kind_policy import check_gate
from koalixcrm.stock.models.choices import SerialConditionState
from koalixcrm.stock.services.serial_unit_retention import assert_deletable


class SerialUnit(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="serial_units")
    serial_number = models.CharField(verbose_name=_("Serial Number"), max_length=100)
    global_uid = models.CharField(verbose_name=_("Global UID (ISO/IEC 15459)"),
                                  max_length=100,
                                  null=True,
                                  blank=True)
    production_date = models.DateField(verbose_name=_("Production Date"), null=True, blank=True)
    warranty_expiry = models.DateField(verbose_name=_("Warranty Expiry"), null=True, blank=True)
    condition_state = models.CharField(verbose_name=_("Condition State"),
                                       max_length=16,
                                       choices=SerialConditionState.choices,
                                       default=SerialConditionState.NEW)
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="serial_units",
                              null=True,
                              blank=True)
    decommissioned_at = models.DateTimeField(verbose_name=_("Decommissioned At"), null=True, blank=True)
    notes = models.TextField(verbose_name=_("Notes"), null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.variant_id is not None:
            check_gate("StockFact", self.variant.product.kind)
        if self.batch_id is not None and self.batch.variant_id != self.variant_id:
            raise ValidationError(
                _("A SerialUnit's Batch must belong to the same ProductVariant.")
            )

    def decommission(self) -> None:
        if self.decommissioned_at is None:
            self.decommissioned_at = timezone.now()
            self.save(update_fields=["decommissioned_at"])

    def delete(self, *args, **kwargs):
        assert_deletable(self)
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.serial_number

    class Meta:
        app_label = "stock"
        db_table = "stock_serialunit"
        verbose_name = _("Serial Unit")
        verbose_name_plural = _("Serial Units")
        ordering = ["serial_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "variant", "serial_number"],
                name="uniq_serial_number_per_variant",
            ),
            models.UniqueConstraint(
                fields=["workspace", "global_uid"],
                condition=Q(global_uid__isnull=False),
                name="uniq_serial_global_uid_per_workspace",
            ),
        ]
        indexes = [
            models.Index(
                fields=["workspace"],
                name="idx_serialunit_active",
                condition=Q(decommissioned_at__isnull=True),
            ),
        ]
