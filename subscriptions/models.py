from django.db import models
from filebrowser.fields import FileBrowseField
from const.events import *
import crm import models

class Subscription(crm.Contract):
  subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=_('Subscription Type'))
  startdate = models.DateField(verbose_name = _("Start Date"), blank=True, null=True)
  cancelingdate = models.DateField(verbose_name = _("Canceling Date"), blank=True, null=True)
   
  def createInvoice(self)
    
  
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

  
class SubscriptionType(models.Model):
  title = models.CharField(verbose_name=_("Title"), max_length=200)
  description = models.TextField(verbose_name=_("Description"))
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
  