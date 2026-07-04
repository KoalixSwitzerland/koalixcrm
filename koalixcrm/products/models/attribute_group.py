# -*- coding: utf-8 -*-
"""`AttributeGroup` — thematic bundle of `AttributeDefinition` entries
(ADR-0004), e.g. "Nutritional values per 100g" or "Coating parameters".

Global for GLOBAL-scope attribute groups (fixture-shipped), workspace-scoped
for WORKSPACE-scope groups a tenant admin defines — hence `workspace` is
nullable here rather than inheriting `WorkspaceScopedModel` outright (see
`clean()` for the scope/workspace consistency invariant)."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import AttributeScope


class AttributeGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    workspace = models.ForeignKey(
        "core.Workspace",
        on_delete=models.CASCADE,
        verbose_name=_("Workspace"),
        related_name="+",
        null=True,
        blank=True,
    )
    scope = models.CharField(
        verbose_name=_("Scope"),
        max_length=32,
        choices=AttributeScope.choices,
        default=AttributeScope.WORKSPACE,
    )
    key = models.SlugField(verbose_name=_("Key"), max_length=100)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.scope == AttributeScope.GLOBAL and self.workspace_id is not None:
            raise ValidationError(_("A GLOBAL-scope attribute group must not carry a workspace."))
        if self.scope != AttributeScope.GLOBAL and self.workspace_id is None:
            raise ValidationError(_("A WORKSPACE-scope attribute group requires a workspace."))

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_attributegroup"
        verbose_name = _("Attribute Group")
        verbose_name_plural = _("Attribute Groups")
        ordering = ["key"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "key"],
                condition=Q(workspace__isnull=False),
                name="unique_attribute_group_key_per_workspace",
            ),
            models.UniqueConstraint(
                fields=["key"],
                condition=Q(workspace__isnull=True),
                name="unique_attribute_group_key_global",
            ),
        ]
