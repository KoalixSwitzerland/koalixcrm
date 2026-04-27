# -*- coding: utf-8 -*-
"""
Accounting API entry point.

Exposes all Accounting REST viewsets for URL routing.
"""
from koalixcrm.accounting.views.account_view_set import AccountViewSet
from koalixcrm.accounting.views.accounting_period_view_set import (
    AccountingPeriodViewSet,
)
from koalixcrm.accounting.views.booking_view_set import BookingViewSet
from koalixcrm.accounting.views.product_category_view_set import ProductCategoryViewSet

__all__ = [
    'AccountViewSet',
    'AccountingPeriodViewSet',
    'BookingViewSet',
    'ProductCategoryViewSet',
]
