# -*- coding: utf-8 -*-
"""`ProductAttributeMapping` — ADR-0018 Layer-3 adapter seam. Maps a
classification standard's native attribute identifier (e.g. an eCl@ss IRDI)
to a canonical `koalix.*` key, data-driven, with no per-standard code.
KoalixCRM ships no licensed eCl@ss/ETIM content; operators import their own
mappings under their own license. Workspace-scoped: an operator's mapping
configuration is tenant data."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductAttributeMapping(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    source_standard = models.CharField(
        verbose_name=_("Source Standard"),
        max_length=50,
        help_text=_("e.g. eclass, gpc, etim, unspsc"),
    )
    source_attribute_id = models.CharField(
        verbose_name=_("Source Attribute Id"),
        max_length=200,
        help_text=_("Native attribute identifier of the source standard, e.g. an eCl@ss IRDI."),
    )
    canonical_key = models.CharField(
        verbose_name=_("Canonical Key"),
        max_length=100,
        help_text=_("ADR-0018 koalix.* canonical vocabulary key this source maps to."),
    )
    transform = models.JSONField(
        verbose_name=_("Transform"),
        null=True,
        blank=True,
        help_text=_("Optional data-driven unit conversion / value mapping formula."),
    )

    def __str__(self) -> str:
        return f"{self.source_standard}:{self.source_attribute_id} -> {self.canonical_key}"

    class Meta:
        app_label = "products"
        db_table = "products_productattributemapping"
        verbose_name = _("Product Attribute Mapping")
        verbose_name_plural = _("Product Attribute Mappings")
        ordering = ["source_standard", "source_attribute_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "source_standard", "source_attribute_id"],
                name="unique_product_attribute_mapping_source",
            )
        ]
