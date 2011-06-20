from django.db import models

class Subscription
  customer = customer
  stopdate = datefield
  stopdate =   datefield
  staff = userfield
  lastmodified = datefield
  lastmodifiedby = datefield
  
  def __unicode__(self):
    return  self.title
   
  class Meta:
     app_label = "subscriptions"
     #app_label_koalix = _("Subscriptions")
     verbose_name = _('Subscription')
     verbose_name_plural = _('Subscriptions')
  
class Subscriptiontype
  kuendbarkeit = integerfield
  contractduration = integerfield
  vertragsverlaengerungbeinnichtkuendigung = integerfield
  vertragsintervall = integerfield
  zahlungsintervall = integerfield
  vertragsdokumente = Filebrowserfield
   
  class Meta:
     app_label = "subscriptions"
     #app_label_koalix = _("Subscriptions")
     verbose_name = _('Subscription Type')
     verbose_name_plural = _('Subscription Types')
  