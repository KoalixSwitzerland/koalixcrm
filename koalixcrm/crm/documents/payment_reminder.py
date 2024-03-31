# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.const.status import *
from django.core.validators import MaxValueValidator, MinValueValidator
from koalixcrm.crm.documents.sales_document import SalesDocument, OptionSalesDocument
from koalixcrm.plugin import *


class PaymentReminder(SalesDocument):
    payable_until = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"),
                                              max_length=100,
                                              blank=True,
                                              null=True)
    iteration_number = models.IntegerField(blank=False,
                                           null=False,
                                           verbose_name=_("Iteration Number"),
                                           validators=[MinValueValidator(1),
                                                       MaxValueValidator(3)])
    status = models.CharField(max_length=1,
                              choices=INVOICESTATUS)

    def create_from_reference(self, calling_model):
        self.create_sales_document(calling_model)
        self.status = 'C'
        self.iteration_number = 1
        self.payable_until = date.today() + \
                             timedelta(days=self.customer.default_customer_billing_cycle.payment_reminder_time_to_payment)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_sales_document_positions(calling_model)
        self.attach_text_paragraphs()
        self.staff = calling_model.staff

    def __str__(self):
        return _("Payment Reminder") + ": " + self.id.__str__() + \
               " " + _("from Contract") + ": " + self.contract.id.__str__()

    class Meta:
        app_label = "crm"
        verbose_name = _('Payment Reminder')
        verbose_name_plural = _('Payment Reminders')


class OptionPaymentReminder(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('payable_until',
                                                       'status',
                                                       'iteration_number')
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Quote specific'), {
            'fields': ('payable_until',
                       'status',
                       'payment_bank_reference',
                       'iteration_number')
        }),
    )

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines
    actions = ['create_purchase_confirmation',
               'create_invoice',
               'create_quote',
               'create_delivery_note',
               'create_pdf',
               'register_invoice_in_accounting',
               'register_payment_in_accounting']

    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("quoteInlines"))
