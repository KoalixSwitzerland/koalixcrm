# -*- coding: utf-8 -*-
from .attribute_definition_view_set import AttributeDefinitionViewSet
from .attribute_group_view_set import AttributeGroupViewSet
from .attribute_set_default_view_set import AttributeSetDefaultViewSet
from .attribute_set_view_sets import AttributeSetGroupViewSet, AttributeSetViewSet
from .attribute_validation_rule_view_set import AttributeValidationRuleViewSet
from .classification_view_sets import ClassificationNodeViewSet, ClassificationViewSet
from .product_attribute_mapping_view_set import ProductAttributeMappingViewSet
from .product_attribute_mirror_view_set import ProductAttributeMirrorViewSet
from .product_attribute_value_view_sets import (
    ProductAttributeBoolViewSet,
    ProductAttributeDecimalViewSet,
    ProductAttributeEnumViewSet,
    ProductAttributeIntViewSet,
    ProductAttributeReferenceViewSet,
    ProductAttributeStringViewSet,
)
from .product_classification_view_set import ProductClassificationViewSet
from .product_view_set import ProductViewSet
from .bill_of_materials_view_set import BillOfMaterialsViewSet, BomItemViewSet
from .price_list_view_set import PriceListViewSet
from .product_passport_view_set import ProductPassportViewSet
from .product_supply_view_set import ProductSupplyViewSet
from .service_profile_view_set import ServiceProfileViewSet
from .unit_of_measure_conversion_view_set import UnitOfMeasureConversionViewSet

__all__ = [
    'ProductViewSet',
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
