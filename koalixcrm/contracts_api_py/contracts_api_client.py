# -*- coding: utf-8 -*-
"""API client for the koalixcrm Contracts app."""
from typing import Any, Dict, List, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.contracts_api_py.dto.contract import Contract
from koalixcrm.contracts_api_py.dto.invoice import Invoice
from koalixcrm.contracts_api_py.dto.quotation import Quotation
from koalixcrm.contracts_api_py.dto.purchase_order import PurchaseOrder
from koalixcrm.contracts_api_py.dto.sales_order import SalesOrder
from koalixcrm.contracts_api_py.dto.despatch_advice import DespatchAdvice
from koalixcrm.contracts_api_py.dto.payment_reminder import PaymentReminder
from koalixcrm.contracts_api_py.dto.commercial_document_position import CommercialDocumentPosition
from koalixcrm.contracts_api_py.dto.credit_note import CreditNote


class KoalixCRMContractsAPIClient(BaseAPIClient):
    """API client for managing contracts, commercial documents, and related entities."""

    api_path_env_var = 'KOALIXCRM_CONTRACTS_API_PATH'
    api_path_default = '/koalixcrm_contracts/api/v1/'
    uses_workspace_id = True

    # ------------------------------------------------------------------
    # Contracts
    # ------------------------------------------------------------------

    def get_contract(self, object_id: int) -> Optional[Contract]:
        return self._get_object(Contract, "/contracts", object_id)

    def get_contract_list(self) -> List[Contract]:
        return self._get_object_list(Contract, "/contracts/")

    def create_contract(self, data: Dict[str, Any]) -> Optional[Contract]:
        response_data = self._make_request("/contracts/", method="POST", data=data)
        if response_data:
            obj = Contract(response_data, self)
            self._cache.set(Contract, obj.id, obj)
            return obj
        return None

    def update_contract(self, object_id: int, data: Dict[str, Any]) -> Optional[Contract]:
        return self._put_full_update(Contract, "/contracts", object_id, data)

    # ------------------------------------------------------------------
    # Invoices
    # ------------------------------------------------------------------

    def get_invoice(self, object_id: int) -> Optional[Invoice]:
        return self._get_object(Invoice, "/invoices", object_id)

    def get_invoice_list(self) -> List[Invoice]:
        return self._get_object_list(Invoice, "/invoices/")

    def create_invoice(self, data: Dict[str, Any]) -> Optional[Invoice]:
        response_data = self._make_request("/invoices/", method="POST", data=data)
        if response_data:
            obj = Invoice(response_data, self)
            self._cache.set(Invoice, obj.id, obj)
            return obj
        return None

    def update_invoice(self, object_id: int, data: Dict[str, Any]) -> Optional[Invoice]:
        return self._put_full_update(Invoice, "/invoices", object_id, data)

    # ------------------------------------------------------------------
    # Quotations
    # ------------------------------------------------------------------

    def get_quotation(self, object_id: int) -> Optional[Quotation]:
        return self._get_object(Quotation, "/quotations", object_id)

    def get_quotation_list(self) -> List[Quotation]:
        return self._get_object_list(Quotation, "/quotations/")

    def create_quotation(self, data: Dict[str, Any]) -> Optional[Quotation]:
        response_data = self._make_request("/quotations/", method="POST", data=data)
        if response_data:
            obj = Quotation(response_data, self)
            self._cache.set(Quotation, obj.id, obj)
            return obj
        return None

    def update_quotation(self, object_id: int, data: Dict[str, Any]) -> Optional[Quotation]:
        return self._put_full_update(Quotation, "/quotations", object_id, data)

    # ------------------------------------------------------------------
    # Purchase Orders
    # ------------------------------------------------------------------

    def get_purchase_order(self, object_id: int) -> Optional[PurchaseOrder]:
        return self._get_object(PurchaseOrder, "/purchase-orders", object_id)

    def get_purchase_order_list(self) -> List[PurchaseOrder]:
        return self._get_object_list(PurchaseOrder, "/purchase-orders/")

    def create_purchase_order(self, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        response_data = self._make_request("/purchase-orders/", method="POST", data=data)
        if response_data:
            obj = PurchaseOrder(response_data, self)
            self._cache.set(PurchaseOrder, obj.id, obj)
            return obj
        return None

    def update_purchase_order(self, object_id: int, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        return self._put_full_update(PurchaseOrder, "/purchase-orders", object_id, data)

    # ------------------------------------------------------------------
    # Sales Orders
    # ------------------------------------------------------------------

    def get_sales_order(self, object_id: int) -> Optional[SalesOrder]:
        return self._get_object(SalesOrder, "/sales-orders", object_id)

    def get_sales_order_list(self) -> List[SalesOrder]:
        return self._get_object_list(SalesOrder, "/sales-orders/")

    def create_sales_order(self, data: Dict[str, Any]) -> Optional[SalesOrder]:
        response_data = self._make_request("/sales-orders/", method="POST", data=data)
        if response_data:
            obj = SalesOrder(response_data, self)
            self._cache.set(SalesOrder, obj.id, obj)
            return obj
        return None

    def update_sales_order(self, object_id: int, data: Dict[str, Any]) -> Optional[SalesOrder]:
        return self._put_full_update(SalesOrder, "/sales-orders", object_id, data)

    # ------------------------------------------------------------------
    # Despatch Advices
    # ------------------------------------------------------------------

    def get_despatch_advice(self, object_id: int) -> Optional[DespatchAdvice]:
        return self._get_object(DespatchAdvice, "/despatch-advices", object_id)

    def get_despatch_advice_list(self) -> List[DespatchAdvice]:
        return self._get_object_list(DespatchAdvice, "/despatch-advices/")

    def create_despatch_advice(self, data: Dict[str, Any]) -> Optional[DespatchAdvice]:
        response_data = self._make_request("/despatch-advices/", method="POST", data=data)
        if response_data:
            obj = DespatchAdvice(response_data, self)
            self._cache.set(DespatchAdvice, obj.id, obj)
            return obj
        return None

    def update_despatch_advice(self, object_id: int, data: Dict[str, Any]) -> Optional[DespatchAdvice]:
        return self._put_full_update(DespatchAdvice, "/despatch-advices", object_id, data)

    # ------------------------------------------------------------------
    # Payment Reminders
    # ------------------------------------------------------------------

    def get_payment_reminder(self, object_id: int) -> Optional[PaymentReminder]:
        return self._get_object(PaymentReminder, "/payment-reminders", object_id)

    def get_payment_reminder_list(self) -> List[PaymentReminder]:
        return self._get_object_list(PaymentReminder, "/payment-reminders/")

    def create_payment_reminder(self, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        response_data = self._make_request("/payment-reminders/", method="POST", data=data)
        if response_data:
            obj = PaymentReminder(response_data, self)
            self._cache.set(PaymentReminder, obj.id, obj)
            return obj
        return None

    def update_payment_reminder(self, object_id: int, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        return self._put_full_update(PaymentReminder, "/payment-reminders", object_id, data)

    # ------------------------------------------------------------------
    # Commercial Document Positions
    # ------------------------------------------------------------------

    def get_commercial_document_position(self, object_id: int) -> Optional[CommercialDocumentPosition]:
        return self._get_object(CommercialDocumentPosition, "/commercial-document-positions", object_id)

    def get_commercial_document_position_list(self) -> List[CommercialDocumentPosition]:
        return self._get_object_list(CommercialDocumentPosition, "/commercial-document-positions/")

    def create_commercial_document_position(self, data: Dict[str, Any]) -> Optional[CommercialDocumentPosition]:
        response_data = self._make_request("/commercial-document-positions/", method="POST", data=data)
        if response_data:
            obj = CommercialDocumentPosition(response_data, self)
            self._cache.set(CommercialDocumentPosition, obj.id, obj)
            return obj
        return None

    def update_commercial_document_position(self, object_id: int, data: Dict[str, Any]) -> Optional[CommercialDocumentPosition]:
        return self._put_full_update(CommercialDocumentPosition, "/commercial-document-positions", object_id, data)

    # ------------------------------------------------------------------
    # Credit Notes
    # ------------------------------------------------------------------

    def get_credit_note(self, object_id: int) -> Optional[CreditNote]:
        return self._get_object(CreditNote, "/credit-notes", object_id)

    def get_credit_note_list(self) -> List[CreditNote]:
        return self._get_object_list(CreditNote, "/credit-notes/")

    def create_credit_note(self, data: Dict[str, Any]) -> Optional[CreditNote]:
        response_data = self._make_request("/credit-notes/", method="POST", data=data)
        if response_data:
            obj = CreditNote(response_data, self)
            self._cache.set(CreditNote, obj.id, obj)
            return obj
        return None

    def update_credit_note(self, object_id: int, data: Dict[str, Any]) -> Optional[CreditNote]:
        return self._put_full_update(CreditNote, "/credit-notes", object_id, data)
