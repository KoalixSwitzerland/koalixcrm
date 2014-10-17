# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _

PURPOSESADDRESSINCONTRACT = (
    ('D', _('Delivery Address')),
    ('B', _('Billing Address')),
    ('C', _('Contact Address')),
)

PURPOSESADDRESSINCUSTOMER = (
    ('H', _('Private')),
    ('O', _('Business')),
    ('P', _('Mobile Private')),
    ('B', _('Mobile Business')),
)