# -*- coding: utf-8 -*

from django.utils.translation import gettext as _

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

PURPOSESTEXTPARAGRAPHINDOCUMENTS = (
    ('BS', _('Before subject')),
    ('AS', _('After subject')),
    ('BT', _('Before total')),
    ('AT', _('After total')),
    ('BW', _('Before wishes')),
    ('AW', _('After wishes')),
    ('C1', _('Custom 1')),
    ('C2', _('Custom 2')),
    ('C3', _('Custom 3')),
    ('C4', _('Custom 4')),
)

PURPOSECALLINCUSTOMER = (
    ('F', _('First commercial call')),
    ('S', _('Planned commercial call')),
    ('A', _('Assistance call')),
)

PURPOSEVISITINCUSTOMER = (
    ('F', _('First commercial visit')),
    ('S', _('Installation')),
)