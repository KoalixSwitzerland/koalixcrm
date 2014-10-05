from datetime import *

from django.db import models
from filebrowser.fields import FileBrowseField

from const.events import *
from crm.models import Quote, Contract, Invoice, Product


class Subscription(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=trans('Subscription Type'))
    subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=trans('Subscription Type'), null=True)

    def create_subscription_from_contract(self, contract):
        self.contract = contract
        self.save()
        return self

    def create_quote(self):
        quote = Quote()
        quote.contract = self.contract
        quote.discount = 0
        quote.staff = self.contract.staff
        quote.customer = self.contract.defaultcustomer
        quote.status = 'C'
        quote.currency = self.contract.defaultcurrency
        quote.validuntil = date.today().__str__()
        quote.dateofcreation = date.today().__str__()
        quote.save()
        return quote

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self.contract
        invoice.discount = 0
        invoice.staff = self.contract.staff
        invoice.customer = self.contract.defaultcustomer
        invoice.status = 'C'
        invoice.currency = self.contract.defaultcurrency
        invoice.payableuntil = date.today() + timedelta(
            days=self.contract.defaultcustomer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.dateofcreation = date.today().__str__()
        invoice.save()
        return invoice

    class Meta:
        app_label = "subscriptions"
        verbose_name = trans('Subscription')
        verbose_name_plural = trans('Subscriptions')


class SubscriptionEvent(models.Model):
    subscriptions = models.ForeignKey('Subscription', verbose_name=trans('Subscription'))
    eventdate = models.DateField(verbose_name=trans("Event Date"), blank=True, null=True)
    event = models.CharField(max_length=1, choices=SUBSCRITIONEVENTS, verbose_name=trans('Event'))

    def __unicode__(self):
        return self.event

    class Meta:
        app_label = "subscriptions"
        verbose_name = trans('Subscription Event')
        verbose_name_plural = trans('Subscription Events')


class SubscriptionType(Product):
    cancelationPeriod = models.IntegerField(verbose_name=trans("Cancelation Period (months)"), blank=True, null=True)
    automaticContractExtension = models.IntegerField(verbose_name=trans("Automatic Contract Extension (months)"),
                                                     blank=True, null=True)
    automaticContractExtensionReminder = models.IntegerField(
        verbose_name=trans("Automatic Contract Extensoin Reminder (days)"), blank=True, null=True)
    minimumDuration = models.IntegerField(verbose_name=trans("Minimum Contract Duration"), blank=True, null=True)
    paymentIntervall = models.IntegerField(verbose_name=trans("Payment Intervall (days)"), blank=True, null=True)
    contractDocument = FileBrowseField(verbose_name=trans("Contract Documents"), blank=True, null=True, max_length=200)

    class Meta:
        app_label = "subscriptions"
        verbose_name = trans('Subscription Type')
        verbose_name_plural = trans('Subscription Types')
  