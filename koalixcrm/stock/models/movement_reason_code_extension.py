# -*- coding: utf-8 -*-
"""`MovementReasonCodeExtension` — workspace-scoped tenant extension of the
global `MovementReasonCode` lookup table (ADR-0011 Workspace-Scoping-
Matrix)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class MovementReasonCodeExtension(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(verbose_name=_("Code"), max_length=100)
    label_de = models.CharField(verbose_name=_("Label (DE)"), max_length=200)
    label_en = models.CharField(verbose_name=_("Label (EN)"), max_length=200)
    applies_to_business_steps = models.JSONField(
        verbose_name=_("Applies To Business Steps"),
        default=list,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.code} ({self.label_en})"

    class Meta:
        app_label = "stock"
        db_table = "stock_movementreasoncodeextension"
        verbose_name = _("Movement Reason Code Extension")
        verbose_name_plural = _("Movement Reason Code Extensions")
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "code"],
                name="uniq_movementreasoncodeext_per_workspace",
            ),
        ]
