# -*- coding: utf-8 -*-
"""
Core API entry point.

Exposes Core (shared value objects) REST viewsets for URL routing.
"""

from __future__ import annotations

from koalixcrm.core_api_py.currency_transform_view_set import CurrencyTransformViewSet
from koalixcrm.core_api_py.currency_view_set import CurrencyViewSet
from koalixcrm.core_api_py.tax_view_set import TaxViewSet
from koalixcrm.core_api_py.unit_transform_view_set import UnitTransformViewSet
from koalixcrm.core_api_py.unit_view_set import UnitViewSet

__all__ = [
    'CurrencyViewSet',
    'TaxViewSet',
    'UnitViewSet',
    'CurrencyTransformViewSet',
    'UnitTransformViewSet',
]
