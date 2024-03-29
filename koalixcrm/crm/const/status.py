# -*- coding: utf-8 -*

from django.utils.translation import gettext as _

INVOICESTATUS = (
    ('P', _('Payed')),
    ('C', _('Invoice created')),
    ('I', _('Invoice sent')),
    ('F', _('First reminder sent')),
    ('R', _('Second reminder sent')),
    ('U', _('Customer cant pay')),
    ('D', _('Deleted')),
)

QUOTESTATUS = (
    ('S', _('Success')),
    ('I', _('Quote created')),
    ('Q', _('Quote sent')),
    ('F', _('First reminder sent')),
    ('R', _('Second reminder sent')),
    ('D', _('Deleted')),
)

PURCHASEORDERSTATUS = (
    ('O', _('Ordered')),
    ('D', _('Delayed')),
    ('Y', _('Delivered')),
    ('I', _('Invoice registered')),
    ('P', _('Invoice payed')),
)

DELIVERYNOTESTATUS = (
    ('C', _('Created')),
    ('S', _('Sent')),
    ('R', _('Received')),
    ('R', _('Lost')),
)

CALLSTATUS = (
    ('P', _('Planned')),
    ('D', _('Delayed')),
    ('R', _('ToRecall')),
    ('F', _('Failed')),
    ('S', _('Success')),
)
