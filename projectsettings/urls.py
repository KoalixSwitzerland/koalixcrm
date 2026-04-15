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
    ProductTypeViewSet, ProductViewSet, ProductPriceViewSet,
    CustomerGroupTransformViewSet,
)
from koalixcrm.settings_api_py.settings_api import (
    CurrencyViewSet, TaxViewSet, UnitViewSet,
    CurrencyTransformViewSet, UnitTransformViewSet,
)
from koalixcrm.contracts_api_py.contracts_api import (
    ContractViewSet, InvoiceViewSet, QuoteViewSet,
    PurchaseOrderViewSet, PurchaseConfirmationViewSet,
    DeliveryNoteViewSet, PaymentReminderViewSet,
    CommercialDocumentPositionViewSet,
    CreditNoteViewSet,
)
from koalixcrm.auth.oidc_views import (
    LoginSelectionView, OAuthLoginView, OAuthCallbackView, MultiProviderLogoutView,
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
router.register(r'accounting_periods', AccountingPeriodViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'product_categories', ProductCategoryViewSet)
# CRM (contacts)
router.register(r'customers', CustomerViewSet)
router.register(r'customer_billing_cycles', CustomerBillingCycleViewSet)
router.register(r'contact_postal_addresses', ContactPostalAddressViewSet)
router.register(r'contact_phone_numbers', ContactPhoneAddressViewSet)
router.register(r'contact_email_addresses', ContactEmailAddressViewSet)
router.register(r'customer_groups', CustomerGroupViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'contacts', ContactViewSet)
# Settings (shared value objects)
router.register(r'currencies', CurrencyViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'units', UnitViewSet)
router.register(r'currency_transforms', CurrencyTransformViewSet)
router.register(r'unit_transforms', UnitTransformViewSet)
# Products
router.register(r'products', ProductTypeViewSet)
router.register(r'product_items', ProductViewSet)
router.register(r'product_prices', ProductPriceViewSet)
router.register(r'customer_group_transforms', CustomerGroupTransformViewSet)
# Contract Object Management
router.register(r'contracts', ContractViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'quotes', QuoteViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)
router.register(r'purchase_confirmations', PurchaseConfirmationViewSet)
router.register(r'delivery_notes', DeliveryNoteViewSet)
router.register(r'payment_reminders', PaymentReminderViewSet)
router.register(r'commercial_document_positions', CommercialDocumentPositionViewSet)
router.register(r'credit_notes', CreditNoteViewSet)
# Reporting
router.register(r'projects', ProjectViewSet)
router.register(r'project_status', ProjectStatusViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task_status', TaskStatusViewSet)
router.register(r'agreements', AgreementViewSet)
router.register(r'works', WorkViewSet)
router.register(r'estimations', EstimationViewSet)
router.register(r'estimation_status', EstimationStatusViewSet)
router.register(r'human_resources', HumanResourceViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'resource_types', ResourceTypeViewSet)
router.register(r'resource_managers', ResourceManagerViewSet)
router.register(r'resource_prices', ResourcePriceViewSet)
router.register(r'reporting_periods', ReportingPeriodViewSet)
router.register(r'reporting_period_status', ReportingPeriodStatusViewSet)
router.register(r'agreement_status', AgreementStatusViewSet)
router.register(r'agreement_types', AgreementTypeViewSet)
router.register(r'project_link_types', ProjectLinkTypeViewSet)
router.register(r'task_link_types', TaskLinkTypeViewSet)
router.register(r'generic_project_links', GenericProjectLinkViewSet)
router.register(r'generic_task_links', GenericTaskLinkViewSet)

admin.autodiscover()
# Override Django admin login to redirect to OIDC
admin.site.login = LoginSelectionView.as_view()

urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),
    path('', include(router.urls)),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('koalixcrm/crm/reporting/', include('koalixcrm.crm.reporting.urls')),
    # OIDC auth (admin login via Keycloak)
    path('auth/login/', LoginSelectionView.as_view(), name='login-selection'),
    path('auth/login/<str:provider>/', OAuthLoginView.as_view(), name='oauth-login'),
    path('auth/callback/<str:provider>/', OAuthCallbackView.as_view(), name='oauth-callback'),
    path('auth/logout/', MultiProviderLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
