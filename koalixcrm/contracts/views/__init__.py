# -*- coding: utf-8 -*-
from .commercial_document_position_view_set import CommercialDocumentPositionViewSet
from .contract_view_set import ContractViewSet
from .credit_note_view_set import CreditNoteViewSet
from .despatch_advice_view_set import DespatchAdviceViewSet
from .invoice_view_set import InvoiceViewSet
from .payment_reminder_view_set import PaymentReminderViewSet
from .purchase_order_view_set import PurchaseOrderViewSet
from .quotation_view_set import QuotationViewSet
from .sales_order_view_set import SalesOrderViewSet

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
