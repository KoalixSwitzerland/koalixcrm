# -*- coding: utf-8 -*-
"""`BomItem` — a single BOM component line (ADR-0006, REQ-0015). Carries
quantity, unit, scrap percentage and an optional alternative component,
plus an optional, non-binding `default_component_variant` suggestion
(ADR-0006 Nachtrag 2026-07-04 / ADR-0021 OQ-0019). The binding component-
variant resolution happens at the booking point (ADR-0011/ADR-0014), not
here."""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class BomItem(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    bill_of_materials = models.ForeignKey("BillOfMaterials",
                                          on_delete=models.CASCADE,
                                          verbose_name=_("Bill of Materials"),
                                          related_name="items")
    component_product = models.ForeignKey("Product",
                                          on_delete=models.PROTECT,
                                          verbose_name=_("Component Product"),
                                          related_name="used_in_bom_items")
    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   max_digits=17,
                                   decimal_places=4,
                                   validators=[MinValueValidator(Decimal("0.0001"))])
    unit = models.ForeignKey("core.Unit",
                             on_delete=models.CASCADE,
                             verbose_name=_("Unit"))
    scrap_pct = models.DecimalField(verbose_name=_("Scrap Percentage"),
                                    max_digits=5,
                                    decimal_places=2,
                                    null=True,
                                    blank=True,
                                    validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))])
    alternative_component = models.ForeignKey("Product",
                                              on_delete=models.SET_NULL,
                                              verbose_name=_("Alternative Component"),
                                              related_name="alternative_in_bom_items",
                                              null=True,
                                              blank=True)
    default_component_variant = models.ForeignKey("ProductVariant",
                                                   on_delete=models.SET_NULL,
                                                   verbose_name=_("Default Component Variant"),
                                                   related_name="default_in_bom_items",
                                                   null=True,
                                                   blank=True,
                                                   help_text=_(
                                                       "Non-binding suggestion for the picking/reservation "
                                                       "form; must be a variant of `component_product`."
                                                   ))
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.bill_of_materials_id is not None and self.component_product_id is not None:
            if self.bill_of_materials.product_id == self.component_product_id:
                raise ValidationError(
                    _("A BomItem's component product may not be the same as the parent BOM's product.")
                )
        if self.default_component_variant_id is not None and self.component_product_id is not None:
            if self.default_component_variant.product_id != self.component_product_id:
                raise ValidationError(
                    _("default_component_variant must be a variant of component_product.")
                )

    def __str__(self) -> str:
        return f"{self.bill_of_materials_id}: {self.component_product} x {self.quantity}"

    class Meta:
        app_label = "products"
        db_table = "products_bomitem"
        verbose_name = _("BOM Item")
        verbose_name_plural = _("BOM Items")
        ordering = ["bill_of_materials_id", "id"]
