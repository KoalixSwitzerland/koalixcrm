# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument


class SalesOrder(CommercialDocument):

    def create_from_reference(self, calling_model):
        self.create_commercial_document(calling_model)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Sales Order") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_salesorder"
        verbose_name = _('Sales Order')
        verbose_name_plural = _('Sales Orders')
