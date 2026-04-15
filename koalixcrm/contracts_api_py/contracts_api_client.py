# -*- coding: utf-8 -*-
"""API client for the koalixcrm Contracts app."""
from typing import Any, Dict, List, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.contracts_api_py.dto.contract import Contract
from koalixcrm.contracts_api_py.dto.invoice import Invoice
from koalixcrm.contracts_api_py.dto.quote import Quote
from koalixcrm.contracts_api_py.dto.purchase_order import PurchaseOrder
from koalixcrm.contracts_api_py.dto.purchase_confirmation import PurchaseConfirmation
from koalixcrm.contracts_api_py.dto.delivery_note import DeliveryNote
from koalixcrm.contracts_api_py.dto.payment_reminder import PaymentReminder
from koalixcrm.contracts_api_py.dto.commercial_document_position import CommercialDocumentPosition
from koalixcrm.contracts_api_py.dto.credit_note import CreditNote


class KoalixCRMContractsAPIClient(BaseAPIClient):
    """API client for managing contracts, commercial documents, and related entities."""

    api_path_env_var = 'KOALIXCRM_CONTRACTS_API_PATH'
    api_path_default = ''

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
    # Quotes
    # ------------------------------------------------------------------

    def get_quote(self, object_id: int) -> Optional[Quote]:
        return self._get_object(Quote, "/quotes", object_id)

    def get_quote_list(self) -> List[Quote]:
        return self._get_object_list(Quote, "/quotes/")

    def create_quote(self, data: Dict[str, Any]) -> Optional[Quote]:
        response_data = self._make_request("/quotes/", method="POST", data=data)
        if response_data:
            obj = Quote(response_data, self)
            self._cache.set(Quote, obj.id, obj)
            return obj
        return None

    def update_quote(self, object_id: int, data: Dict[str, Any]) -> Optional[Quote]:
        return self._put_full_update(Quote, "/quotes", object_id, data)

    # ------------------------------------------------------------------
    # Purchase Orders
    # ------------------------------------------------------------------

    def get_purchase_order(self, object_id: int) -> Optional[PurchaseOrder]:
        return self._get_object(PurchaseOrder, "/purchase_orders", object_id)

    def get_purchase_order_list(self) -> List[PurchaseOrder]:
        return self._get_object_list(PurchaseOrder, "/purchase_orders/")

    def create_purchase_order(self, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        response_data = self._make_request("/purchase_orders/", method="POST", data=data)
        if response_data:
            obj = PurchaseOrder(response_data, self)
            self._cache.set(PurchaseOrder, obj.id, obj)
            return obj
        return None

    def update_purchase_order(self, object_id: int, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        return self._put_full_update(PurchaseOrder, "/purchase_orders", object_id, data)

    # ------------------------------------------------------------------
    # Purchase Confirmations
    # ------------------------------------------------------------------

    def get_purchase_confirmation(self, object_id: int) -> Optional[PurchaseConfirmation]:
        return self._get_object(PurchaseConfirmation, "/purchase_confirmations", object_id)

    def get_purchase_confirmation_list(self) -> List[PurchaseConfirmation]:
        return self._get_object_list(PurchaseConfirmation, "/purchase_confirmations/")

    def create_purchase_confirmation(self, data: Dict[str, Any]) -> Optional[PurchaseConfirmation]:
        response_data = self._make_request("/purchase_confirmations/", method="POST", data=data)
        if response_data:
            obj = PurchaseConfirmation(response_data, self)
            self._cache.set(PurchaseConfirmation, obj.id, obj)
            return obj
        return None

    def update_purchase_confirmation(self, object_id: int, data: Dict[str, Any]) -> Optional[PurchaseConfirmation]:
        return self._put_full_update(PurchaseConfirmation, "/purchase_confirmations", object_id, data)

    # ------------------------------------------------------------------
    # Delivery Notes
    # ------------------------------------------------------------------

    def get_delivery_note(self, object_id: int) -> Optional[DeliveryNote]:
        return self._get_object(DeliveryNote, "/delivery_notes", object_id)

    def get_delivery_note_list(self) -> List[DeliveryNote]:
        return self._get_object_list(DeliveryNote, "/delivery_notes/")

    def create_delivery_note(self, data: Dict[str, Any]) -> Optional[DeliveryNote]:
        response_data = self._make_request("/delivery_notes/", method="POST", data=data)
        if response_data:
            obj = DeliveryNote(response_data, self)
            self._cache.set(DeliveryNote, obj.id, obj)
            return obj
        return None

    def update_delivery_note(self, object_id: int, data: Dict[str, Any]) -> Optional[DeliveryNote]:
        return self._put_full_update(DeliveryNote, "/delivery_notes", object_id, data)

    # ------------------------------------------------------------------
    # Payment Reminders
    # ------------------------------------------------------------------

    def get_payment_reminder(self, object_id: int) -> Optional[PaymentReminder]:
        return self._get_object(PaymentReminder, "/payment_reminders", object_id)

    def get_payment_reminder_list(self) -> List[PaymentReminder]:
        return self._get_object_list(PaymentReminder, "/payment_reminders/")

    def create_payment_reminder(self, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        response_data = self._make_request("/payment_reminders/", method="POST", data=data)
        if response_data:
            obj = PaymentReminder(response_data, self)
            self._cache.set(PaymentReminder, obj.id, obj)
            return obj
        return None

    def update_payment_reminder(self, object_id: int, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        return self._put_full_update(PaymentReminder, "/payment_reminders", object_id, data)

    # ------------------------------------------------------------------
    # Commercial Document Positions
    # ------------------------------------------------------------------

    def get_commercial_document_position(self, object_id: int) -> Optional[CommercialDocumentPosition]:
        return self._get_object(CommercialDocumentPosition, "/commercial_document_positions", object_id)

    def get_commercial_document_position_list(self) -> List[CommercialDocumentPosition]:
        return self._get_object_list(CommercialDocumentPosition, "/commercial_document_positions/")

    def create_commercial_document_position(self, data: Dict[str, Any]) -> Optional[CommercialDocumentPosition]:
        response_data = self._make_request("/commercial_document_positions/", method="POST", data=data)
        if response_data:
            obj = CommercialDocumentPosition(response_data, self)
            self._cache.set(CommercialDocumentPosition, obj.id, obj)
            return obj
        return None

    def update_commercial_document_position(self, object_id: int, data: Dict[str, Any]) -> Optional[CommercialDocumentPosition]:
        return self._put_full_update(CommercialDocumentPosition, "/commercial_document_positions", object_id, data)

    # ------------------------------------------------------------------
    # Credit Notes
    # ------------------------------------------------------------------

    def get_credit_note(self, object_id: int) -> Optional[CreditNote]:
        return self._get_object(CreditNote, "/credit_notes", object_id)

    def get_credit_note_list(self) -> List[CreditNote]:
        return self._get_object_list(CreditNote, "/credit_notes/")

    def create_credit_note(self, data: Dict[str, Any]) -> Optional[CreditNote]:
        response_data = self._make_request("/credit_notes/", method="POST", data=data)
        if response_data:
            obj = CreditNote(response_data, self)
            self._cache.set(CreditNote, obj.id, obj)
            return obj
        return None

    def update_credit_note(self, object_id: int, data: Dict[str, Any]) -> Optional[CreditNote]:
        return self._put_full_update(CreditNote, "/credit_notes", object_id, data)
