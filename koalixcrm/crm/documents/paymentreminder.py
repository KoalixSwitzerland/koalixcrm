# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm.crm.documents.salescontract import SalesContract
from django.core.validators import MaxValueValidator, MinValueValidator
import koalixcrm.crm.documents.pdfexport


class PaymentReminder(SalesContract):
    derived_from_invoice = models.ForeignKey("Invoice", blank=True, null=True)
    iteration_number = models.IntegerField(blank=False, null=False, verbose_name=_("Iteration Number"),
                                           validators=[MinValueValidator(1), MaxValueValidator(3)])
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def create_pdf(self):
        self.last_print_date = datetime.now()
        self.save()
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self)

    def __str__(self):
        return _("Payment Reminder") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Payment Reminder')
        verbose_name_plural = _('Payment Reminders')