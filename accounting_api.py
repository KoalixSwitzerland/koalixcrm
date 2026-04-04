# -*- coding: utf-8 -*-
"""
Accounting API entry point.

Exposes all Accounting REST viewsets for URL routing.
"""
from koalixcrm.accounting.serializers.restinterface import (
    AccountAsJSON,
    AccountingPeriodAsJSON,
    BookingAsJSON,
    ProductCategoryAsJSON,
)

__all__ = [
    'AccountAsJSON',
    'AccountingPeriodAsJSON',
    'BookingAsJSON',
    'ProductCategoryAsJSON',
]
