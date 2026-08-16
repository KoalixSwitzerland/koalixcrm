# -*- coding: utf-8 -*-
"""`ProductPassport` — JSONB placeholder for EU Digital Product Passport
metadata (ADR-0008). 1:1 with `Product`; kind-agnostic (ADR-0019 Gating-
Matrix — allowed for every `kind`). `passport_data` is reserved for
unstructured regulatory metadata with no structured home elsewhere;
structured DPP fields will be a future projection over the event log
(ADR-0011) and product master data (ADR-0003/ADR-0004), not stored here."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductPassport(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Product"),
                                   related_name="passport")
    passport_data = models.JSONField(verbose_name=_("Passport Data"), default=dict, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return f"ProductPassport for {self.product}"

    class Meta:
        app_label = "products"
        db_table = "products_productpassport"
        verbose_name = _("Product Passport")
        verbose_name_plural = _("Product Passports")
        ordering = ["product_id"]
