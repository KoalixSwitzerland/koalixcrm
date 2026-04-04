# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _
from filebrowser.fields import FileBrowseField


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
