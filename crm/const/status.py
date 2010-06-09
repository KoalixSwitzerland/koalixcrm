# -*- coding: utf-8 -*

from django.utils.translation import ugettext as _

INVOICESTATES = (
    ('P', _('Payed')),
    ('C', _('Invoice created')),
    ('I', _('Invoice sent')),
    ('F', _('First reminder sent')),
    ('R', _('Second reminder sent')),
    ('U', _('Customer cant pay')),
    ('D', _('Deleted')),
)

QUOTESTATES = (
    ('S', _('Success')),
    ('I', _('Quote created')),
    ('Q', _('Quote sent')),
    ('F', _('First reminder sent')),
    ('R', _('Second reminder sent')),
    ('D', _('Deleted')),
)

PURCHASEORDERSTATES = (
    ('O', _('Ordered')),
    ('D', _('Delayed')),
    ('Y', _('Delivered')),
    ('I', _('Invoice registered')),
    ('P', _('Invoice payed')),
)
