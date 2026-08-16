# -*- coding: utf-8 -*-
"""`Location` — a node in the n-level stock location hierarchy (ADR-0009,
REQ-0018). A single recursive self-FK (`parent`) supports arbitrary depth
(Warehouse -> Zone -> Aisle -> Rack -> Shelf -> Layer -> Bin) without a
schema change. `external_ref` is the GLN/AS-RS-address/barcode-text
resolution target (ADR-0016 AI (414))."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import LocationType
from koalixcrm.stock.services.location_hierarchy import assert_no_cycle, get_ancestor_path


class Location(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    parent = models.ForeignKey("self",
                               on_delete=models.PROTECT,
                               verbose_name=_("Parent Location"),
                               related_name="children",
                               null=True,
                               blank=True)
    location_type = models.CharField(verbose_name=_("Location Type"),
                                     max_length=32,
                                     choices=LocationType.choices)
    code = models.CharField(verbose_name=_("Code"), max_length=100)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    external_ref = models.CharField(verbose_name=_("External Reference"),
                                    max_length=200,
                                    null=True,
                                    blank=True,
                                    help_text=_("Optional AS/RS address string or barcode plaintext "
                                                "(also the GLN AI (414) resolution target)."))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.parent_id is not None:
            if self.parent.workspace_id != self.workspace_id:
                raise ValidationError(
                    _("A Location's parent must belong to the same workspace.")
                )
            assert_no_cycle(self)

    def get_ancestor_path(self) -> list["Location"]:
        """Root -> self, via a single recursive-CTE query (REQ-0018 AC-2)."""
        return get_ancestor_path(self)

    def __str__(self) -> str:
        return f"{self.code} ({self.name})"

    class Meta:
        app_label = "stock"
        db_table = "stock_location"
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "code"],
                name="uniq_location_code_per_workspace",
            ),
            models.UniqueConstraint(
                fields=["workspace", "external_ref"],
                condition=Q(external_ref__isnull=False),
                name="uniq_location_external_ref_per_workspace",
            ),
        ]
