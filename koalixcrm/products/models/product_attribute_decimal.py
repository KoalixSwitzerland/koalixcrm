# -*- coding: utf-8 -*-
"""`ProductAttributeDecimal` — typed EAV value table for `decimal` (and
`measure`, decimal + unit) attributes (ADR-0004)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeDecimal(ProductAttributeValueBase):
    value = models.DecimalField(verbose_name=_("Value"), max_digits=20, decimal_places=6)
    unit = models.ForeignKey(
        "core.Unit",
        on_delete=models.SET_NULL,
        verbose_name=_("Unit"),
        related_name="+",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.value}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributedecimal"
        verbose_name = _("Product Attribute (Decimal)")
        verbose_name_plural = _("Product Attributes (Decimal)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_decimal_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_decimal_pvad",
            )
        ]
