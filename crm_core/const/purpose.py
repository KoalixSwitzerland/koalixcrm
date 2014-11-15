# -*- coding: utf-8 -*
from django_utils import choices
from django.utils.translation import ugettext_lazy as _


class PostalAddressPurpose(choices.Choices):
    DeliveryAddress = choices.Choice('D', _('Delivery Address'))
    BillingAddress = choices.Choice('B', _('Billing Address'))
    ContactAddress = choices.Choice('C', _('Contact Address'))


class PhoneAddressPurpose(choices.Choices):
    Private = choices.Choice('H', _('Private'))
    Business = choices.Choice('O', _('Business'))
    MobilePrivate = choices.Choice('P', _('Mobile Private'))
    MobileBusiness = choices.Choice('B', _('Mobile Business'))


class EmailAddressPurpose(choices.Choices):
    Private = choices.Choice('H', _('Private'))
    Business = choices.Choice('O', _('Business'))