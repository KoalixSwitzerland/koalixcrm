# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _


POSTAL_ADDRESS_PURPOSE_CHOICES = (
    ('D', _('Delivery Address')),
    ('B', _('Billing Address')),
    ('C', _('Contact Address'))
)


PHONE_ADDRESS_PURPOSE_CHOICES = (
    ('H', _('Private')),
    ('O', _('Business')),
    ('P', _('Mobile Private')),
    ('B', _('Mobile Business'))
)


EMAIL_ADDRESS_PURPOSE_CHOICES = (
    ('H', _('Private')),
    ('O', _('Business'))
)
