# -*- coding: utf-8 -*-
"""
Contract Object Management API entry point.

Exposes Contract/Document REST viewsets for URL routing.
"""
from koalixcrm.contracts.views.contract_view_set import ContractViewSet
from koalixcrm.contracts.views.invoice_view_set import InvoiceViewSet
from koalixcrm.contracts.views.quote_view_set import QuoteViewSet
from koalixcrm.contracts.views.purchase_order_view_set import PurchaseOrderViewSet
from koalixcrm.contracts.views.purchase_confirmation_view_set import PurchaseConfirmationViewSet
from koalixcrm.contracts.views.delivery_note_view_set import DeliveryNoteViewSet
from koalixcrm.contracts.views.payment_reminder_view_set import PaymentReminderViewSet
from koalixcrm.contracts.views.sales_document_position_view_set import SalesDocumentPositionViewSet

__all__ = [
    'ContractViewSet',
    'InvoiceViewSet',
    'QuoteViewSet',
    'PurchaseOrderViewSet',
    'PurchaseConfirmationViewSet',
    'DeliveryNoteViewSet',
    'PaymentReminderViewSet',
    'SalesDocumentPositionViewSet',
]
