# -*- coding: utf-8 -*-
"""
Settings API entry point.

Exposes Settings REST viewsets for URL routing.
"""
from koalixcrm.settings.views.currency_view_set import CurrencyViewSet
from koalixcrm.settings.views.tax_view_set import TaxViewSet
from koalixcrm.settings.views.unit_view_set import UnitViewSet
from koalixcrm.settings.views.currency_transform_view_set import CurrencyTransformViewSet
from koalixcrm.settings.views.unit_transform_view_set import UnitTransformViewSet

__all__ = [
    'CurrencyViewSet',
    'TaxViewSet',
    'UnitViewSet',
    'CurrencyTransformViewSet',
    'UnitTransformViewSet',
]
