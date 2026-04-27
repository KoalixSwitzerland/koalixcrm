# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.subscriptions.const.events import *


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
