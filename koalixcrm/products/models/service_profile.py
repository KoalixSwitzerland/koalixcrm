# -*- coding: utf-8 -*-
"""`ServiceProfile` — 1:1 extension of `Product` for `kind = SERVICE`
(ADR-0007, REQ-0016). Gated via `ProductKindPolicy` (ADR-0019)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.choices import ServiceBillingModel
from koalixcrm.products.services.product_kind_policy import check_gate


class ServiceProfile(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField("Product",
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Product"),
                                   related_name="service_profile")
    billing_model = models.CharField(verbose_name=_("Billing Model"),
                                     max_length=32,
                                     choices=ServiceBillingModel.choices)
    default_duration = models.PositiveIntegerField(verbose_name=_("Default Duration (minutes)"),
                                                    null=True,
                                                    blank=True)
    deliverable = models.TextField(verbose_name=_("Deliverable"))
    sla_reference = models.CharField(verbose_name=_("SLA Reference"),
                                     max_length=500,
                                     null=True,
                                     blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.product_id is not None:
            check_gate("ServiceProfile", self.product.kind)

    def __str__(self) -> str:
        return f"ServiceProfile for {self.product}"

    class Meta:
        app_label = "products"
        db_table = "products_serviceprofile"
        verbose_name = _("Service Profile")
        verbose_name_plural = _("Service Profiles")
        ordering = ["product_id"]
