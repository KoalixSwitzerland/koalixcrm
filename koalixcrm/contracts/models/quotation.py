# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.html import format_html
from koalixcrm.core.const.status import *
from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.global_support_functions import limit_string_length


class Quotation(CommercialDocument):
    valid_until = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTATIONSTATUS, verbose_name=_('Status'))

    def link_to_quotation(self):
        if self.id:
            return format_html("<a href='/admin/contract_object_management/quotation/%s' >%s</a>" % (str(self.id),
                                                                          limit_string_length(str(self.description),
                                                                                              30)))
        else:
            return "Not present"
    link_to_quotation.short_description = _("Quotation");

    def create_from_reference(self, calling_model):
        self.create_commercial_document(calling_model)
        self.status = 'I'
        self.valid_until = date.today().__str__()
        self.date_of_creation = date.today().__str__()
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Quotation") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_quotation"
        verbose_name = _('Quotation')
        verbose_name_plural = _('Quotations')
