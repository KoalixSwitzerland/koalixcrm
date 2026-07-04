# -*- coding: utf-8 -*-
"""`ProductVariant` — the sellable SKU (ADR-0003, ADR-0021).

ADR-0021 Korrektur 2 / 3-Ebenen-Topologie: `ProductVariant` carries a FK to
`Product` (not to `ProductFamily`). Every `Product` has >= 1
`ProductVariant`. All trade- and logistics-specific identifiers and
physical properties live here per the ADR-0021 keying table: `sku`,
`gtin`, `mpn`, `weight_kg`, `dimensions_*`.

`axis_values` is a placeholder JSON store for variant-axis attribute
values (e.g. color x size) until ADR-0004's typed EAV value tables (Option
A, nullable `variant_id`) are implemented; it is not itself an EAV table.
"""
from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.choices import TrackingMode
from koalixcrm.products.services.product_kind_policy import check_tracking_mode


class ProductVariant(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name="variants")
    sku = models.CharField(verbose_name=_("SKU"), max_length=200)
    gtin = models.CharField(verbose_name=_("GTIN"), max_length=14, null=True, blank=True)
    mpn = models.CharField(verbose_name=_("Manufacturer Part Number"), max_length=200, null=True, blank=True)
    weight_kg = models.DecimalField(verbose_name=_("Weight (kg)"),
                                    max_digits=12,
                                    decimal_places=4,
                                    null=True,
                                    blank=True,
                                    validators=[MinValueValidator(0)])
    dimensions_length_m = models.DecimalField(verbose_name=_("Length (m)"),
                                              max_digits=12,
                                              decimal_places=4,
                                              null=True,
                                              blank=True,
                                              validators=[MinValueValidator(0)])
    dimensions_width_m = models.DecimalField(verbose_name=_("Width (m)"),
                                             max_digits=12,
                                             decimal_places=4,
                                             null=True,
                                             blank=True,
                                             validators=[MinValueValidator(0)])
    dimensions_height_m = models.DecimalField(verbose_name=_("Height (m)"),
                                              max_digits=12,
                                              decimal_places=4,
                                              null=True,
                                              blank=True,
                                              validators=[MinValueValidator(0)])
    axis_values = models.JSONField(verbose_name=_("Variant Axis Values"), default=dict, blank=True)
    tracking_mode = models.CharField(verbose_name=_("Tracking Mode"),
                                     max_length=16,
                                     choices=TrackingMode.choices,
                                     default=TrackingMode.NONE,
                                     help_text=_("ADR-0009/ADR-0012/ADR-0021: NONE, BATCH "
                                                 "(requires stock.Batch) or SERIAL (requires "
                                                 "stock.SerialUnit)."))
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        # ADR-0019: tracking_mode must be NONE for kind = SERVICE.
        check_tracking_mode(self.product.kind, self.tracking_mode)

    def __str__(self) -> str:
        return self.sku

    class Meta:
        app_label = "products"
        db_table = "products_productvariant"
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        ordering = ["sku"]
