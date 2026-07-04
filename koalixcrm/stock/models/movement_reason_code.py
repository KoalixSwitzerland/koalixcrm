# -*- coding: utf-8 -*-
"""`MovementReasonCode` — global lookup table for `StockMovement.reason_code`
(ADR-0011). Platform-wide stable codes shipped as a fixture; tenants can add
their own via the workspace-scoped `MovementReasonCodeExtension`."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _


class MovementReasonCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(verbose_name=_("Code"), max_length=100, unique=True)
    label_de = models.CharField(verbose_name=_("Label (DE)"), max_length=200)
    label_en = models.CharField(verbose_name=_("Label (EN)"), max_length=200)
    applies_to_business_steps = models.JSONField(
        verbose_name=_("Applies To Business Steps"),
        default=list,
        blank=True,
        help_text=_("List of business_step values this reason code is valid for; "
                    "empty list = valid for all business steps."),
    )

    def __str__(self) -> str:
        return f"{self.code} ({self.label_en})"

    class Meta:
        app_label = "stock"
        db_table = "stock_movementreasoncode"
        verbose_name = _("Movement Reason Code")
        verbose_name_plural = _("Movement Reason Codes")
        ordering = ["code"]
