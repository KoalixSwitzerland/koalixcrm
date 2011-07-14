from django.db import models
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField
from const.events import *
import crm

class Subscription(crm.models.Contract):
  subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=_('Subscription Type'))
  startdate = models.DateField(verbose_name = _("Start Date"), blank=True, null=True)
  cancelingdate = models.DateField(verbose_name = _("Canceling Date"), blank=True, null=True)
   
  def createInvoice(self):
    Invoice()
    return invoice
  
  class Meta:
     app_label = "subscriptions"
     #app_label_koalix = _("Subscriptions")
     verbose_name = _('Subscription')
     verbose_name_plural = _('Subscriptions')
  
class SubscriptionEvent(models.Model):
  subscriptions =  models.ForeignKey('Subscription', verbose_name= _('Subscription'))
  eventdate = models.DateField(verbose_name = _("Event Date"), blank=True, null=True)
  event = models.CharField(max_length=1, choices=SUBSCRITIONEVENTS, verbose_name=_('Event'))
    
  def __unicode__(self):
    return  self.event
   
  class Meta:
     app_label = "subscriptions"
     #app_label_koalix = _("Subscriptions")
     verbose_name = _('Subscription Event')
     verbose_name_plural = _('Subscription Events')

  
class SubscriptionType(crm.models.Product):
  cancelationPeriod = models.IntegerField(verbose_name = _("Cancelation Period (months)"), blank=True, null=True)
  automaticContractExtension = models.IntegerField(verbose_name = _("Automatic Contract Extension (months)"), blank=True, null=True)
  automaticContractExtensionReminder = models.IntegerField(verbose_name = _("Automatic Contract Extensoin Reminder (days)"), blank=True, null=True)
  minimumDuration = models.IntegerField(verbose_name = _("Minimum Contract Duration"), blank=True, null=True)
  paymentIntervall = models.IntegerField(verbose_name = _("Payment Intervall (days)"), blank=True, null=True)
  contractDocument = FileBrowseField(verbose_name=_("Contract Documents"), blank=True, null=True, max_length=200)
   
  class Meta:
     app_label = "subscriptions"
     #app_label_koalix = _("Subscriptions")
     verbose_name = _('Subscription Type')
     verbose_name_plural = _('Subscription Types')
  