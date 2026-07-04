# -*- coding: utf-8 -*-
"""`ProductionOrder` — a manufacturing/assembly order against a
`BillOfMaterials` (ADR-0014). Lives in the stock app (not products) because
it drives `StockReservation`/`StockMovement` postings and the stock app
already depends on products (`required_peers`); the reverse dependency
would be circular. Gated to `kind in {MANUFACTURED_GOOD, KIT}` via
`ProductKindPolicy` (ADR-0019) and registered as a kind-lock-set provider
(`services/kind_lock_providers.py`)."""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_kind_policy import check_gate
from koalixcrm.stock.models.choices import ProductionOrderStatus


class ProductionOrder(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("products.Product",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product"),
                                related_name="production_orders")
    bill_of_materials = models.ForeignKey("products.BillOfMaterials",
                                          on_delete=models.PROTECT,
                                          verbose_name=_("Bill of Materials"),
                                          related_name="production_orders")
    planned_qty = models.DecimalField(verbose_name=_("Planned Quantity"),
                                      max_digits=18,
                                      decimal_places=4,
                                      validators=[MinValueValidator(Decimal("0.0001"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"))
    status = models.CharField(verbose_name=_("Status"),
                              max_length=16,
                              choices=ProductionOrderStatus.choices,
                              default=ProductionOrderStatus.DRAFT)
    planned_start = models.DateTimeField(verbose_name=_("Planned Start"), null=True, blank=True)
    completed_at = models.DateTimeField(verbose_name=_("Completed At"), null=True, blank=True)
    document_type = models.ForeignKey("contenttypes.ContentType",
                                      on_delete=models.PROTECT,
                                      verbose_name=_("Document Type"),
                                      null=True,
                                      blank=True)
    document_id = models.PositiveIntegerField(verbose_name=_("Document ID"), null=True, blank=True)
    finished_serial_unit = models.ForeignKey("SerialUnit",
                                             on_delete=models.PROTECT,
                                             verbose_name=_("Finished Serial Unit"),
                                             related_name="produced_by_production_orders",
                                             null=True,
                                             blank=True,
                                             help_text=_("Set on completion when the finished "
                                                         "good's tracking_mode = SERIAL."))
    finished_batch = models.ForeignKey("Batch",
                                       on_delete=models.PROTECT,
                                       verbose_name=_("Finished Batch"),
                                       related_name="produced_by_production_orders",
                                       null=True,
                                       blank=True,
                                       help_text=_("Set on completion when the finished good's "
                                                   "tracking_mode = BATCH."))
    aggregation_group = models.UUIDField(verbose_name=_("Aggregation Group"), null=True, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.product_id is not None:
            check_gate("ProductionOrder", self.product.kind)
        if self.bill_of_materials_id is not None and self.product_id is not None:
            if self.bill_of_materials.product_id != self.product_id:
                raise ValidationError(
                    _("ProductionOrder.bill_of_materials must belong to ProductionOrder.product.")
                )

    def __str__(self) -> str:
        return f"ProductionOrder#{self.pk} {self.product_id} x {self.planned_qty} ({self.status})"

    class Meta:
        app_label = "stock"
        db_table = "stock_productionorder"
        verbose_name = _("Production Order")
        verbose_name_plural = _("Production Orders")
        ordering = ["-date_of_creation"]
        indexes = [
            models.Index(fields=["workspace", "status"], name="idx_productionorder_status"),
            models.Index(fields=["workspace", "product"], name="idx_productionorder_product"),
        ]
