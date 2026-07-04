# -*- coding: utf-8 -*-
"""`AttributeDefinition` — Layer-2 EAV metadata (ADR-0004): data type, unit,
validation rules, scope. Global for GLOBAL-scope, workspace-scoped for
WORKSPACE-scope — see `AttributeGroup` docstring for why `workspace` is
nullable here rather than inheriting `WorkspaceScopedModel` outright.

`canonical_key` is the optional bridge into the ADR-0018 canonical
`koalix.*` vocabulary: when set, this attribute definition backs a
canonical key whose value lives in the EAV layer (as opposed to canonical
keys that read straight off a Layer-1 column, e.g. `koalix.weight_kg`)."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import AttributeDataType, AttributeScope


class AttributeDefinition(models.Model):
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
    canonical_key = models.CharField(
        verbose_name=_("Canonical Key"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("ADR-0018 koalix.* canonical vocabulary key this attribute backs, if any."),
    )
    label = models.CharField(verbose_name=_("Label"), max_length=200)
    data_type = models.CharField(verbose_name=_("Data Type"), max_length=16, choices=AttributeDataType.choices)
    unit = models.ForeignKey(
        "core.Unit",
        on_delete=models.SET_NULL,
        verbose_name=_("Unit"),
        related_name="+",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        "AttributeGroup",
        on_delete=models.SET_NULL,
        verbose_name=_("Attribute Group"),
        related_name="attribute_definitions",
        null=True,
        blank=True,
    )
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)
    min_value = models.DecimalField(verbose_name=_("Min Value"), max_digits=20, decimal_places=6, null=True, blank=True)
    max_value = models.DecimalField(verbose_name=_("Max Value"), max_digits=20, decimal_places=6, null=True, blank=True)
    regex = models.CharField(verbose_name=_("Regex"), max_length=500, null=True, blank=True)
    enum_values = models.JSONField(verbose_name=_("Enum Values"), default=list, blank=True)
    is_localized = models.BooleanField(verbose_name=_("Is Localized"), default=False)
    is_required = models.BooleanField(verbose_name=_("Is Required"), default=False)
    is_multivalued = models.BooleanField(verbose_name=_("Is Multivalued"), default=False)

    def clean(self) -> None:
        super().clean()
        if self.scope == AttributeScope.GLOBAL and self.workspace_id is not None:
            raise ValidationError(_("A GLOBAL-scope attribute definition must not carry a workspace."))
        if self.scope != AttributeScope.GLOBAL and self.workspace_id is None:
            raise ValidationError(_("A WORKSPACE-scope attribute definition requires a workspace."))
        if self.data_type == AttributeDataType.ENUM and not self.enum_values:
            raise ValidationError(_("An enum attribute definition requires at least one enum_values entry."))

    def __str__(self) -> str:
        return self.label

    class Meta:
        app_label = "products"
        db_table = "products_attributedefinition"
        verbose_name = _("Attribute Definition")
        verbose_name_plural = _("Attribute Definitions")
        ordering = ["key"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "key"],
                condition=Q(workspace__isnull=False),
                name="unique_attribute_definition_key_per_workspace",
            ),
            models.UniqueConstraint(
                fields=["key"],
                condition=Q(workspace__isnull=True),
                name="unique_attribute_definition_key_global",
            ),
        ]
