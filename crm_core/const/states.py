# -*- coding: utf-8 -*
from django_utils import choices
from django.utils.translation import ugettext_lazy as _


class InvoiceStatesEnum(choices.Choices):
    Open = choices.Choice(10, _('Open'))
    Payed = choices.Choice(20, _('Payed'))
    Invoice_created = choices.Choice(30, _('Invoice created'))
    Invoice_sent = choices.Choice(40, _('Invoice sent'))
    First_reminder_sent = choices.Choice(50, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(60, _('Second reminder sent'))
    Customer_cant_pay = choices.Choice(70, _('Unpayed'))
    Deleted = choices.Choice(80, _('Deleted'))


class InvoiceStatesLabelEnum(choices.Choices):
    Open = choices.Choice(10, 'label-primary')
    Payed = choices.Choice(20, 'label-success')
    Invoice_created = choices.Choice(30, 'label-info')
    Invoice_sent = choices.Choice(40, 'label-warning')
    First_reminder_sent = choices.Choice(50, 'label-warning')
    Second_reminder_sent = choices.Choice(60, 'label-danger')
    Customer_cant_pay = choices.Choice(70, 'label-default')
    Deleted = choices.Choice(80, 'label-default')


class QuoteStatesEnum(choices.Choices):
    New = choices.Choice(10, _('New'))
    Success = choices.Choice(20, _('Success'))
    Quote_created = choices.Choice(30, _('Quote created'))
    Quote_sent = choices.Choice(40, _('Quote sent'))
    Purchaseorder_created = choices.Choice(50, _('Purchase order created'))
    First_reminder_sent = choices.Choice(60, _('First reminder sent'))
    Second_reminder_sent = choices.Choice(70, _('Second reminder sent'))
    Deleted = choices.Choice(80, _('Deleted'))


class QuoteStatesLabelEnum(choices.Choices):
    New = choices.Choice(10, 'label-default')
    Success = choices.Choice(20, 'label-success')
    Quote_created = choices.Choice(30, 'label-info')
    Quote_sent = choices.Choice(40, 'label-warning')
    Purchaseorder_created = choices.Choice(50, 'label-info')
    First_reminder_sent = choices.Choice(60, 'label-warning')
    Second_reminder_sent = choices.Choice(70, 'label-danger')
    Deleted = choices.Choice(80, 'label-default')


class PurchaseOrderStatesEnum(choices.Choices):
    New = choices.Choice(10, _('New'))
    Ordered = choices.Choice(20, _('Ordered'))
    Delayed = choices.Choice(30, _('Delayed'))
    Delivered = choices.Choice(40, _('Delivered'))
    Invoice_registered = choices.Choice(50, _('Invoice registered'))
    Invoice_payed = choices.Choice(60, _('Invoice payed'))


class PurchaseOrderStatesLabelEnum(choices.Choices):
    New = choices.Choice(10, 'label-default')
    Ordered = choices.Choice(20, 'label-warning')
    Delayed = choices.Choice(30, 'label-danger')
    Delivered = choices.Choice(40, 'label-info')
    Invoice_registered = choices.Choice(50, 'label-info')
    Invoice_payed = choices.Choice(60, 'label-success')


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
    Open = choices.Choice(10, 'label-primary')
    Payed = choices.Choice(20, 'label-success')
    Invoice_created = choices.Choice(30, 'label-info')
    Invoice_sent = choices.Choice(40, 'label-warning')
    Quote_created = choices.Choice(50, 'label-info')
    Quote_sent = choices.Choice(60, 'label-warning')
    PurchaseOrder_created = choices.Choice(70, 'label-info')
    Customer_cant_pay = choices.Choice(90, 'label-default')
    Deleted = choices.Choice(100, 'label-default')