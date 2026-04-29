# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.core.const.status import *


class PaymentReminder(CommercialDocument):
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

    def create_from_reference(self, calling_model: models.Model) -> None:
        self.create_commercial_document(calling_model)
        self.status = 'C'
        self.iteration_number = 1
        cycle = self.party.default_billing_cycle
        self.payable_until = date.today() + timedelta(days=cycle.payment_reminder_time_to_payment)
        self.template_set = self.contract.get_template_set(self)
        self.save()
        self.attach_commercial_document_positions(calling_model)
        self.attach_text_paragraphs()
        self.staff = calling_model.staff

    def __str__(self) -> str:
        return _("Payment Reminder") + ": " + str(self.id) + \
               " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_paymentreminder"
        verbose_name = _('Payment Reminder')
        verbose_name_plural = _('Payment Reminders')
