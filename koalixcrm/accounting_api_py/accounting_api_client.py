# -*- coding: utf-8 -*-
"""API client for the koalixcrm Accounting app."""
from __future__ import annotations

from typing import Any

from koalixcrm.accounting_api_py.dto.account import Account
from koalixcrm.accounting_api_py.dto.accounting_period import AccountingPeriod
from koalixcrm.accounting_api_py.dto.booking import Booking
from koalixcrm.accounting_api_py.dto.product_category import ProductCategory
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMAccountingAPIClient(BaseAPIClient):
    """API client for managing accounts, bookings, and related entities."""

    api_path_env_var = 'KOALIXCRM_ACCOUNTING_API_PATH'
    api_path_default = '/koalixcrm_accounting/api/v1/'
    uses_workspace_id = True

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    def get_account(self, object_id: int) -> Account | None:
        return self._get_object(Account, "/accounts", object_id)

    def get_account_list(self) -> list[Account]:
        return self._get_object_list(Account, "/accounts/")

    def create_account(self, data: dict[str, Any]) -> Account | None:
        response_data = self._make_request("/accounts/", method="POST", data=data)
        if response_data:
            obj = Account(response_data, self)
            self._cache.set(Account, obj.id, obj)
            return obj
        return None

    def update_account(self, object_id: int, data: dict[str, Any]) -> Account | None:
        return self._put_full_update(Account, "/accounts", object_id, data)

    # ------------------------------------------------------------------
    # Accounting Periods
    # ------------------------------------------------------------------

    def get_accounting_period(self, object_id: int) -> AccountingPeriod | None:
        return self._get_object(AccountingPeriod, "/accounting-periods", object_id)

    def get_accounting_period_list(self) -> list[AccountingPeriod]:
        return self._get_object_list(AccountingPeriod, "/accounting-periods/")

    def create_accounting_period(self, data: dict[str, Any]) -> AccountingPeriod | None:
        response_data = self._make_request("/accounting-periods/", method="POST", data=data)
        if response_data:
            obj = AccountingPeriod(response_data, self)
            self._cache.set(AccountingPeriod, obj.id, obj)
            return obj
        return None

    def update_accounting_period(self, object_id: int, data: dict[str, Any]) -> AccountingPeriod | None:
        return self._put_full_update(AccountingPeriod, "/accounting-periods", object_id, data)

    # ------------------------------------------------------------------
    # Bookings
    # ------------------------------------------------------------------

    def get_booking(self, object_id: int) -> Booking | None:
        return self._get_object(Booking, "/bookings", object_id)

    def get_booking_list(self) -> list[Booking]:
        return self._get_object_list(Booking, "/bookings/")

    def create_booking(self, data: dict[str, Any]) -> Booking | None:
        response_data = self._make_request("/bookings/", method="POST", data=data)
        if response_data:
            obj = Booking(response_data, self)
            self._cache.set(Booking, obj.id, obj)
            return obj
        return None

    def update_booking(self, object_id: int, data: dict[str, Any]) -> Booking | None:
        return self._put_full_update(Booking, "/bookings", object_id, data)

    # ------------------------------------------------------------------
    # Product Categories
    # ------------------------------------------------------------------

    def get_product_category(self, object_id: int) -> ProductCategory | None:
        return self._get_object(ProductCategory, "/product-categories", object_id)

    def get_product_category_list(self) -> list[ProductCategory]:
        return self._get_object_list(ProductCategory, "/product-categories/")

    def create_product_category(self, data: dict[str, Any]) -> ProductCategory | None:
        response_data = self._make_request("/product-categories/", method="POST", data=data)
        if response_data:
            obj = ProductCategory(response_data, self)
            self._cache.set(ProductCategory, obj.id, obj)
            return obj
        return None

    def update_product_category(self, object_id: int, data: dict[str, Any]) -> ProductCategory | None:
        return self._put_full_update(ProductCategory, "/product-categories", object_id, data)
