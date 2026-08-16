# -*- coding: utf-8 -*-
"""`ProductFamily` — optional grouping of `Product` objects (ADR-0021).

Correction 1 of ADR-0003 Amendment 2026-06-28: `ProductFamily` groups
`Product` objects, not `ProductVariant` objects. A `Product` belongs to at
most one `ProductFamily`; a `Product` without a `ProductFamily` is valid.
`ProductFamily` is also an additional `AttributeSet` binding axis
(ADR-0004/ADR-0021), not yet implemented in this stage.
"""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductFamily(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_productfamily"
        verbose_name = _("Product Family")
        verbose_name_plural = _("Product Families")
        ordering = ["name"]
