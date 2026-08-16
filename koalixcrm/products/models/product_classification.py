# -*- coding: utf-8 -*-
"""`ProductClassification` — M:N link between `Product` and
`ClassificationNode` (ADR-0004). Workspace-scoped: a product is hung under
multiple taxonomies (UNSPSC, eCl@ss, internal) at once, per tenant."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductClassification(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="classifications",
    )
    classification_node = models.ForeignKey(
        "ClassificationNode",
        on_delete=models.CASCADE,
        verbose_name=_("Classification Node"),
        related_name="product_classifications",
    )
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product_id} -> {self.classification_node_id}"

    class Meta:
        app_label = "products"
        db_table = "products_productclassification"
        verbose_name = _("Product Classification")
        verbose_name_plural = _("Product Classifications")
        ordering = ["product_id", "classification_node_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "classification_node"],
                name="unique_product_classification_node",
            )
        ]
