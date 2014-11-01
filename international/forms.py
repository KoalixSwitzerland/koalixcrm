"""
This file is part of django-international.
Copyright (c) 2012 Monwara LLC.
All rights reserved.

Licensed under BSD license. See LICENSE file for more details.
"""

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

import settings
from models import currencies, countries, Country

def get_arg(kwarg, arg_name, default):
    arg_val = default
    if arg_name in kwarg:
        arg_val = kwarg[arg_name]
        del kwarg[arg_name]
    return arg_val, kwarg



class CountryForm(forms.Form):
    """Country form

    Following settings are applicable:


    COUNTRY_FORM_LABEL
    ------------------

    Label for the 'country' field. Defaults to 'country'.

    COUNTRY_FORM_INCLUDE_EMPTY
    --------------------------

    This settings controls whether country form will include empty value when
    instantiated. You can also use the ``COUNTRY_FORM_EMPTY_VALUE`` to control the
    value of the item that will be treted as empty (no country). Default is
    ``False``.

    COUNTRY_FORM_EMPTY_VALUE
    ------------------------

    This setting controls the value that is assigned to empty value (no country) if
    ``COUNTRY_FORM_INCLUDE_EMPTY`` is set to ``True``.

    COUNTRY_FORM_EMPTY_LABEL
    ------------------------

    Customizes the label for the empty value (no country). Default is 'All
    countries'.

    COUNTRY_FORM_USE_STATIC
    -----------------------

    Use hard-coded values instead of reading the database.

    """

    def __init__(self, *arg, **kwarg):
        use_static, kwarg = get_arg(kwarg, 'use_static',
                                    settings.COUNTRY_FORM_USE_STATIC)
        include_empty, kwarg = get_arg(kwarg, 'include_empty',
                                       settings.COUNTRY_FORM_INCLUDE_EMPTY)
        empty_value, kwarg = get_arg(kwarg, 'empty_value',
                                     settings.COUNTRY_FORM_EMPTY_VALUE)
        empty_label, kwarg = get_arg(kwarg, 'empty_label',
                                     settings.COUNTRY_FORM_EMPTY_LABEL)

        super(CountryForm, self).__init__(*arg, **kwarg)

        choices = []

        # Use static data or not
        if use_static:
            choices = list(countries)
        else:
            # Create choices for country field
            for country in Country.objects.all():
                choices.append((country.code, country.get_code_display()))

        # Include empty or not
        if include_empty:
            choices.insert(0, (empty_value, empty_label))

        # Assign values
        self.fields['country'].choices = choices

    country = forms.ChoiceField(required=False,
                                choices=(),
                                label=settings.COUNTRY_FORM_LABEL,
                                initial=settings.COUNTRY_FORM_INITIAL_VALUE)


class CurrencyForm(forms.Form):
    """Currency form

    Following settings are applicable:


    CURRENCY_FORM_LABEL
    -------------------

    Label for the 'currency' field. Defaults to 'currency'.

    CURRENCY_FORM_INCLUDE_EMPTY
    ---------------------------

    Same as ``COUNTRY_FORM_INCLUDE_EMPTY`` but for currency form.

    CURRENCY_FORM_EMPTY_VALUE
    -------------------------

    Same as ``COUNTRY_FORM_EMPTY_VALUE`` but for currency form.

    CURRENCY_FORM_EMPTY_LABEL
    -------------------------

    Same as ``COUNTRY_FORM_EMPTY_LABEL`` but for currency form. Defaults to 'All
    currencies'.

    """

    def __init__(self, *arg, **kwarg):
        include_empty, kwarg = get_arg(kwarg, 'include_empty',
                                       settings.CURRENCY_FORM_INCLUDE_EMPTY)
        empty_value, kwarg = get_arg(kwarg, 'empty_value',
                                     settings.CURRENCY_FORM_EMPTY_VALUE)
        empty_label, kwarg = get_arg(kwarg, 'empty_label',
                                     settings.CURRENCY_FORM_EMPTY_LABEL)

        super(CurrencyForm, self).__init__(*arg, **kwarg)

        choices = list(currencies)

        if include_empty:
            choices.insert(0, (empty_value, empty_label))

        self.fields['currency'].choices = choices

    currency = forms.ChoiceField(required=False, choices=currencies,
                                 label=settings.CURRENCY_FORM_LABEL,
                                 initial=settings.CURRENCY_FORM_INITIAL_VALUE)


class CountryCurrencyForm(CountryForm, CurrencyForm, forms.Form):
    pass
