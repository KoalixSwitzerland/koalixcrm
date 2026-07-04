# -*- coding: utf-8 -*-
"""`RetentionPolicy` — the workspace-wide configurable retention floor for
decommissioned `SerialUnit` rows (ADR-0012). Default retention is
"forever" (`serial_unit_retention_floor_days = null`); the floor is an
additive protective lower bound on manual deletion, never an automatic
deletion trigger."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class RetentionPolicy(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    serial_unit_retention_floor_days = models.PositiveIntegerField(
        verbose_name=_("SerialUnit Retention Floor (days)"),
        null=True,
        blank=True,
        help_text=_("Minimum number of days a decommissioned SerialUnit must be retained "
                    "before deletion may be attempted. Null = no configured floor beyond "
                    "the mandatory decommissioning requirement (ADR-0012 default: forever)."),
    )
    stock_movement_retention_floor_days = models.PositiveIntegerField(
        verbose_name=_("StockMovement Retention Floor (days)"),
        null=True,
        blank=True,
        help_text=_("Minimum number of days a StockMovement row must be retained (counted "
                    "from occurred_at) before deletion may be attempted. Null = no "
                    "configured floor; default retention is forever (ADR-0011). This is an "
                    "additive protective lower bound, never an automatic deletion trigger."),
    )

    def __str__(self) -> str:
        return f"RetentionPolicy({self.workspace_id})"

    class Meta:
        app_label = "stock"
        db_table = "stock_retentionpolicy"
        verbose_name = _("Retention Policy")
        verbose_name_plural = _("Retention Policies")
        constraints = [
            models.UniqueConstraint(fields=["workspace"], name="uniq_retentionpolicy_per_workspace"),
        ]
