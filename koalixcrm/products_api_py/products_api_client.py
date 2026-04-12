# -*- coding: utf-8 -*-
"""KoalixCRM Products API Client"""
from typing import Dict, List, Any, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.products_api_py.dto.currency import Currency
from koalixcrm.products_api_py.dto.tax import Tax
from koalixcrm.products_api_py.dto.unit import Unit
from koalixcrm.products_api_py.dto.product_type import ProductType
from koalixcrm.products_api_py.dto.product import Product
from koalixcrm.products_api_py.dto.product_price import ProductPrice
from koalixcrm.products_api_py.dto.price import Price
from koalixcrm.products_api_py.dto.currency_transform import CurrencyTransform
from koalixcrm.products_api_py.dto.unit_transform import UnitTransform
from koalixcrm.products_api_py.dto.customer_group_transform import CustomerGroupTransform


class KoalixCRMProductsAPIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_PRODUCTS_API_PATH'
    api_path_default = ''

    def __init__(self, api_url=None, username=None, password=None):
        super().__init__(api_url=api_url, username=username, password=password)

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
    # ProductType (endpoint: /products)
    # ------------------------------------------------------------------

    def get_product_type(self, object_id: int) -> Optional[ProductType]:
        return self._get_object(ProductType, "/products", object_id)

    def get_product_type_list(self) -> List[ProductType]:
        return self._get_object_list(ProductType, "/products/")

    def create_product_type(self, data: Dict[str, Any]) -> Optional[ProductType]:
        response_data = self._make_request("/products/", method="POST", data=data)
        if response_data:
            obj = ProductType(response_data, self)
            self._cache.set(ProductType, obj.id, obj)
            return obj
        return None

    def update_product_type(self, object_id: int, data: Dict[str, Any]) -> Optional[ProductType]:
        return self._put_full_update(ProductType, "/products", object_id, data)

    # ------------------------------------------------------------------
    # Product (endpoint: /product_items)
    # ------------------------------------------------------------------

    def get_product(self, object_id: int) -> Optional[Product]:
        return self._get_object(Product, "/product_items", object_id)

    def get_product_list(self) -> List[Product]:
        return self._get_object_list(Product, "/product_items/")

    def create_product(self, data: Dict[str, Any]) -> Optional[Product]:
        response_data = self._make_request("/product_items/", method="POST", data=data)
        if response_data:
            obj = Product(response_data, self)
            self._cache.set(Product, obj.id, obj)
            return obj
        return None

    def update_product(self, object_id: int, data: Dict[str, Any]) -> Optional[Product]:
        return self._put_full_update(Product, "/product_items", object_id, data)

    # ------------------------------------------------------------------
    # ProductPrice (endpoint: /product_prices)
    # ------------------------------------------------------------------

    def get_product_price(self, object_id: int) -> Optional[ProductPrice]:
        return self._get_object(ProductPrice, "/product_prices", object_id)

    def get_product_price_list(self) -> List[ProductPrice]:
        return self._get_object_list(ProductPrice, "/product_prices/")

    def create_product_price(self, data: Dict[str, Any]) -> Optional[ProductPrice]:
        response_data = self._make_request("/product_prices/", method="POST", data=data)
        if response_data:
            obj = ProductPrice(response_data, self)
            self._cache.set(ProductPrice, obj.id, obj)
            return obj
        return None

    def update_product_price(self, object_id: int, data: Dict[str, Any]) -> Optional[ProductPrice]:
        return self._put_full_update(ProductPrice, "/product_prices", object_id, data)

    # ------------------------------------------------------------------
    # CurrencyTransform (endpoint: /currency_transforms)
    # ------------------------------------------------------------------

    def get_currency_transform(self, object_id: int) -> Optional[CurrencyTransform]:
        return self._get_object(CurrencyTransform, "/currency_transforms", object_id)

    def get_currency_transform_list(self) -> List[CurrencyTransform]:
        return self._get_object_list(CurrencyTransform, "/currency_transforms/")

    def create_currency_transform(self, data: Dict[str, Any]) -> Optional[CurrencyTransform]:
        response_data = self._make_request("/currency_transforms/", method="POST", data=data)
        if response_data:
            obj = CurrencyTransform(response_data, self)
            self._cache.set(CurrencyTransform, obj.id, obj)
            return obj
        return None

    def update_currency_transform(self, object_id: int, data: Dict[str, Any]) -> Optional[CurrencyTransform]:
        return self._put_full_update(CurrencyTransform, "/currency_transforms", object_id, data)

    # ------------------------------------------------------------------
    # UnitTransform (endpoint: /unit_transforms)
    # ------------------------------------------------------------------

    def get_unit_transform(self, object_id: int) -> Optional[UnitTransform]:
        return self._get_object(UnitTransform, "/unit_transforms", object_id)

    def get_unit_transform_list(self) -> List[UnitTransform]:
        return self._get_object_list(UnitTransform, "/unit_transforms/")

    def create_unit_transform(self, data: Dict[str, Any]) -> Optional[UnitTransform]:
        response_data = self._make_request("/unit_transforms/", method="POST", data=data)
        if response_data:
            obj = UnitTransform(response_data, self)
            self._cache.set(UnitTransform, obj.id, obj)
            return obj
        return None

    def update_unit_transform(self, object_id: int, data: Dict[str, Any]) -> Optional[UnitTransform]:
        return self._put_full_update(UnitTransform, "/unit_transforms", object_id, data)

    # ------------------------------------------------------------------
    # CustomerGroupTransform (endpoint: /customer_group_transforms)
    # ------------------------------------------------------------------

    def get_customer_group_transform(self, object_id: int) -> Optional[CustomerGroupTransform]:
        return self._get_object(CustomerGroupTransform, "/customer_group_transforms", object_id)

    def get_customer_group_transform_list(self) -> List[CustomerGroupTransform]:
        return self._get_object_list(CustomerGroupTransform, "/customer_group_transforms/")

    def create_customer_group_transform(self, data: Dict[str, Any]) -> Optional[CustomerGroupTransform]:
        response_data = self._make_request("/customer_group_transforms/", method="POST", data=data)
        if response_data:
            obj = CustomerGroupTransform(response_data, self)
            self._cache.set(CustomerGroupTransform, obj.id, obj)
            return obj
        return None

    def update_customer_group_transform(self, object_id: int, data: Dict[str, Any]) -> Optional[CustomerGroupTransform]:
        return self._put_full_update(CustomerGroupTransform, "/customer_group_transforms", object_id, data)
