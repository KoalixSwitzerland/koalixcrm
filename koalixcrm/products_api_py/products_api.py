# -*- coding: utf-8 -*-
"""
Products API entry point.

Exposes Products REST viewsets for URL routing.
"""

from __future__ import annotations

from koalixcrm.products.views.customer_group_transform_view_set import (
    CustomerGroupTransformViewSet,
)
from koalixcrm.products.views.product_price_view_set import ProductPriceViewSet
from koalixcrm.products.views.product_type_view_set import ProductTypeViewSet
from koalixcrm.products.views.product_view_set import ProductViewSet

__all__ = [
    'ProductTypeViewSet',
    'ProductViewSet',
    'ProductPriceViewSet',
    'CustomerGroupTransformViewSet',
]
