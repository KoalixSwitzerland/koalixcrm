from django.db import models
from filebrowser.fields import FileBrowseField
from const.events import *
import crm import models

class Subscription(models.Model):
  customer = models.ForeignKey('Customer', verbose_name= _('Customer'))
  subscriptiontype = models.ForeignKey('SubscriptionType', verbose_name=_('Subscription Type'))
  startdate = models.DateField(verbose_name = _("Start Date"), blank=True, null=True)
  staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relpostaff", null=True)
  cancelingdate = models.DateField(verbose_name = _("Canceling Date"), blank=True, null=True)
  lastmodification = models.DateTimeField(verbose_name = _("Last modified"), auto_now_add=True)
  lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_polstmodified")
  
  def __unicode__(self):
    return  self.title
   
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
  