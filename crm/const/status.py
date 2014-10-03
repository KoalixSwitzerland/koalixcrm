# -*- coding: utf-8 -*

from django.utils.translation import ugettext as trans

INVOICESTATUS = (
    ('P', trans('Payed')),
    ('C', trans('Invoice created')),
    ('I', trans('Invoice sent')),
    ('F', trans('First reminder sent')),
    ('R', trans('Second reminder sent')),
    ('U', trans('Customer cant pay')),
    ('D', trans('Deleted')),
)

QUOTESTATUS = (
    ('S', trans('Success')),
    ('I', trans('Quote created')),
    ('Q', trans('Quote sent')),
    ('F', trans('First reminder sent')),
    ('R', trans('Second reminder sent')),
    ('D', trans('Deleted')),
)

PURCHASEORDERSTATUS = (
    ('O', trans('Ordered')),
    ('D', trans('Delayed')),
    ('Y', trans('Delivered')),
    ('I', trans('Invoice registered')),
    ('P', trans('Invoice payed')),
)
