# -*- coding: utf-8 -*-
"""`AttributeSetDefault` — the cascade-stage-3 default value an
`AttributeSet` supplies for one of its bound `AttributeDefinition` entries
(ADR-0004/ADR-0021: Varianten-Override -> Produkt-Wert ->
Familie-/AttributeSet-Standard). Stored as a scalar JSON value; the cascade
resolver (`koalixcrm.products.services.attribute_cascade`) coerces it
against the attribute's `data_type` at read time."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class AttributeSetDefault(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    attribute_set = models.ForeignKey(
        "AttributeSet",
        on_delete=models.CASCADE,
        verbose_name=_("Attribute Set"),
        related_name="defaults",
    )
    attribute_definition = models.ForeignKey(
        "AttributeDefinition",
        on_delete=models.CASCADE,
        verbose_name=_("Attribute Definition"),
        related_name="set_defaults",
    )
    default_value = models.JSONField(verbose_name=_("Default Value"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.attribute_set_id}:{self.attribute_definition_id}={self.default_value!r}"

    class Meta:
        app_label = "products"
        db_table = "products_attributesetdefault"
        verbose_name = _("Attribute Set Default")
        verbose_name_plural = _("Attribute Set Defaults")
        ordering = ["attribute_set_id", "attribute_definition_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["attribute_set", "attribute_definition"],
                name="unique_attribute_set_default",
            )
        ]
