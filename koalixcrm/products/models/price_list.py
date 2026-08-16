# -*- coding: utf-8 -*-
"""`PriceList` — explicit channel/customer-segment grouping of `ProductPrice`
rows (ADR-0005, REQ-0012). A `ProductPrice` without a `PriceList` FK is the
workspace-wide default price (three-level price precedence, ADR-0005)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class PriceList(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    channel = models.CharField(verbose_name=_("Channel"),
                               max_length=100,
                               null=True,
                               blank=True,
                               help_text=_("Optional channel identifier (e.g. 'webshop', 'wholesale')."))
    party_group = models.ForeignKey("contacts.PartyGroup",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Customer Segment"),
                                    related_name="price_lists",
                                    null=True,
                                    blank=True,
                                    help_text=_("Optional customer segment this price list applies to."))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_pricelist"
        verbose_name = _("Price List")
        verbose_name_plural = _("Price Lists")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["workspace", "name"], name="pricelist_unique_name_per_workspace"),
        ]
