# -*- coding: utf-8 -*-
"""`ProductAttributeMirror` — denormalized JSON read-mirror per
(product, variant) (ADR-0004). Supports read-heavy search/listing paths
without joining the six typed EAV tables. Maintained synchronously by
`post_save`/`post_delete` signals on the typed value tables (see
`koalixcrm.products.signals.attribute_mirror`) calling
`koalixcrm.products.services.attribute_mirror.rebuild_attribute_mirror`.

Uses `JSONField` (not Postgres-specific `JSONB`) so the mirror works
identically on sqlite (dev/test) and Postgres (ADR-0004 §Getypte
Wertetabellen: "optionaler denormalisierter JSONB-Spiegel")."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductAttributeMirror(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="attribute_mirrors",
    )
    variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        verbose_name=_("Variant"),
        related_name="attribute_mirrors",
        null=True,
        blank=True,
    )
    data = models.JSONField(verbose_name=_("Data"), default=dict, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)

    def __str__(self) -> str:
        return f"mirror({self.product_id}, {self.variant_id})"

    class Meta:
        app_label = "products"
        db_table = "products_productattributemirror"
        verbose_name = _("Product Attribute Mirror")
        verbose_name_plural = _("Product Attribute Mirrors")
        ordering = ["product_id", "variant_id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "variant"], name="unique_attribute_mirror_pv"),
        ]
