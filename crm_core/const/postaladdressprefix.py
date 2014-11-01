# -*- coding: utf-8 -*
from django_utils import choices
from django.utils.translation import ugettext_lazy as _


class PostalAddressPrefix(choices.Choices):
    Company = choices.Choice('F', _('Company'))
    Mister = choices.Choice('H', _('Mr'))
    Misses = choices.Choice('W', _('Mrs'))
    Miss = choices.Choice('G', _('Ms'))