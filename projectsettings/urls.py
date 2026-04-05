"""koalixcrm URL Configuration"""

from django.urls import path, include
from django.conf.urls.static import *
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.shortcuts import redirect
from filebrowser.sites import site
from rest_framework import routers

from koalixcrm.accounting_api_py.accounting_api import (
    AccountViewSet, AccountingPeriodViewSet, BookingViewSet, ProductCategoryViewSet,
)
from koalixcrm.crm_api_py.crm_api import (
    CustomerViewSet, CustomerGroupViewSet, CustomerBillingCycleViewSet,
    ContactPostalAddressViewSet, ContactEmailAddressViewSet, ContactPhoneAddressViewSet,
    SupplierViewSet, PersonViewSet, ContactViewSet,
)
from koalixcrm.products_api_py.products_api import (
    CurrencyViewSet, TaxViewSet, UnitViewSet, ProductTypeViewSet,
    ProductViewSet, ProductPriceViewSet, CurrencyTransformViewSet,
    UnitTransformViewSet, CustomerGroupTransformViewSet,
)
from koalixcrm.contracts_api_py.contracts_api import (
    ContractViewSet, InvoiceViewSet, QuoteViewSet,
    PurchaseOrderViewSet, PurchaseConfirmationViewSet,
    DeliveryNoteViewSet, PaymentReminderViewSet,
    SalesDocumentPositionViewSet,
)
from koalixcrm.reporting_api_py.reporting_api import (
    TaskViewSet, TaskStatusViewSet, ProjectViewSet, ProjectStatusViewSet, AgreementViewSet,
    WorkViewSet, EstimationViewSet, EstimationStatusViewSet,
    HumanResourceViewSet, ResourceViewSet, ResourceTypeViewSet,
    ResourceManagerViewSet, ResourcePriceViewSet,
    ReportingPeriodViewSet, ReportingPeriodStatusViewSet,
    AgreementStatusViewSet, AgreementTypeViewSet,
    ProjectLinkTypeViewSet, TaskLinkTypeViewSet,
    GenericProjectLinkViewSet, GenericTaskLinkViewSet,
)

router = routers.DefaultRouter()
# Accounting
router.register(r'accounts', AccountViewSet)
router.register(r'accountingPeriods', AccountingPeriodViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'productCategories', ProductCategoryViewSet)
# CRM (contacts)
router.register(r'customers', CustomerViewSet)
router.register(r'customerBillingCycles', CustomerBillingCycleViewSet)
router.register(r'contactPostalAddresses', ContactPostalAddressViewSet)
router.register(r'contactPhoneNumbers', ContactPhoneAddressViewSet)
router.register(r'contactEmailAddresses', ContactEmailAddressViewSet)
router.register(r'customerGroups', CustomerGroupViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'contacts', ContactViewSet)
# Products
router.register(r'currencies', CurrencyViewSet)
router.register(r'products', ProductTypeViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'units', UnitViewSet)
router.register(r'productItems', ProductViewSet)
router.register(r'productPrices', ProductPriceViewSet)
router.register(r'currencyTransforms', CurrencyTransformViewSet)
router.register(r'unitTransforms', UnitTransformViewSet)
router.register(r'customerGroupTransforms', CustomerGroupTransformViewSet)
# Contract Object Management
router.register(r'contracts', ContractViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'quotes', QuoteViewSet)
router.register(r'purchaseOrders', PurchaseOrderViewSet)
router.register(r'purchaseConfirmations', PurchaseConfirmationViewSet)
router.register(r'deliveryNotes', DeliveryNoteViewSet)
router.register(r'paymentReminders', PaymentReminderViewSet)
router.register(r'salesDocumentPositions', SalesDocumentPositionViewSet)
# Reporting
router.register(r'projects', ProjectViewSet)
router.register(r'projectStatus', ProjectStatusViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'taskstatus', TaskStatusViewSet)
router.register(r'agreements', AgreementViewSet)
router.register(r'works', WorkViewSet)
router.register(r'estimations', EstimationViewSet)
router.register(r'estimationStatus', EstimationStatusViewSet)
router.register(r'humanResources', HumanResourceViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'resourceTypes', ResourceTypeViewSet)
router.register(r'resourceManagers', ResourceManagerViewSet)
router.register(r'resourcePrices', ResourcePriceViewSet)
router.register(r'reportingPeriods', ReportingPeriodViewSet)
router.register(r'reportingPeriodStatus', ReportingPeriodStatusViewSet)
router.register(r'agreementStatus', AgreementStatusViewSet)
router.register(r'agreementTypes', AgreementTypeViewSet)
router.register(r'projectLinkTypes', ProjectLinkTypeViewSet)
router.register(r'taskLinkTypes', TaskLinkTypeViewSet)
router.register(r'genericProjectLinks', GenericProjectLinkViewSet)
router.register(r'genericTaskLinks', GenericTaskLinkViewSet)

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
