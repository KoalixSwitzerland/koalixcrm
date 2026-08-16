# -*- coding: utf-8 -*-
"""`AttributeSet` — binds `AttributeGroup` entries to a `ClassificationNode`,
a `kind` value, and/or a `ProductFamily` (ADR-0004, ADR-0021 Amendment
2026-06-28). Every product classified under (or of that kind, or in that
family) inherits the set's fields, required flags, and validation rules
without a code change. Workspace-scoped per the ADR-0004 matrix."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.choices import ProductKind


class AttributeSet(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    classification_node = models.ForeignKey(
        "ClassificationNode",
        on_delete=models.CASCADE,
        verbose_name=_("Classification Node"),
        related_name="attribute_sets",
        null=True,
        blank=True,
    )
    kind = models.CharField(
        verbose_name=_("Kind"),
        max_length=32,
        choices=ProductKind.choices,
        null=True,
        blank=True,
    )
    product_family = models.ForeignKey(
        "ProductFamily",
        on_delete=models.CASCADE,
        verbose_name=_("Product Family"),
        related_name="attribute_sets",
        null=True,
        blank=True,
    )
    attribute_groups = models.ManyToManyField(
        "AttributeGroup",
        through="AttributeSetGroup",
        related_name="attribute_sets",
        verbose_name=_("Attribute Groups"),
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_attributeset"
        verbose_name = _("Attribute Set")
        verbose_name_plural = _("Attribute Sets")
        ordering = ["name"]


class AttributeSetGroup(models.Model):
    """Through table ordering `AttributeGroup` entries within an
    `AttributeSet`."""

    id = models.BigAutoField(primary_key=True)
    attribute_set = models.ForeignKey(AttributeSet, on_delete=models.CASCADE, related_name="set_groups")
    attribute_group = models.ForeignKey("AttributeGroup", on_delete=models.CASCADE, related_name="set_groups")
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)

    def __str__(self) -> str:
        return f"{self.attribute_set_id}:{self.attribute_group_id}"

    class Meta:
        app_label = "products"
        db_table = "products_attributesetgroup"
        verbose_name = _("Attribute Set Group")
        verbose_name_plural = _("Attribute Set Groups")
        ordering = ["attribute_set", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["attribute_set", "attribute_group"],
                name="unique_attribute_set_group",
            )
        ]
