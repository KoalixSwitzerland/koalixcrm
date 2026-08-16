# -*- coding: utf-8 -*-
"""`ProductAttributeInt` — typed EAV value table for `int` attributes
(ADR-0004)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeInt(ProductAttributeValueBase):
    value = models.BigIntegerField(verbose_name=_("Value"))

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.value}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributeint"
        verbose_name = _("Product Attribute (Int)")
        verbose_name_plural = _("Product Attributes (Int)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_int_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_int_pvad",
            )
        ]
