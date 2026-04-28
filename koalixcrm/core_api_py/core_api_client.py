# -*- coding: utf-8 -*-
"""KoalixCRM Core API Client"""
from __future__ import annotations

from typing import Any

from koalixcrm.core_api_py.dto.currency import Currency
from koalixcrm.core_api_py.dto.currency_transform import CurrencyTransform
from koalixcrm.core_api_py.dto.tax import Tax
from koalixcrm.core_api_py.dto.unit import Unit
from koalixcrm.core_api_py.dto.unit_transform import UnitTransform
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMCoreAPIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_CORE_API_PATH'
    api_path_default = '/koalixcrm_core/api/v1/'
    uses_workspace_id = True

    def __init__(
        self,
        api_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        workspace_id: int | None = None,
    ) -> None:
        super().__init__(api_url=api_url, username=username, password=password, workspace_id=workspace_id)

    # ------------------------------------------------------------------
    # Currency (endpoint: /currencies)
    # ------------------------------------------------------------------

    def get_currency(self, object_id: int) -> Currency | None:
        return self._get_object(Currency, "/currencies", object_id)

    def get_currency_list(self) -> list[Currency]:
        return self._get_object_list(Currency, "/currencies/")

    def create_currency(self, data: dict[str, Any]) -> Currency | None:
        response_data = self._make_request("/currencies/", method="POST", data=data)
        if response_data:
            obj = Currency(response_data, self)
            self._cache.set(Currency, obj.id, obj)
            return obj
        return None

    def update_currency(self, object_id: int, data: dict[str, Any]) -> Currency | None:
        return self._put_full_update(Currency, "/currencies", object_id, data)

    # ------------------------------------------------------------------
    # Tax (endpoint: /taxes)
    # ------------------------------------------------------------------

    def get_tax(self, object_id: int) -> Tax | None:
        return self._get_object(Tax, "/taxes", object_id)

    def get_tax_list(self) -> list[Tax]:
        return self._get_object_list(Tax, "/taxes/")

    def create_tax(self, data: dict[str, Any]) -> Tax | None:
        response_data = self._make_request("/taxes/", method="POST", data=data)
        if response_data:
            obj = Tax(response_data, self)
            self._cache.set(Tax, obj.id, obj)
            return obj
        return None

    def update_tax(self, object_id: int, data: dict[str, Any]) -> Tax | None:
        return self._put_full_update(Tax, "/taxes", object_id, data)

    # ------------------------------------------------------------------
    # Unit (endpoint: /units)
    # ------------------------------------------------------------------

    def get_unit(self, object_id: int) -> Unit | None:
        return self._get_object(Unit, "/units", object_id)

    def get_unit_list(self) -> list[Unit]:
        return self._get_object_list(Unit, "/units/")

    def create_unit(self, data: dict[str, Any]) -> Unit | None:
        response_data = self._make_request("/units/", method="POST", data=data)
        if response_data:
            obj = Unit(response_data, self)
            self._cache.set(Unit, obj.id, obj)
            return obj
        return None

    def update_unit(self, object_id: int, data: dict[str, Any]) -> Unit | None:
        return self._put_full_update(Unit, "/units", object_id, data)

    # ------------------------------------------------------------------
    # CurrencyTransform (endpoint: /currency_transforms)
    # ------------------------------------------------------------------

    def get_currency_transform(self, object_id: int) -> CurrencyTransform | None:
        return self._get_object(CurrencyTransform, "/currency-transforms", object_id)

    def get_currency_transform_list(self) -> list[CurrencyTransform]:
        return self._get_object_list(CurrencyTransform, "/currency-transforms/")

    def create_currency_transform(self, data: dict[str, Any]) -> CurrencyTransform | None:
        response_data = self._make_request("/currency-transforms/", method="POST", data=data)
        if response_data:
            obj = CurrencyTransform(response_data, self)
            self._cache.set(CurrencyTransform, obj.id, obj)
            return obj
        return None

    def update_currency_transform(self, object_id: int, data: dict[str, Any]) -> CurrencyTransform | None:
        return self._put_full_update(CurrencyTransform, "/currency-transforms", object_id, data)

    # ------------------------------------------------------------------
    # UnitTransform (endpoint: /unit_transforms)
    # ------------------------------------------------------------------

    def get_unit_transform(self, object_id: int) -> UnitTransform | None:
        return self._get_object(UnitTransform, "/unit-transforms", object_id)

    def get_unit_transform_list(self) -> list[UnitTransform]:
        return self._get_object_list(UnitTransform, "/unit-transforms/")

    def create_unit_transform(self, data: dict[str, Any]) -> UnitTransform | None:
        response_data = self._make_request("/unit-transforms/", method="POST", data=data)
        if response_data:
            obj = UnitTransform(response_data, self)
            self._cache.set(UnitTransform, obj.id, obj)
            return obj
        return None

    def update_unit_transform(self, object_id: int, data: dict[str, Any]) -> UnitTransform | None:
        return self._put_full_update(UnitTransform, "/unit-transforms", object_id, data)
