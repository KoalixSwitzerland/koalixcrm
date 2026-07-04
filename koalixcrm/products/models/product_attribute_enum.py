# -*- coding: utf-8 -*-
"""`ProductAttributeEnum` — typed EAV value table for `enum` attributes
(ADR-0004). `value` must be one of `attribute_definition.enum_values`;
enforced in `clean()`."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeEnum(ProductAttributeValueBase):
    value = models.CharField(verbose_name=_("Value"), max_length=200)

    def clean(self) -> None:
        super().clean()
        allowed = self.attribute_definition.enum_values or []
        if allowed and self.value not in allowed:
            raise ValidationError(
                {"value": _("%(value)s is not one of the allowed enum values %(allowed)s.") % {
                    "value": self.value, "allowed": allowed,
                }}
            )

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.value}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributeenum"
        verbose_name = _("Product Attribute (Enum)")
        verbose_name_plural = _("Product Attributes (Enum)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_enum_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_enum_pvad",
            )
        ]
