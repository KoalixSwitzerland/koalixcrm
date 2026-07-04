# -*- coding: utf-8 -*-
"""
Products API entry point.

Exposes Products REST viewsets for URL routing.
"""

from __future__ import annotations

from koalixcrm.products.views.attribute_definition_view_set import (
    AttributeDefinitionViewSet,
)
from koalixcrm.products.views.attribute_group_view_set import AttributeGroupViewSet
from koalixcrm.products.views.attribute_set_default_view_set import (
    AttributeSetDefaultViewSet,
)
from koalixcrm.products.views.attribute_set_view_sets import (
    AttributeSetGroupViewSet,
    AttributeSetViewSet,
)
from koalixcrm.products.views.attribute_validation_rule_view_set import (
    AttributeValidationRuleViewSet,
)
from koalixcrm.products.views.classification_view_sets import (
    ClassificationNodeViewSet,
    ClassificationViewSet,
)
from koalixcrm.products.views.customer_group_transform_view_set import (
    CustomerGroupTransformViewSet,
)
from koalixcrm.products.views.product_attribute_mapping_view_set import (
    ProductAttributeMappingViewSet,
)
from koalixcrm.products.views.product_attribute_mirror_view_set import (
    ProductAttributeMirrorViewSet,
)
from koalixcrm.products.views.product_attribute_value_view_sets import (
    ProductAttributeBoolViewSet,
    ProductAttributeDecimalViewSet,
    ProductAttributeEnumViewSet,
    ProductAttributeIntViewSet,
    ProductAttributeReferenceViewSet,
    ProductAttributeStringViewSet,
)
from koalixcrm.products.views.product_classification_view_set import (
    ProductClassificationViewSet,
)
from koalixcrm.products.views.product_family_view_set import ProductFamilyViewSet
from koalixcrm.products.views.product_media_view_set import ProductMediaViewSet
from koalixcrm.products.views.product_price_view_set import ProductPriceViewSet
from koalixcrm.products.views.product_translation_view_set import (
    ProductTranslationViewSet,
)
from koalixcrm.products.views.product_variant_view_set import ProductVariantViewSet
from koalixcrm.products.views.product_view_set import ProductViewSet
from koalixcrm.products.views.bill_of_materials_view_set import (
    BillOfMaterialsViewSet,
    BomItemViewSet,
)
from koalixcrm.products.views.price_list_view_set import PriceListViewSet
from koalixcrm.products.views.product_passport_view_set import ProductPassportViewSet
from koalixcrm.products.views.product_supply_view_set import ProductSupplyViewSet
from koalixcrm.products.views.service_profile_view_set import ServiceProfileViewSet
from koalixcrm.products.views.unit_of_measure_conversion_view_set import (
    UnitOfMeasureConversionViewSet,
)

__all__ = [
    'ProductViewSet',
    'ProductFamilyViewSet',
    'ProductVariantViewSet',
    'ProductTranslationViewSet',
    'ProductMediaViewSet',
    'ProductPriceViewSet',
    'CustomerGroupTransformViewSet',
    'ClassificationViewSet',
    'ClassificationNodeViewSet',
    'ProductClassificationViewSet',
    'AttributeGroupViewSet',
    'AttributeDefinitionViewSet',
    'AttributeSetViewSet',
    'AttributeSetGroupViewSet',
    'AttributeSetDefaultViewSet',
    'ProductAttributeMappingViewSet',
    'ProductAttributeMirrorViewSet',
    'AttributeValidationRuleViewSet',
    'ProductAttributeStringViewSet',
    'ProductAttributeIntViewSet',
    'ProductAttributeDecimalViewSet',
    'ProductAttributeBoolViewSet',
    'ProductAttributeEnumViewSet',
    'ProductAttributeReferenceViewSet',
    'PriceListViewSet',
    'UnitOfMeasureConversionViewSet',
    'ProductSupplyViewSet',
    'BillOfMaterialsViewSet',
    'BomItemViewSet',
    'ServiceProfileViewSet',
    'ProductPassportViewSet',
]
