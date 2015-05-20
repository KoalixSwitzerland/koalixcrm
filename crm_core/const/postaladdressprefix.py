# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _
from django_utils import choices


class PostalAddressPrefix(choices.Choices):
    Company = choices.Choice('F', _('Company'))
    Mister = choices.Choice('H', _('Mr'))
    Misses = choices.Choice('W', _('Mrs'))
    Miss = choices.Choice('G', _('Ms'))

POSTAL_ADDRESS_PREFIX_CHOICES = (
    ('F', _('Company')),
    ('H', _('Mr')),
    ('W', _('Mrs')),
    ('G', _('Ms')),
)
