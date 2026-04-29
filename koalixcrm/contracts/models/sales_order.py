# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument


class SalesOrder(CommercialDocument):
    def create_from_reference(self, calling_model: models.Model) -> None:
        self.create_commercial_document(calling_model)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self) -> str:
        return (
            _("Sales Order") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)
        )

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_salesorder"
        verbose_name = _("Sales Order")
        verbose_name_plural = _("Sales Orders")
