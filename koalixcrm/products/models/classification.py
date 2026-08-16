# -*- coding: utf-8 -*-
"""`Classification` / `ClassificationNode` — global taxonomy trees (ADR-0004).

Both models are global lookup/master data (not `WorkspaceScopedModel`) per
the ADR-0004 Workspace-Scoping-Matrix: classification schemes and their
nodes are shared across all tenants. UNSPSC may ship as an open-source
fixture; eCl@ss/ETIM content is licensed and must never be bundled (see
ADR-0004 Lizenzbeschränkung) — only the schema exists here, operators
import licensed content themselves.
"""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _


class Classification(models.Model):
    """A classification scheme: UNSPSC, eCl@ss, an internal scheme, etc."""

    id = models.BigAutoField(primary_key=True)
    code = models.SlugField(verbose_name=_("Code"), max_length=50, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_classification"
        verbose_name = _("Classification")
        verbose_name_plural = _("Classifications")
        ordering = ["code"]


class ClassificationNode(models.Model):
    """A node in the hierarchical tree of a `Classification` scheme (e.g.
    UNSPSC Segment -> Family -> Class -> Commodity)."""

    id = models.BigAutoField(primary_key=True)
    classification = models.ForeignKey(
        Classification,
        on_delete=models.CASCADE,
        verbose_name=_("Classification"),
        related_name="nodes",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("Parent Node"),
        related_name="children",
        null=True,
        blank=True,
    )
    code = models.CharField(verbose_name=_("Code"), max_length=100)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    level = models.PositiveSmallIntegerField(verbose_name=_("Level"), default=0)

    def __str__(self) -> str:
        return f"{self.classification.code}:{self.code} {self.name}"

    class Meta:
        app_label = "products"
        db_table = "products_classificationnode"
        verbose_name = _("Classification Node")
        verbose_name_plural = _("Classification Nodes")
        ordering = ["classification", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["classification", "code"],
                name="unique_classification_node_code",
            )
        ]
