"""Per-app REST API routes for koalixcrm Products.

Mounted at ``/koalixcrm_products/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from koalixcrm.products_api_py.products_api import (
    AttributeDefinitionViewSet,
    AttributeGroupViewSet,
    AttributeSetDefaultViewSet,
    AttributeSetGroupViewSet,
    AttributeSetViewSet,
    AttributeValidationRuleViewSet,
    BillOfMaterialsViewSet,
    BomItemViewSet,
    ClassificationNodeViewSet,
    ClassificationViewSet,
    CustomerGroupTransformViewSet,
    PriceListViewSet,
    ProductAttributeBoolViewSet,
    ProductAttributeDecimalViewSet,
    ProductAttributeEnumViewSet,
    ProductAttributeIntViewSet,
    ProductAttributeMappingViewSet,
    ProductAttributeMirrorViewSet,
    ProductAttributeReferenceViewSet,
    ProductAttributeStringViewSet,
    ProductClassificationViewSet,
    ProductFamilyViewSet,
    ProductMediaViewSet,
    ProductPassportViewSet,
    ProductPriceViewSet,
    ProductSupplyViewSet,
    ProductTranslationViewSet,
    ProductVariantViewSet,
    ProductViewSet,
    ServiceProfileViewSet,
    UnitOfMeasureConversionViewSet,
)

router = DefaultRouter()
# ADR-0003 Amendment 2026-06-27 (v2.0.0 breaking cut): `producttype` ->
# `product` resource rename. `products` now maps to `ProductViewSet`
# (backed by the renamed `Product` model, formerly `ProductType`). The
# former `/product-items` endpoint (backed by the removed identifier-hull
# `Product` model) is retired; its identification role is carried by
# `ProductVariant` (`/product-variants`) per ADR-0021.
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-families', ProductFamilyViewSet, basename='product-family')
router.register(r'product-variants', ProductVariantViewSet, basename='product-variant')
router.register(r'product-translations', ProductTranslationViewSet, basename='product-translation')
router.register(r'product-media', ProductMediaViewSet, basename='product-media')
router.register(r'product-prices', ProductPriceViewSet, basename='product-price')
router.register(r'customer-group-transforms', CustomerGroupTransformViewSet, basename='customer-group-transform')

# ADR-0004 / ADR-0018 / ADR-0019 / ADR-0020 (Stage 2): classification,
# extensible attributes, canonical vocabulary support, and declarative
# validation rules.
router.register(r'classifications', ClassificationViewSet, basename='classification')
router.register(r'classification-nodes', ClassificationNodeViewSet, basename='classification-node')
router.register(r'product-classifications', ProductClassificationViewSet, basename='product-classification')
router.register(r'attribute-groups', AttributeGroupViewSet, basename='attribute-group')
router.register(r'attribute-definitions', AttributeDefinitionViewSet, basename='attribute-definition')
router.register(r'attribute-sets', AttributeSetViewSet, basename='attribute-set')
router.register(r'attribute-set-groups', AttributeSetGroupViewSet, basename='attribute-set-group')
router.register(r'attribute-set-defaults', AttributeSetDefaultViewSet, basename='attribute-set-default')
router.register(r'attribute-validation-rules', AttributeValidationRuleViewSet, basename='attribute-validation-rule')
router.register(r'product-attribute-mappings', ProductAttributeMappingViewSet, basename='product-attribute-mapping')
router.register(r'product-attribute-mirrors', ProductAttributeMirrorViewSet, basename='product-attribute-mirror')
router.register(r'product-attribute-strings', ProductAttributeStringViewSet, basename='product-attribute-string')
router.register(r'product-attribute-ints', ProductAttributeIntViewSet, basename='product-attribute-int')
router.register(r'product-attribute-decimals', ProductAttributeDecimalViewSet, basename='product-attribute-decimal')
router.register(r'product-attribute-bools', ProductAttributeBoolViewSet, basename='product-attribute-bool')
router.register(r'product-attribute-enums', ProductAttributeEnumViewSet, basename='product-attribute-enum')
router.register(
    r'product-attribute-references', ProductAttributeReferenceViewSet, basename='product-attribute-reference'
)

# Stage 3 (ADR-0005/0006/0007/0008): pricing/UoM, sourcing/BOM, service
# profile, DPP placeholder.
router.register(r'price-lists', PriceListViewSet, basename='price-list')
router.register(r'uom-conversions', UnitOfMeasureConversionViewSet, basename='uom-conversion')
router.register(r'product-supplies', ProductSupplyViewSet, basename='product-supply')
router.register(r'bills-of-materials', BillOfMaterialsViewSet, basename='bill-of-materials')
router.register(r'bom-items', BomItemViewSet, basename='bom-item')
router.register(r'service-profiles', ServiceProfileViewSet, basename='service-profile')
router.register(r'product-passports', ProductPassportViewSet, basename='product-passport')

urlpatterns = router.urls
