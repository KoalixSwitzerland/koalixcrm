# -*- coding: utf-8 -*-
"""`ProductTranslation` — multi-language name/description for `Product`
(ADR-0003). See `koalixcrm.products.services.product_translation_resolver`
for the 3-step read-time fallback chain."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductTranslation(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name="translations")
    language_code = models.CharField(verbose_name=_("Language Code"), max_length=10)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    short_description = models.CharField(verbose_name=_("Short Description"),
                                         max_length=500,
                                         null=True,
                                         blank=True)
    long_description = models.TextField(verbose_name=_("Long Description"), null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product_id} [{self.language_code}] {self.name}"

    class Meta:
        app_label = "products"
        db_table = "products_producttranslation"
        verbose_name = _("Product Translation")
        verbose_name_plural = _("Product Translations")
        ordering = ["language_code"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "language_code"],
                name="unique_product_translation_per_language",
            )
        ]
