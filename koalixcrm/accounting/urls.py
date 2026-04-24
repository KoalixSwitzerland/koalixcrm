"""Per-app REST API routes for koalixcrm Accounting.

Mounted at ``/koalixcrm_accounting/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from rest_framework.routers import DefaultRouter

from koalixcrm.accounting_api_py.accounting_api import (
    AccountViewSet,
    AccountingPeriodViewSet,
    BookingViewSet,
    ProductCategoryViewSet,
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'accounting-periods', AccountingPeriodViewSet, basename='accounting-period')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'product-categories', ProductCategoryViewSet, basename='product-category')

urlpatterns = router.urls
