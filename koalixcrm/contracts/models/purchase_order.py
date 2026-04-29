# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.core.const.status import *


class PurchaseOrder(CommercialDocument):
    # Supplier is the inherited CommercialDocument.party. The legacy
    # PurchaseOrder.supplier FK was dropped in #395 G3.
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)

    def create_from_reference(self, calling_model: models.Model) -> None:
        self.create_commercial_document(calling_model)
        self.status = "O"
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()
        self.staff = calling_model.staff

    def __str__(self) -> str:
        return (
            _("Purchase Order")
            + ": "
            + str(self.id)
            + " "
            + _("from Contract")
            + ": "
            + str(self.contract.id)
        )

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_purchaseorder"
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")
