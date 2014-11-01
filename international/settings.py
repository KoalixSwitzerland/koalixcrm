"""
This file is part of django-international.
Copyright (c) 2012 Monwara LLC.
All rights reserved.

Licensed under BSD license. See LICENSE file for more details.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

def getsetting(setting, default):
    return getattr(settings, setting, default)

COUNTRY_FORM_LABEL = getsetting('COUNTRY_FORM_LABEL', _('country'))
COUNTRY_FORM_INCLUDE_EMPTY = getsetting('COUNTRY_FORM_INCLUDE_EMPTY', False)
COUNTRY_FORM_EMPTY_VALUE = getsetting('COUNTRY_FORM_EMPTY_VALUE', '')
COUNTRY_FORM_EMPTY_LABEL = getsetting('COUNTRY_FORM_EMPTY_LABEL',
                                      _('All countries'))
COUNTRY_FORM_INITIAL_VALUE = getsetting('COUNTRY_FORM_INITIAL_VALUE', None)
COUNTRY_FORM_USE_STATIC = getsetting('COUNTRY_FORM_USE_STATIC', False)
CURRENCY_FORM_LABEL = getsetting('CURRENCY_FORM_LABEL', _('currency'))
CURRENCY_FORM_INCLUDE_EMPTY = getsetting('CURRENCY_FORM_INCLUDE_EMPTY', False)
CURRENCY_FORM_EMPTY_VALUE = getsetting('CURRENCY_FORM_EMPTY_VALUE', '')
CURRENCY_FORM_EMPTY_LABEL = getsetting('CURRENCY_FORM_EMPTY_LABEL',
                                       _('All currencies'))
CURRENCY_FORM_INITIAL_VALUE = getsetting('CURRENCY_FORM_INITIAL_VALUE', None)

