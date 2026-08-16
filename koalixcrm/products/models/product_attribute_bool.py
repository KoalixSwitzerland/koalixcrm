# -*- coding: utf-8 -*-
"""`ProductAttributeBool` — typed EAV value table for `bool` attributes
(ADR-0004)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeBool(ProductAttributeValueBase):
    value = models.BooleanField(verbose_name=_("Value"))

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.value}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributebool"
        verbose_name = _("Product Attribute (Bool)")
        verbose_name_plural = _("Product Attributes (Bool)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_bool_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_bool_pvad",
            )
        ]
