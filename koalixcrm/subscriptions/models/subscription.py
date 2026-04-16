# -*- coding: utf-8 -*-
from datetime import *
from django.db import models
from django.utils.translation import gettext as _
import koalixcrm.core.documents


class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey('contract_object_management.Contract', on_delete=models.CASCADE, verbose_name=_('Subscription Type'))
    subscription_type = models.ForeignKey('SubscriptionType', on_delete=models.CASCADE, verbose_name=_('Subscription Type'), null=True)

    def create_subscription_from_contract(self, contract):
        self.contract = contract
        self.save()
        return self

    def create_quotation(self):
        quotation = koalixcrm.core.documents.quotation.Quotation()
        quotation.contract = self.contract
        quotation.discount = 0
        quotation.staff = self.contract.staff
        quotation.customer = self.contract.defaultcustomer
        quotation.status = 'C'
        quotation.currency = self.contract.defaultcurrency
        quotation.valid_until = date.today().__str__()
        quotation.date_of_creation = date.today().__str__()
        quotation.save()
        return quotation

    def create_invoice(self):
        invoice = koalixcrm.core.documents.invoice.Invoice()
        invoice.contract = self.contract
        invoice.discount = 0
        invoice.staff = self.contract.staff
        invoice.customer = self.contract.default_customer
        invoice.status = 'C'
        invoice.currency = self.contract.default_currency
        invoice.payable_until = date.today() + timedelta(
            days=self.contract.defaultcustomer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.date_of_creation = date.today().__str__()
        invoice.save()
        return invoice

    class Meta:
        app_label = "subscriptions"
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
