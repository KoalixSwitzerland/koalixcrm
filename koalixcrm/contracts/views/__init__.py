# -*- coding: utf-8 -*-
from .contract_view_set import ContractViewSet
from .invoice_view_set import InvoiceViewSet
from .quotation_view_set import QuotationViewSet
from .purchase_order_view_set import PurchaseOrderViewSet
from .sales_order_view_set import SalesOrderViewSet
from .despatch_advice_view_set import DespatchAdviceViewSet
from .payment_reminder_view_set import PaymentReminderViewSet
from .commercial_document_position_view_set import CommercialDocumentPositionViewSet
from .credit_note_view_set import CreditNoteViewSet

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
