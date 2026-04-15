# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.contracts.models.sales_document import SalesDocument


class PurchaseConfirmation(SalesDocument):

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()

    def __str__(self):
        return _("Purchase Confirmation") + ": " + self.id.__str__() + " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_purchaseconfirmation"
        verbose_name = _('Purchase Confirmation')
        verbose_name_plural = _('Purchase Confirmations')
