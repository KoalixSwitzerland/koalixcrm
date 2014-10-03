# -*- coding: utf-8 -*

from django.utils.translation import ugettext as trans

PURPOSESADDRESSINCONTRACT = (
    ('D', trans('Delivery Address')),
    ('B', trans('Billing Address')),
    ('C', trans('Contact Address')),
)

PURPOSESADDRESSINCUSTOMER = (
    ('H', trans('Private')),
    ('O', trans('Business')),
    ('P', trans('Mobile Private')),
    ('B', trans('Mobile Business')),
)