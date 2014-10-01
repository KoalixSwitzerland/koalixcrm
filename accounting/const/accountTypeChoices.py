# -*- coding: utf-8 -*

from django.utils.translation import ugettext as trans

ACCOUNTTYPECHOICES = (
    ('E', trans('Earnings')),
    ('S', trans('Spendings')),
    ('L', trans('Liabilities')),
    ('A', trans('Assets')),
)