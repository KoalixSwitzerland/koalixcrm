"""Per-app REST API routes for koalixcrm Products.

Mounted at ``/koalixcrm_products/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from rest_framework.routers import DefaultRouter

from koalixcrm.products_api_py.products_api import (
    ProductTypeViewSet,
    ProductViewSet,
    ProductPriceViewSet,
    CustomerGroupTransformViewSet,
)

router = DefaultRouter()
# `products` historically pointed at ProductTypeViewSet (flat router kept it
# that way for backwards compat); the kebab-case rename keeps the same
# mapping — no semantic change, only casing.
router.register(r'products', ProductTypeViewSet, basename='product')
router.register(r'product-items', ProductViewSet, basename='product-item')
router.register(r'product-prices', ProductPriceViewSet, basename='product-price')
router.register(r'customer-group-transforms', CustomerGroupTransformViewSet, basename='customer-group-transform')

urlpatterns = router.urls
