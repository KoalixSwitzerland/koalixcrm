# -*- coding: utf-8 -*-
"""KoalixCRM Products API Client"""

from __future__ import annotations

from typing import Any

from koalixcrm.products_api_py.dto.customer_group_transform import (
    CustomerGroupTransform,
)
from koalixcrm.products_api_py.dto.product import Product
from koalixcrm.products_api_py.dto.product_price import ProductPrice
from koalixcrm.products_api_py.dto.product_type import ProductType
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMProductsAPIClient(BaseAPIClient):
    api_path_env_var = "KOALIXCRM_PRODUCTS_API_PATH"
    api_path_default = "/koalixcrm_products/api/v1/"
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
    # ProductType (endpoint: /products)
    # ------------------------------------------------------------------

    def get_product_type(self, object_id: int) -> ProductType | None:
        return self._get_object(ProductType, "/products", object_id)

    def get_product_type_list(self) -> list[ProductType]:
        return self._get_object_list(ProductType, "/products/")

    def create_product_type(self, data: dict[str, Any]) -> ProductType | None:
        response_data = self._make_request("/products/", method="POST", data=data)
        if response_data:
            obj = ProductType(response_data, self)
            self._cache.set(ProductType, obj.id, obj)
            return obj
        return None

    def update_product_type(self, object_id: int, data: dict[str, Any]) -> ProductType | None:
        return self._put_full_update(ProductType, "/products", object_id, data)

    # ------------------------------------------------------------------
    # Product (endpoint: /product_items)
    # ------------------------------------------------------------------

    def get_product(self, object_id: int) -> Product | None:
        return self._get_object(Product, "/product-items", object_id)

    def get_product_list(self) -> list[Product]:
        return self._get_object_list(Product, "/product-items/")

    def create_product(self, data: dict[str, Any]) -> Product | None:
        response_data = self._make_request("/product-items/", method="POST", data=data)
        if response_data:
            obj = Product(response_data, self)
            self._cache.set(Product, obj.id, obj)
            return obj
        return None

    def update_product(self, object_id: int, data: dict[str, Any]) -> Product | None:
        return self._put_full_update(Product, "/product-items", object_id, data)

    # ------------------------------------------------------------------
    # ProductPrice (endpoint: /product_prices)
    # ------------------------------------------------------------------

    def get_product_price(self, object_id: int) -> ProductPrice | None:
        return self._get_object(ProductPrice, "/product-prices", object_id)

    def get_product_price_list(self) -> list[ProductPrice]:
        return self._get_object_list(ProductPrice, "/product-prices/")

    def create_product_price(self, data: dict[str, Any]) -> ProductPrice | None:
        response_data = self._make_request("/product-prices/", method="POST", data=data)
        if response_data:
            obj = ProductPrice(response_data, self)
            self._cache.set(ProductPrice, obj.id, obj)
            return obj
        return None

    def update_product_price(self, object_id: int, data: dict[str, Any]) -> ProductPrice | None:
        return self._put_full_update(ProductPrice, "/product-prices", object_id, data)

    # ------------------------------------------------------------------
    # CustomerGroupTransform (endpoint: /customer_group_transforms)
    # ------------------------------------------------------------------

    def get_customer_group_transform(self, object_id: int) -> CustomerGroupTransform | None:
        return self._get_object(CustomerGroupTransform, "/customer-group-transforms", object_id)

    def get_customer_group_transform_list(self) -> list[CustomerGroupTransform]:
        return self._get_object_list(CustomerGroupTransform, "/customer-group-transforms/")

    def create_customer_group_transform(self, data: dict[str, Any]) -> CustomerGroupTransform | None:
        response_data = self._make_request("/customer-group-transforms/", method="POST", data=data)
        if response_data:
            obj = CustomerGroupTransform(response_data, self)
            self._cache.set(CustomerGroupTransform, obj.id, obj)
            return obj
        return None

    def update_customer_group_transform(
        self, object_id: int, data: dict[str, Any]
    ) -> CustomerGroupTransform | None:
        return self._put_full_update(CustomerGroupTransform, "/customer-group-transforms", object_id, data)
