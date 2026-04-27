# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.core.const.status import *


class DespatchAdvice(CommercialDocument):
    tracking_reference = models.CharField(verbose_name=_("Tracking Reference"), max_length=100, blank=True)
    status = models.CharField(max_length=1, choices=DESPATCHADVICESTATUS)

    def create_from_reference(self, calling_model):
        self.create_commercial_document(calling_model)
        self.status = "C"
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return (
            _("Despatch Advice")
            + ": "
            + self.id.__str__()
            + " "
            + _("from Contract")
            + ": "
            + self.contract.id.__str__()
        )

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_despatchadvice"
        verbose_name = _("Despatch Advice")
        verbose_name_plural = _("Despatch Advices")
