# -*- coding: utf-8 -*-
"""KoalixCRM Products API Client"""

from __future__ import annotations

from typing import Any

from koalixcrm.products_api_py.dto.customer_group_transform import (
    CustomerGroupTransform,
)
from koalixcrm.products_api_py.dto.product import Product
from koalixcrm.products_api_py.dto.product_family import ProductFamily
from koalixcrm.products_api_py.dto.product_media import ProductMedia
from koalixcrm.products_api_py.dto.product_price import ProductPrice
from koalixcrm.products_api_py.dto.product_translation import ProductTranslation
from koalixcrm.products_api_py.dto.product_variant import ProductVariant
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
    # Product (endpoint: /products) — renamed from ProductType,
    # ADR-0003 Amendment 2026-06-27.
    # ------------------------------------------------------------------

    def get_product_type(self, object_id: int) -> Product | None:
        return self._get_object(Product, "/products", object_id)

    def get_product_type_list(self) -> list[Product]:
        return self._get_object_list(Product, "/products/")

    def create_product_type(self, data: dict[str, Any]) -> Product | None:
        response_data = self._make_request("/products/", method="POST", data=data)
        if response_data:
            obj = Product(response_data, self)
            self._cache.set(Product, obj.id, obj)
            return obj
        return None

    def update_product_type(self, object_id: int, data: dict[str, Any]) -> Product | None:
        return self._put_full_update(Product, "/products", object_id, data)

    # ------------------------------------------------------------------
    # ProductFamily (endpoint: /product-families)
    # ------------------------------------------------------------------

    def get_product_family(self, object_id: int) -> ProductFamily | None:
        return self._get_object(ProductFamily, "/product-families", object_id)

    def get_product_family_list(self) -> list[ProductFamily]:
        return self._get_object_list(ProductFamily, "/product-families/")

    def create_product_family(self, data: dict[str, Any]) -> ProductFamily | None:
        response_data = self._make_request("/product-families/", method="POST", data=data)
        if response_data:
            obj = ProductFamily(response_data, self)
            self._cache.set(ProductFamily, obj.id, obj)
            return obj
        return None

    def update_product_family(self, object_id: int, data: dict[str, Any]) -> ProductFamily | None:
        return self._put_full_update(ProductFamily, "/product-families", object_id, data)

    # ------------------------------------------------------------------
    # ProductVariant (endpoint: /product-variants) — carries the
    # identification role formerly held by the (now removed) hollow
    # `Product` model.
    # ------------------------------------------------------------------

    def get_product_variant(self, object_id: int) -> ProductVariant | None:
        return self._get_object(ProductVariant, "/product-variants", object_id)

    def get_product_variant_list(self) -> list[ProductVariant]:
        return self._get_object_list(ProductVariant, "/product-variants/")

    def create_product_variant(self, data: dict[str, Any]) -> ProductVariant | None:
        response_data = self._make_request("/product-variants/", method="POST", data=data)
        if response_data:
            obj = ProductVariant(response_data, self)
            self._cache.set(ProductVariant, obj.id, obj)
            return obj
        return None

    def update_product_variant(self, object_id: int, data: dict[str, Any]) -> ProductVariant | None:
        return self._put_full_update(ProductVariant, "/product-variants", object_id, data)

    # ------------------------------------------------------------------
    # ProductTranslation (endpoint: /product-translations)
    # ------------------------------------------------------------------

    def get_product_translation(self, object_id: int) -> ProductTranslation | None:
        return self._get_object(ProductTranslation, "/product-translations", object_id)

    def get_product_translation_list(self) -> list[ProductTranslation]:
        return self._get_object_list(ProductTranslation, "/product-translations/")

    def create_product_translation(self, data: dict[str, Any]) -> ProductTranslation | None:
        response_data = self._make_request("/product-translations/", method="POST", data=data)
        if response_data:
            obj = ProductTranslation(response_data, self)
            self._cache.set(ProductTranslation, obj.id, obj)
            return obj
        return None

    def update_product_translation(self, object_id: int, data: dict[str, Any]) -> ProductTranslation | None:
        return self._put_full_update(ProductTranslation, "/product-translations", object_id, data)

    # ------------------------------------------------------------------
    # ProductMedia (endpoint: /product-media)
    # ------------------------------------------------------------------

    def get_product_media(self, object_id: int) -> ProductMedia | None:
        return self._get_object(ProductMedia, "/product-media", object_id)

    def get_product_media_list(self) -> list[ProductMedia]:
        return self._get_object_list(ProductMedia, "/product-media/")

    def create_product_media(self, data: dict[str, Any]) -> ProductMedia | None:
        response_data = self._make_request("/product-media/", method="POST", data=data)
        if response_data:
            obj = ProductMedia(response_data, self)
            self._cache.set(ProductMedia, obj.id, obj)
            return obj
        return None

    def update_product_media(self, object_id: int, data: dict[str, Any]) -> ProductMedia | None:
        return self._put_full_update(ProductMedia, "/product-media", object_id, data)

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
