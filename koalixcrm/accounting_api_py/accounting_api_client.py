# -*- coding: utf-8 -*-
"""API client for the koalixcrm Accounting app."""
from typing import Any, Dict, List, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.accounting_api_py.dto.account import Account
from koalixcrm.accounting_api_py.dto.accounting_period import AccountingPeriod
from koalixcrm.accounting_api_py.dto.booking import Booking
from koalixcrm.accounting_api_py.dto.product_category import ProductCategory


class KoalixCRMAccountingAPIClient(BaseAPIClient):
    """API client for managing accounts, bookings, and related entities."""

    api_path_env_var = 'KOALIXCRM_ACCOUNTING_API_PATH'
    api_path_default = ''

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    def get_account(self, object_id: int) -> Optional[Account]:
        return self._get_object(Account, "/accounts", object_id)

    def get_account_list(self) -> List[Account]:
        return self._get_object_list(Account, "/accounts/")

    def create_account(self, data: Dict[str, Any]) -> Optional[Account]:
        response_data = self._make_request("/accounts/", method="POST", data=data)
        if response_data:
            obj = Account(response_data, self)
            self._cache.set(Account, obj.id, obj)
            return obj
        return None

    def update_account(self, object_id: int, data: Dict[str, Any]) -> Optional[Account]:
        return self._put_full_update(Account, "/accounts", object_id, data)

    # ------------------------------------------------------------------
    # Accounting Periods
    # ------------------------------------------------------------------

    def get_accounting_period(self, object_id: int) -> Optional[AccountingPeriod]:
        return self._get_object(AccountingPeriod, "/accountingPeriods", object_id)

    def get_accounting_period_list(self) -> List[AccountingPeriod]:
        return self._get_object_list(AccountingPeriod, "/accountingPeriods/")

    def create_accounting_period(self, data: Dict[str, Any]) -> Optional[AccountingPeriod]:
        response_data = self._make_request("/accountingPeriods/", method="POST", data=data)
        if response_data:
            obj = AccountingPeriod(response_data, self)
            self._cache.set(AccountingPeriod, obj.id, obj)
            return obj
        return None

    def update_accounting_period(self, object_id: int, data: Dict[str, Any]) -> Optional[AccountingPeriod]:
        return self._put_full_update(AccountingPeriod, "/accountingPeriods", object_id, data)

    # ------------------------------------------------------------------
    # Bookings
    # ------------------------------------------------------------------

    def get_booking(self, object_id: int) -> Optional[Booking]:
        return self._get_object(Booking, "/bookings", object_id)

    def get_booking_list(self) -> List[Booking]:
        return self._get_object_list(Booking, "/bookings/")

    def create_booking(self, data: Dict[str, Any]) -> Optional[Booking]:
        response_data = self._make_request("/bookings/", method="POST", data=data)
        if response_data:
            obj = Booking(response_data, self)
            self._cache.set(Booking, obj.id, obj)
            return obj
        return None

    def update_booking(self, object_id: int, data: Dict[str, Any]) -> Optional[Booking]:
        return self._put_full_update(Booking, "/bookings", object_id, data)

    # ------------------------------------------------------------------
    # Product Categories
    # ------------------------------------------------------------------

    def get_product_category(self, object_id: int) -> Optional[ProductCategory]:
        return self._get_object(ProductCategory, "/productCategories", object_id)

    def get_product_category_list(self) -> List[ProductCategory]:
        return self._get_object_list(ProductCategory, "/productCategories/")

    def create_product_category(self, data: Dict[str, Any]) -> Optional[ProductCategory]:
        response_data = self._make_request("/productCategories/", method="POST", data=data)
        if response_data:
            obj = ProductCategory(response_data, self)
            self._cache.set(ProductCategory, obj.id, obj)
            return obj
        return None

    def update_product_category(self, object_id: int, data: Dict[str, Any]) -> Optional[ProductCategory]:
        return self._put_full_update(ProductCategory, "/productCategories", object_id, data)
