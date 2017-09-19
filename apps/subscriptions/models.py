from datetime import *

from django.db import models
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField
from apps.crm import models as crmmodels
from apps.subscriptions.const.events import *


class Subscription(models.Model):
    contract = models.ForeignKey(crmmodels.Contract, verbose_name=_('Subscription Type'))
    subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=_('Subscription Type'), null=True)

    def createSubscriptionFromContract(self, contract):
        self.contract = contract
        self.save()
        return self

    def createQuote(self):
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

    def createInvoice(self):
        invoice = crmmodels.Invoice()
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
        # app_label_koalix = _("Subscriptions")
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class SubscriptionEvent(models.Model):
    subscriptions = models.ForeignKey('Subscription', verbose_name=_('Subscription'))
    eventdate = models.DateField(verbose_name=_("Event Date"), blank=True, null=True)
    event = models.CharField(max_length=1, choices=SUBSCRITIONEVENTS, verbose_name=_('Event'))

    def __str__(self):
        return self.event

    class Meta:
        app_label = "subscriptions"
        # app_label_koalix = _("Subscriptions")
        verbose_name = _('Subscription Event')
        verbose_name_plural = _('Subscription Events')


class SubscriptionType(crmmodels.Product):
    cancelationPeriod = models.IntegerField(verbose_name=_("Cancelation Period (months)"), blank=True, null=True)
    automaticContractExtension = models.IntegerField(verbose_name=_("Automatic Contract Extension (months)"),
                                                     blank=True, null=True)
    automaticContractExtensionReminder = models.IntegerField(
        verbose_name=_("Automatic Contract Extensoin Reminder (days)"), blank=True, null=True)
    minimumDuration = models.IntegerField(verbose_name=_("Minimum Contract Duration"), blank=True, null=True)
    paymentIntervall = models.IntegerField(verbose_name=_("Payment Intervall (days)"), blank=True, null=True)
    contractDocument = FileBrowseField(verbose_name=_("Contract Documents"), blank=True, null=True, max_length=200)

    class Meta:
        app_label = "subscriptions"
        # app_label_koalix = _("Subscriptions")
        verbose_name = _('Subscription Type')
        verbose_name_plural = _('Subscription Types')
