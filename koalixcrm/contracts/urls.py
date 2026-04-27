"""Per-app REST API routes for koalixcrm Contracts.

Mounted at ``/koalixcrm_contracts/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.
"""
from rest_framework.routers import DefaultRouter

# CR-002 §2.1 note: commercial_document_media currently lives under
# contracts.views; keep it in the Contracts router (§2.1 default recommendation).
from koalixcrm.contracts.views.commercial_document_media_view_set import (
    CommercialDocumentMediaViewSet,
)
from koalixcrm.contracts_api_py.contracts_api import (
    CommercialDocumentPositionViewSet,
    ContractViewSet,
    CreditNoteViewSet,
    DespatchAdviceViewSet,
    InvoiceViewSet,
    PaymentReminderViewSet,
    PurchaseOrderViewSet,
    QuotationViewSet,
    SalesOrderViewSet,
)

router = DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'quotations', QuotationViewSet, basename='quotation')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'sales-orders', SalesOrderViewSet, basename='sales-order')
router.register(r'despatch-advices', DespatchAdviceViewSet, basename='despatch-advice')
router.register(r'payment-reminders', PaymentReminderViewSet, basename='payment-reminder')
router.register(r'commercial-document-positions', CommercialDocumentPositionViewSet, basename='commercial-document-position')
router.register(r'commercial-document-media', CommercialDocumentMediaViewSet, basename='commercial-document-media')
router.register(r'credit-notes', CreditNoteViewSet, basename='credit-note')

urlpatterns = router.urls
