# -*- coding: utf-8 -*-
"""`ProductAttributeReference` — typed EAV value table for `reference`
attributes (ADR-0004): a value that is itself a FK into an arbitrary
lookup entity (e.g. `RalColor(code, name, hex)`). Implemented via Django's
generic-relations framework (`ContentType` + `object_id`) rather than a
per-lookup-entity FK, so the value table stays generic across operator-
defined lookup entities without a schema migration per entity."""
from __future__ import annotations

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.attribute_value_base import ProductAttributeValueBase


class ProductAttributeReference(ProductAttributeValueBase):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Lookup Entity Type"))
    object_id = models.PositiveBigIntegerField(verbose_name=_("Lookup Entity Id"))
    value = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.attribute_definition_id}={self.content_type_id}:{self.object_id}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributereference"
        verbose_name = _("Product Attribute (Reference)")
        verbose_name_plural = _("Product Attributes (Reference)")
        indexes = [
            models.Index(fields=["product", "variant", "attribute_definition"], name="pa_reference_pvad_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "variant", "attribute_definition"],
                name="unique_pa_reference_pvad",
            )
        ]
