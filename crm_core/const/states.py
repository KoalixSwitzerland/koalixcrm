# -*- coding: utf-8 -*
from django_utils import choices
from django.utils.translation import ugettext_lazy as _


class InvoiceStatesEnum(choices.Choices):
    Open = choices.Choice(10, _('open'))
    Payed = choices.Choice(20, _('payed'))
    Invoice_created = choices.Choice(30, _('Invoice created'))
    Invoice_sent = choices.Choice(40, _('Invoice sent'))
    First_reminder_sent = choices.Choice(50, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(60, _('Second reminder sent'))
    Customer_cant_pay = choices.Choice(70, _('Unpayed'))
    Deleted = choices.Choice(80, _('Deleted'))


class InvoiceStatesLabelEnum(choices.Choices):
    Open = choices.Choice(10, 'primary')
    Payed = choices.Choice(20, 'success')
    Invoice_created = choices.Choice(30, 'info')
    Invoice_sent = choices.Choice(40, 'warning')
    First_reminder_sent = choices.Choice(50, 'warning')
    Second_reminder_sent = choices.Choice(60, 'danger')
    Customer_cant_pay = choices.Choice(70, 'default')
    Deleted = choices.Choice(80, 'default')


class QuoteStatesEnum(choices.Choices):
    New = choices.Choice(10, _('New'))
    Success = choices.Choice(20, _('Success'))
    Quote_created = choices.Choice(30, _('Quote created'))
    Quote_sent = choices.Choice(40, _('Quote sent'))
    Purchaseorder_created = choices.Choice(50, _('Purchaseorder created'))
    First_reminder_sent = choices.Choice(60, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(70, _('Second reminder sent'))
    Deleted = choices.Choice(80, _('Deleted'))


class QuoteStatesLabelEnum(choices.Choices):
    New = choices.Choice(10, 'default')
    Success = choices.Choice(20, 'success')
    Quote_created = choices.Choice(30, 'info')
    Quote_sent = choices.Choice(40, 'warning')
    Purchaseorder_created = choices.Choice(50, 'info')
    First_reminder_sent = choices.Choice(60, 'warning')
    Second_reminder_sent = choices.Choice(70, 'danger')
    Deleted = choices.Choice(80, 'default')


class PurchaseOrderStatesEnum(choices.Choices):
    New = choices.Choice(10, _('New'))
    Ordered = choices.Choice(20, _('Ordered'))
    Delayed = choices.Choice(30, _('Delayed'))
    Delivered = choices.Choice(40, _('Delivered'))
    Invoice_registered = choices.Choice(50, _('Invoice registered'))
    Invoice_payed = choices.Choice(60, _('Invoice payed'))


class PurchaseOrderStatesLabelEnum(choices.Choices):
    New = choices.Choice(10, 'default')
    Ordered = choices.Choice(20, 'warning')
    Delayed = choices.Choice(30, 'danger')
    Delivered = choices.Choice(40, 'info')
    Invoice_registered = choices.Choice(50, 'info')
    Invoice_payed = choices.Choice(60, 'success')


class ContractStatesEnum(choices.Choices):
    Open = choices.Choice(10, _('open'))
    Payed = choices.Choice(20, _('payed'))
    Invoice_created = choices.Choice(30, _('Invoice created'))
    Invoice_sent = choices.Choice(40, _('Invoice sent'))
    Quote_created = choices.Choice(50, _('Quote created'))
    Quote_sent = choices.Choice(60, _('Quote sent'))
    PurchaseOrder_created = choices.Choice(70, _('Quote created'))
    Customer_cant_pay = choices.Choice(90, _('Unpayed'))
    Deleted = choices.Choice(100, _('Deleted'))


class ContractStatesLabelEnum(choices.Choices):
    Open = choices.Choice(10, 'primary')
    Payed = choices.Choice(20, 'success')
    Invoice_created = choices.Choice(30, 'info')
    Invoice_sent = choices.Choice(40, 'warning')
    Quote_created = choices.Choice(50, 'info')
    Quote_sent = choices.Choice(60, 'warning')
    PurchaseOrder_created = choices.Choice(70, 'info')
    Customer_cant_pay = choices.Choice(90, 'default')
    Deleted = choices.Choice(100, 'default')