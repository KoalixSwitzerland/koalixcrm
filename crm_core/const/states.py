# -*- coding: utf-8 -*
from django_utils import choices
from django.utils.translation import ugettext_lazy as _


class InvoiceStatesEnum(choices.Choices):
    Open = choices.Choice(1, _('Open'))
    Payed = choices.Choice(2, _('Payed'))
    Invoice_created = choices.Choice(3, _('Invoice created'))
    Invoice_sent = choices.Choice(4, _('Invoice sent'))
    First_reminder_sent = choices.Choice(5, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(6, _('Second reminder sent'))
    Customer_cant_pay = choices.Choice(7, _('Unpayed'))
    Deleted = choices.Choice(8, _('Deleted'))


class QuoteStatesEnum(choices.Choices):
    New = choices.Choice(1, _('New'))
    Success = choices.Choice(2, _('Success'))
    Quote_created = choices.Choice(3, _('Quote created'))
    Quote_sent = choices.Choice(4, _('Quote sent'))
    First_reminder_sent = choices.Choice(5, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(6, _('Second reminder sent'))
    Deleted = choices.Choice(7, _('Deleted'))


class PurchaseOrderStatesEnum(choices.Choices):
    New = choices.Choice(1, _('New'))
    Ordered = choices.Choice(2, _('Ordered'))
    Delayed = choices.Choice(3, _('Delayed'))
    Delivered = choices.Choice(4, _('Delivered'))
    Invoice_registered = choices.Choice(5, _('Invoice registered'))
    Invoice_payed = choices.Choice(6, _('Invoice payed'))
