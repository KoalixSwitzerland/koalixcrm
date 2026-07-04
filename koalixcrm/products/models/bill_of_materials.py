# -*- coding: utf-8 -*-
"""`BillOfMaterials` — ISA-95 Part 2 bill of materials, 1:1 with `Product`
(ADR-0006, REQ-0015). Gated to `kind in {MANUFACTURED_GOOD, KIT}` via
`ProductKindPolicy` (ADR-0019); `BillOfMaterials` stays `Product`-keyed
(ADR-0021 Nachtrag 2026-07-04) — component variant resolution happens at
the booking point, not in the BOM definition."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_kind_policy import check_gate


class BillOfMaterials(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Product"),
                                   related_name="bill_of_materials")
    name = models.CharField(verbose_name=_("Name"), max_length=200, null=True, blank=True)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    version = models.PositiveIntegerField(
        verbose_name=_("Version"),
        default=1,
        help_text=_("ADR-0014: bumped whenever a BomItem of this BOM is created, changed or "
                    "removed; the BOM-explosion snapshot pins the version it was computed "
                    "against so the pick-time path can detect staleness."),
    )
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.product_id is not None:
            check_gate("BillOfMaterials", self.product.kind)

    def __str__(self) -> str:
        return f"BOM for {self.product}"

    class Meta:
        app_label = "products"
        db_table = "products_billofmaterials"
        verbose_name = _("Bill of Materials")
        verbose_name_plural = _("Bills of Materials")
        ordering = ["product_id"]
