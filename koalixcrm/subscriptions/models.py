# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.utils.translation import gettext as _
from filebrowser.fields import FileBrowseField
from koalixcrm.subscriptions.const.events import *
import koalixcrm.crm.documents


class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey('crm.Contract', on_delete=models.CASCADE, verbose_name=_('Subscription Type'))
    subscription_type = models.ForeignKey('SubscriptionType', on_delete=models.CASCADE, verbose_name=_('Subscription Type'), null=True)

    def create_subscription_from_contract(self, contract):
        self.contract = contract
        self.save()
        return self

    def create_quote(self):
        quote = koalixcrm.crm.documents.quote.Quote()
        quote.contract = self.contract
        quote.discount = 0
        quote.staff = self.contract.staff
        quote.customer = self.contract.defaultcustomer
        quote.status = 'C'
        quote.currency = self.contract.defaultcurrency
        quote.valid_until = date.today().__str__()
        quote.date_of_creation = date.today().__str__()
        quote.save()
        return quote

    def create_invoice(self):
        invoice = koalixcrm.crm.documents.invoice.Invoice()
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


class SubscriptionEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscriptions = models.ForeignKey('Subscription',
                                      on_delete=models.CASCADE,
                                      verbose_name=_('Subscription'))
    event_date = models.DateField(verbose_name=_("Event Date"),
                                  blank=True, null=True)
    event = models.CharField(max_length=1, choices=SUBSCRITIONEVENTS,
                             verbose_name=_('Event'))

    def __str__(self):
        return self.event

    class Meta:
        app_label = "subscriptions"
        verbose_name = _('Subscription Event')
        verbose_name_plural = _('Subscription Events')


class SubscriptionType(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_type = models.ForeignKey('crm.ProductType',
                                     verbose_name=_('Product Type'),
                                     on_delete=models.deletion.SET_NULL,
                                     null=True,
                                     blank=True)
    cancellation_period = models.IntegerField(verbose_name=_("Cancellation Period (months)"),
                                              blank=True,
                                              null=True)
    automatic_contract_extension = models.IntegerField(verbose_name=_("Automatic Contract Extension (months)"),
                                                       blank=True,
                                                       null=True)
    automatic_contract_extension_reminder = models.IntegerField(
        verbose_name=_("Automatic Contract Extension Reminder (days)"),
        blank=True,
        null=True)
    minimum_duration = models.IntegerField(verbose_name=_("Minimum Contract Duration"),
                                           blank=True,
                                           null=True)
    payment_interval = models.IntegerField(verbose_name=_("Payment Interval (days)"),
                                           blank=True,
                                           null=True)
    contract_document = FileBrowseField(verbose_name=_("Contract Documents"),
                                        blank=True,
                                        null=True,
                                        max_length=200)

    class Meta:
        app_label = "subscriptions"
        verbose_name = _('Subscription Type')
        verbose_name_plural = _('Subscription Types')
