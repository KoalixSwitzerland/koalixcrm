# -*- coding: utf-8 -*-
"""`HandlingUnit` — a physical container (pallet, carton, tray) with GS1
SSCC identification, an aggregation level over multiple `OnHandRecord`
rows (ADR-0009)."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import HandlingUnitType
from koalixcrm.stock.services.sscc import validate_sscc


class HandlingUnit(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    sscc = models.CharField(verbose_name=_("SSCC"), max_length=18)
    parent_handling_unit = models.ForeignKey("self",
                                             on_delete=models.SET_NULL,
                                             verbose_name=_("Parent Handling Unit"),
                                             related_name="child_handling_units",
                                             null=True,
                                             blank=True)
    location = models.ForeignKey("Location",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("Location"),
                                 related_name="handling_units")
    hu_type = models.CharField(verbose_name=_("Handling Unit Type"),
                              max_length=16,
                              choices=HandlingUnitType.choices)
    is_open = models.BooleanField(verbose_name=_("Is Open"), default=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        validate_sscc(self.sscc)
        if self.location_id is not None and self.location.workspace_id != self.workspace_id:
            raise ValidationError(
                _("A HandlingUnit's Location must belong to the same workspace.")
            )
        if self.parent_handling_unit_id is not None:
            if self.parent_handling_unit.workspace_id != self.workspace_id:
                raise ValidationError(
                    _("A HandlingUnit's parent must belong to the same workspace.")
                )
            if self.pk is not None and self.parent_handling_unit_id == self.pk:
                raise ValidationError(_("A HandlingUnit cannot be its own parent."))

    def __str__(self) -> str:
        return self.sscc

    class Meta:
        app_label = "stock"
        db_table = "stock_handlingunit"
        verbose_name = _("Handling Unit")
        verbose_name_plural = _("Handling Units")
        ordering = ["sscc"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "sscc"],
                name="uniq_handlingunit_sscc_per_workspace",
            ),
        ]
