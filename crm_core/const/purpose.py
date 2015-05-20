# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _
from django_utils import choices


class PostalAddressPurpose(choices.Choices):
    DeliveryAddress = choices.Choice('D', _('Delivery Address'))
    BillingAddress = choices.Choice('B', _('Billing Address'))
    ContactAddress = choices.Choice('C', _('Contact Address'))

POSTAL_ADDRESS_PURPOSE_CHOICES = (
    ('D', _('Delivery Address')),
    ('B', _('Billing Address')),
    ('C', _('Contact Address'))
)


class PhoneAddressPurpose(choices.Choices):
    Private = choices.Choice('H', _('Private'))
    Business = choices.Choice('O', _('Business'))
    MobilePrivate = choices.Choice('P', _('Mobile Private'))
    MobileBusiness = choices.Choice('B', _('Mobile Business'))

PHONE_ADDRESS_PURPOSE_CHOICES = (
    ('H', _('Private')),
    ('O', _('Business')),
    ('P', _('Mobile Private')),
    ('B', _('Mobile Business'))
)


class EmailAddressPurpose(choices.Choices):
    Private = choices.Choice('H', _('Private'))
    Business = choices.Choice('O', _('Business'))

EMAIL_ADDRESS_PURPOSE_CHOICES = (
    ('H', _('Private')),
    ('O', _('Business'))
)
