# -*- coding: utf-8 -*-
"""
ProductAdmin for koalixcrm products (ADR-0003 renamed `ProductType` ->
`Product`; see products migration 0007).
"""
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.core.admin.currency_transform_admin import CurrencyTransformInlineAdmin
from koalixcrm.core.admin.unit_transform_admin import UnitTransformInlineAdmin
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.products.admin.customer_group_transform_admin import (
    CustomerGroupTransformInlineAdmin,
)
from koalixcrm.products.admin.product_attribute_value_admin import (
    ProductAttributeBoolInlineAdmin,
    ProductAttributeDecimalInlineAdmin,
    ProductAttributeEnumInlineAdmin,
    ProductAttributeIntInlineAdmin,
    ProductAttributeReferenceInlineAdmin,
    ProductAttributeStringInlineAdmin,
)
from koalixcrm.products.admin.product_classification_admin import (
    ProductClassificationInlineAdmin,
)
from koalixcrm.products.admin.bill_of_materials_admin import BillOfMaterialsInlineAdmin
from koalixcrm.products.admin.product_media_admin import ProductMediaInlineAdmin
from koalixcrm.products.admin.product_passport_admin import ProductPassportInlineAdmin
from koalixcrm.products.admin.product_supply_admin import ProductSupplyInlineAdmin
from koalixcrm.products.admin.product_translation_admin import (
    ProductTranslationInlineAdmin,
)
from koalixcrm.products.admin.product_variant_admin import ProductVariantInlineAdmin
from koalixcrm.products.admin.service_profile_admin import ServiceProfileInlineAdmin
from koalixcrm.products.admin.unit_of_measure_conversion_admin import (
    UnitOfMeasureConversionInlineAdmin,
)
from koalixcrm.products.models.product import Product


@admin.register(Product)
class ProductAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = (
        'product_type_identifier',
        'title',
        'kind',
        'lifecycle_status',
        'base_uom',
        'tax_class',
        'brand',
        'product_family')
    list_display_links = ('product_type_identifier',)
    list_filter = ('workspace', 'kind', 'lifecycle_status')
    search_fields = ('product_type_identifier', 'title', 'brand')
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'product_type_identifier',
                'title',
                'description',
                'kind',
                'lifecycle_status',
                'base_uom',
                'tax_class',
                'product_family')
        }),
        (_('Manufacturer'), {
            'fields': (
                'brand',
                'manufacturer_party',
                'country_of_origin')
        }),
    )
    inlines = [ProductVariantInlineAdmin,
               ProductTranslationInlineAdmin,
               ProductMediaInlineAdmin,
               UnitTransformInlineAdmin,
               CurrencyTransformInlineAdmin,
               CustomerGroupTransformInlineAdmin,
               ProductClassificationInlineAdmin,
               ProductAttributeStringInlineAdmin,
               ProductAttributeIntInlineAdmin,
               ProductAttributeDecimalInlineAdmin,
               ProductAttributeBoolInlineAdmin,
               ProductAttributeEnumInlineAdmin,
               ProductAttributeReferenceInlineAdmin,
               UnitOfMeasureConversionInlineAdmin,
               ProductSupplyInlineAdmin,
               BillOfMaterialsInlineAdmin,
               ServiceProfileInlineAdmin,
               ProductPassportInlineAdmin]
