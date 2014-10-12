# -*- coding: utf-8 -*

from django.utils.translation import ugettext as _


class InvoiseStatesEnum(object):
    Open = 0
    Payed = 1
    Invoice_created = 2
    Invoice_sent = 3
    First_reminder_sent = 4
    Second_reminder_sent = 5
    Customer_cant_pay = 6
    Deleted = 7


class QuoteStatesEnum(object):
    New = 0
    Success = 1
    Quote_created = 2
    Quote_sent = 3
    First_reminder_sent = 4
    Second_reminder_sent = 5
    Deleted = 6


class PurchaseOrderStatesEnum(object):
    New = 0
    Ordered = 1
    Delayed = 2
    Delivered = 3
    Invoice_registered = 4
    Invoice_payed = 5
