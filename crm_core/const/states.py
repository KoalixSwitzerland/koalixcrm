# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _
from enum import Enum


class InvoiceStatesEnum(Enum):
    Open = 1
    Payed = 2
    Invoice_created = 3
    Invoice_sent = 4
    First_reminder_sent = 5
    Second_reminder_sent = 6
    Customer_cant_pay = 7
    Deleted = 8


class QuoteStatesEnum(Enum):
    New = 1
    Success = 2
    Quote_created = 3
    Quote_sent = 4
    First_reminder_sent = 5
    Second_reminder_sent = 6
    Deleted = 7


class PurchaseOrderStatesEnum(Enum):
    New = 1
    Ordered = 2
    Delayed = 3
    Delivered = 4
    Invoice_registered = 5
    Invoice_payed = 6
