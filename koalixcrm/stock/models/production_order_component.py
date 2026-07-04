# -*- coding: utf-8 -*-
"""`ProductionOrderComponent` — a component line of a `ProductionOrder`
(ADR-0014). `variant` is mandatory (Nachtrag 2026-07-04, OQ-0019); it is
resolved by `services/component_variant_resolution.py` following the
three-step order also used by ADR-0011: explicit -> `BomItem.
default_component_variant` -> the component Product's single variant."""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductionOrderComponent(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    production_order = models.ForeignKey("ProductionOrder",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Production Order"),
                                         related_name="components")
    bom_item = models.ForeignKey("products.BomItem",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("BOM Item"),
                                 related_name="production_order_components")
    product = models.ForeignKey("products.Product",
                                on_delete=models.PROTECT,
                                verbose_name=_("Component Product"),
                                related_name="production_order_components")
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Component Product Variant"),
                                related_name="production_order_components")
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="production_order_components",
                              null=True,
                              blank=True)
    planned_qty = models.DecimalField(verbose_name=_("Planned Quantity"),
                                      max_digits=18,
                                      decimal_places=4,
                                      validators=[MinValueValidator(Decimal("0"))])
    actual_qty = models.DecimalField(verbose_name=_("Actual Quantity"),
                                     max_digits=18,
                                     decimal_places=4,
                                     default=Decimal("0"),
                                     validators=[MinValueValidator(Decimal("0"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"))
    reservation = models.ForeignKey("StockReservation",
                                    on_delete=models.SET_NULL,
                                    verbose_name=_("Stock Reservation"),
                                    related_name="production_order_components",
                                    null=True,
                                    blank=True)

    def clean(self) -> None:
        super().clean()
        if self.variant_id is not None and self.product_id is not None:
            if self.variant.product_id != self.product_id:
                raise ValidationError(
                    _("ProductionOrderComponent.variant must belong to "
                      "ProductionOrderComponent.product.")
                )
        if self.batch_id is not None and self.variant_id is not None:
            if self.batch.variant_id != self.variant_id:
                raise ValidationError(
                    _("ProductionOrderComponent.batch must belong to the same ProductVariant.")
                )

    def __str__(self) -> str:
        return f"{self.production_order_id}: {self.variant_id} x {self.planned_qty}"

    class Meta:
        app_label = "stock"
        db_table = "stock_productionordercomponent"
        verbose_name = _("Production Order Component")
        verbose_name_plural = _("Production Order Components")
        ordering = ["production_order_id", "id"]
        indexes = [
            models.Index(fields=["workspace", "variant"], name="idx_prodordercomp_variant"),
        ]
