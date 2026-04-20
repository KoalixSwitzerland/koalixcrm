# -*- coding: utf-8 -*-
"""KoalixCRM Core API Client"""
from typing import Dict, List, Any, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.core_api_py.dto.currency import Currency
from koalixcrm.core_api_py.dto.tax import Tax
from koalixcrm.core_api_py.dto.unit import Unit
from koalixcrm.core_api_py.dto.currency_transform import CurrencyTransform
from koalixcrm.core_api_py.dto.unit_transform import UnitTransform


class KoalixCRMCoreAPIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_CORE_API_PATH'
    api_path_default = '/koalixcrm_core/api/v1/'
    uses_workspace_id = True

    def __init__(self, api_url=None, username=None, password=None, workspace_id=None):
        super().__init__(api_url=api_url, username=username, password=password, workspace_id=workspace_id)

    # ------------------------------------------------------------------
    # Currency (endpoint: /currencies)
    # ------------------------------------------------------------------

    def get_currency(self, object_id: int) -> Optional[Currency]:
        return self._get_object(Currency, "/currencies", object_id)

    def get_currency_list(self) -> List[Currency]:
        return self._get_object_list(Currency, "/currencies/")

    def create_currency(self, data: Dict[str, Any]) -> Optional[Currency]:
        response_data = self._make_request("/currencies/", method="POST", data=data)
        if response_data:
            obj = Currency(response_data, self)
            self._cache.set(Currency, obj.id, obj)
            return obj
        return None

    def update_currency(self, object_id: int, data: Dict[str, Any]) -> Optional[Currency]:
        return self._put_full_update(Currency, "/currencies", object_id, data)

    # ------------------------------------------------------------------
    # Tax (endpoint: /taxes)
    # ------------------------------------------------------------------

    def get_tax(self, object_id: int) -> Optional[Tax]:
        return self._get_object(Tax, "/taxes", object_id)

    def get_tax_list(self) -> List[Tax]:
        return self._get_object_list(Tax, "/taxes/")

    def create_tax(self, data: Dict[str, Any]) -> Optional[Tax]:
        response_data = self._make_request("/taxes/", method="POST", data=data)
        if response_data:
            obj = Tax(response_data, self)
            self._cache.set(Tax, obj.id, obj)
            return obj
        return None

    def update_tax(self, object_id: int, data: Dict[str, Any]) -> Optional[Tax]:
        return self._put_full_update(Tax, "/taxes", object_id, data)

    # ------------------------------------------------------------------
    # Unit (endpoint: /units)
    # ------------------------------------------------------------------

    def get_unit(self, object_id: int) -> Optional[Unit]:
        return self._get_object(Unit, "/units", object_id)

    def get_unit_list(self) -> List[Unit]:
        return self._get_object_list(Unit, "/units/")

    def create_unit(self, data: Dict[str, Any]) -> Optional[Unit]:
        response_data = self._make_request("/units/", method="POST", data=data)
        if response_data:
            obj = Unit(response_data, self)
            self._cache.set(Unit, obj.id, obj)
            return obj
        return None

    def update_unit(self, object_id: int, data: Dict[str, Any]) -> Optional[Unit]:
        return self._put_full_update(Unit, "/units", object_id, data)

    # ------------------------------------------------------------------
    # CurrencyTransform (endpoint: /currency_transforms)
    # ------------------------------------------------------------------

    def get_currency_transform(self, object_id: int) -> Optional[CurrencyTransform]:
        return self._get_object(CurrencyTransform, "/currency-transforms", object_id)

    def get_currency_transform_list(self) -> List[CurrencyTransform]:
        return self._get_object_list(CurrencyTransform, "/currency-transforms/")

    def create_currency_transform(self, data: Dict[str, Any]) -> Optional[CurrencyTransform]:
        response_data = self._make_request("/currency-transforms/", method="POST", data=data)
        if response_data:
            obj = CurrencyTransform(response_data, self)
            self._cache.set(CurrencyTransform, obj.id, obj)
            return obj
        return None

    def update_currency_transform(self, object_id: int, data: Dict[str, Any]) -> Optional[CurrencyTransform]:
        return self._put_full_update(CurrencyTransform, "/currency-transforms", object_id, data)

    # ------------------------------------------------------------------
    # UnitTransform (endpoint: /unit_transforms)
    # ------------------------------------------------------------------

    def get_unit_transform(self, object_id: int) -> Optional[UnitTransform]:
        return self._get_object(UnitTransform, "/unit-transforms", object_id)

    def get_unit_transform_list(self) -> List[UnitTransform]:
        return self._get_object_list(UnitTransform, "/unit-transforms/")

    def create_unit_transform(self, data: Dict[str, Any]) -> Optional[UnitTransform]:
        response_data = self._make_request("/unit-transforms/", method="POST", data=data)
        if response_data:
            obj = UnitTransform(response_data, self)
            self._cache.set(UnitTransform, obj.id, obj)
            return obj
        return None

    def update_unit_transform(self, object_id: int, data: Dict[str, Any]) -> Optional[UnitTransform]:
        return self._put_full_update(UnitTransform, "/unit-transforms", object_id, data)
