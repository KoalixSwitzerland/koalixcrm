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

QUOTATIONSTATUS = (
    ('S', _('Success')),
    ('I', _('Quotation created')),
    ('Q', _('Quotation sent')),
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

DESPATCHADVICESTATUS = (
    ('C', _('Created')),
    ('S', _('Sent')),
    ('R', _('Received')),
    ('R', _('Lost')),
)

CREDITNOTESTATUS = (
    ('C', _('Credit note created')),
    ('S', _('Credit note sent')),
    ('B', _('Booked')),
    ('D', _('Deleted')),
)

CALLSTATUS = (
    ('P', _('Planned')),
    ('D', _('Delayed')),
    ('R', _('ToRecall')),
    ('F', _('Failed')),
    ('S', _('Success')),
)
