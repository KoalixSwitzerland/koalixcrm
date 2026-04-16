# -*- coding: utf-8 -*-
"""
Contract Object Management API entry point.

Exposes Contract/Document REST viewsets for URL routing.
"""
from koalixcrm.contracts.views.contract_view_set import ContractViewSet
from koalixcrm.contracts.views.invoice_view_set import InvoiceViewSet
from koalixcrm.contracts.views.quotation_view_set import QuotationViewSet
from koalixcrm.contracts.views.purchase_order_view_set import PurchaseOrderViewSet
from koalixcrm.contracts.views.sales_order_view_set import SalesOrderViewSet
from koalixcrm.contracts.views.despatch_advice_view_set import DespatchAdviceViewSet
from koalixcrm.contracts.views.payment_reminder_view_set import PaymentReminderViewSet
from koalixcrm.contracts.views.commercial_document_position_view_set import CommercialDocumentPositionViewSet
from koalixcrm.contracts.views.credit_note_view_set import CreditNoteViewSet

__all__ = [
    'ContractViewSet',
    'InvoiceViewSet',
    'QuotationViewSet',
    'PurchaseOrderViewSet',
    'SalesOrderViewSet',
    'DespatchAdviceViewSet',
    'PaymentReminderViewSet',
    'CommercialDocumentPositionViewSet',
    'CreditNoteViewSet',
]
