"""koalixcrm URL Configuration"""

from django.urls import path, include
from django.conf.urls.static import *
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.shortcuts import redirect
from filebrowser.sites import site
from rest_framework import routers

from accounting_api import (
    AccountAsJSON, AccountingPeriodAsJSON, BookingAsJSON, ProductCategoryAsJSON,
)
from crm_api import (
    CustomerViewSet, CustomerGroupViewSet, CustomerBillingCycleViewSet,
    ContactPostalAddressViewSet, ContactEmailAddressViewSet, ContactPhoneAddressViewSet,
)
from products_api import (
    CurrencyViewSet, TaxViewSet, UnitViewSet, ProductTypeViewSet,
)
from contract_object_management_api import (
    ContractViewSet,
)
from reporting_api import (
    TaskViewSet, TaskStatusViewSet, ProjectViewSet, ProjectStatusViewSet, AgreementViewSet,
)

router = routers.DefaultRouter()
# Accounting
router.register(r'accounts', AccountAsJSON)
router.register(r'accountingPeriods', AccountingPeriodAsJSON)
router.register(r'bookings', BookingAsJSON)
router.register(r'productCategories', ProductCategoryAsJSON)
# CRM (contacts)
router.register(r'customers', CustomerViewSet)
router.register(r'customerBillingCycles', CustomerBillingCycleViewSet)
router.register(r'contactPostalAddresses', ContactPostalAddressViewSet)
router.register(r'contactPhoneNumbers', ContactPhoneAddressViewSet)
router.register(r'contactEmailAddresses', ContactEmailAddressViewSet)
router.register(r'customerGroups', CustomerGroupViewSet)
# Products
router.register(r'currencies', CurrencyViewSet)
router.register(r'products', ProductTypeViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'units', UnitViewSet)
# Contract Object Management
router.register(r'contracts', ContractViewSet)
# Reporting
router.register(r'projects', ProjectViewSet)
router.register(r'projectStatus', ProjectStatusViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'taskstatus', TaskStatusViewSet)
router.register(r'agreements', AgreementViewSet)

admin.autodiscover()

urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),
    path('', include(router.urls)),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('koalixcrm/crm/reporting/', include('koalixcrm.crm.reporting.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
