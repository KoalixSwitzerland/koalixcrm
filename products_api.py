# -*- coding: utf-8 -*-
"""
Products API entry point.

Exposes Products REST viewsets for URL routing.
"""
from koalixcrm.products.views.currency_view_set import CurrencyViewSet
from koalixcrm.products.views.tax_view_set import TaxViewSet
from koalixcrm.products.views.unit_view_set import UnitViewSet
from koalixcrm.products.views.product_type_view_set import ProductTypeViewSet

__all__ = [
    'CurrencyViewSet',
    'TaxViewSet',
    'UnitViewSet',
    'ProductTypeViewSet',
]
