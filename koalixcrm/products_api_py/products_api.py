# -*- coding: utf-8 -*-
"""
Products API entry point.

Exposes Products REST viewsets for URL routing.
"""
from koalixcrm.products.views.currency_view_set import CurrencyViewSet
from koalixcrm.products.views.tax_view_set import TaxViewSet
from koalixcrm.products.views.unit_view_set import UnitViewSet
from koalixcrm.products.views.product_type_view_set import ProductTypeViewSet
from koalixcrm.products.views.product_view_set import ProductViewSet
from koalixcrm.products.views.product_price_view_set import ProductPriceViewSet
from koalixcrm.products.views.currency_transform_view_set import CurrencyTransformViewSet
from koalixcrm.products.views.unit_transform_view_set import UnitTransformViewSet
from koalixcrm.products.views.customer_group_transform_view_set import CustomerGroupTransformViewSet

__all__ = [
    'CurrencyViewSet',
    'TaxViewSet',
    'UnitViewSet',
    'ProductTypeViewSet',
    'ProductViewSet',
    'ProductPriceViewSet',
    'CurrencyTransformViewSet',
    'UnitTransformViewSet',
    'CustomerGroupTransformViewSet',
]
