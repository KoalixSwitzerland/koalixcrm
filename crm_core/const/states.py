# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _
from django_utils import choices


class ContractStatesEnum(choices.Choices):
    Open = choices.Choice(10, _('open'))
    Payed = choices.Choice(20, _('payed'))
    Invoice_created = choices.Choice(30, _('Invoice created'))
    Invoice_sent = choices.Choice(40, _('Invoice sent'))
    Quote_created = choices.Choice(50, _('Quote created'))
    Quote_sent = choices.Choice(60, _('Quote sent'))
    PurchaseOrder_created = choices.Choice(70, _('Purchaseorder created'))
    Customer_cant_pay = choices.Choice(90, _('Unpayed'))
    Deleted = choices.Choice(100, _('Deleted'))

CONTRACT_STATE_CHOICES = (
    (10, _('open')),
    (20, _('payed')),
    (30, _('Invoice created')),
    (40, _('Invoice sent')),
    (50, _('Quote created')),
    (60, _('Quote sent')),
    (70, _('Purchaseorder created')),
    (90, _('Unpayed')),
    (100, _('Deleted'))
)

class ContractStatesLabelEnum(choices.Choices):
    Open = choices.Choice(10, 'danger')
    Payed = choices.Choice(20, 'default')
    Invoice_created = choices.Choice(30, 'warning')
    Invoice_sent = choices.Choice(40, 'warning')
    Quote_created = choices.Choice(50, 'primary')
    Quote_sent = choices.Choice(60, 'primary')
    PurchaseOrder_created = choices.Choice(70, 'success')
    Customer_cant_pay = choices.Choice(90, 'info')
    Deleted = choices.Choice(100, 'default')
