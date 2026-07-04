# -*- coding: utf-8 -*-
"""`ProductAttributeString` — typed EAV value table for `string` attributes
(ADR-0004)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeString(ProductAttributeValueBase):
    value = models.TextField(verbose_name=_("Value"))

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.value!r}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributestring"
        verbose_name = _("Product Attribute (String)")
        verbose_name_plural = _("Product Attributes (String)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_string_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_string_pvad",
            )
        ]
