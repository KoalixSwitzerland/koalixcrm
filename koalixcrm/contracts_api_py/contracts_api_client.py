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
from koalixcrm.contracts_api_py.dto.sales_document_position import SalesDocumentPosition


class KoalixCRMContractsAPIClient(BaseAPIClient):
    """API client for managing contracts, sales documents, and related entities."""

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
        return self._get_object(PurchaseOrder, "/purchaseOrders", object_id)

    def get_purchase_order_list(self) -> List[PurchaseOrder]:
        return self._get_object_list(PurchaseOrder, "/purchaseOrders/")

    def create_purchase_order(self, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        response_data = self._make_request("/purchaseOrders/", method="POST", data=data)
        if response_data:
            obj = PurchaseOrder(response_data, self)
            self._cache.set(PurchaseOrder, obj.id, obj)
            return obj
        return None

    def update_purchase_order(self, object_id: int, data: Dict[str, Any]) -> Optional[PurchaseOrder]:
        return self._put_full_update(PurchaseOrder, "/purchaseOrders", object_id, data)

    # ------------------------------------------------------------------
    # Purchase Confirmations
    # ------------------------------------------------------------------

    def get_purchase_confirmation(self, object_id: int) -> Optional[PurchaseConfirmation]:
        return self._get_object(PurchaseConfirmation, "/purchaseConfirmations", object_id)

    def get_purchase_confirmation_list(self) -> List[PurchaseConfirmation]:
        return self._get_object_list(PurchaseConfirmation, "/purchaseConfirmations/")

    def create_purchase_confirmation(self, data: Dict[str, Any]) -> Optional[PurchaseConfirmation]:
        response_data = self._make_request("/purchaseConfirmations/", method="POST", data=data)
        if response_data:
            obj = PurchaseConfirmation(response_data, self)
            self._cache.set(PurchaseConfirmation, obj.id, obj)
            return obj
        return None

    def update_purchase_confirmation(self, object_id: int, data: Dict[str, Any]) -> Optional[PurchaseConfirmation]:
        return self._put_full_update(PurchaseConfirmation, "/purchaseConfirmations", object_id, data)

    # ------------------------------------------------------------------
    # Delivery Notes
    # ------------------------------------------------------------------

    def get_delivery_note(self, object_id: int) -> Optional[DeliveryNote]:
        return self._get_object(DeliveryNote, "/deliveryNotes", object_id)

    def get_delivery_note_list(self) -> List[DeliveryNote]:
        return self._get_object_list(DeliveryNote, "/deliveryNotes/")

    def create_delivery_note(self, data: Dict[str, Any]) -> Optional[DeliveryNote]:
        response_data = self._make_request("/deliveryNotes/", method="POST", data=data)
        if response_data:
            obj = DeliveryNote(response_data, self)
            self._cache.set(DeliveryNote, obj.id, obj)
            return obj
        return None

    def update_delivery_note(self, object_id: int, data: Dict[str, Any]) -> Optional[DeliveryNote]:
        return self._put_full_update(DeliveryNote, "/deliveryNotes", object_id, data)

    # ------------------------------------------------------------------
    # Payment Reminders
    # ------------------------------------------------------------------

    def get_payment_reminder(self, object_id: int) -> Optional[PaymentReminder]:
        return self._get_object(PaymentReminder, "/paymentReminders", object_id)

    def get_payment_reminder_list(self) -> List[PaymentReminder]:
        return self._get_object_list(PaymentReminder, "/paymentReminders/")

    def create_payment_reminder(self, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        response_data = self._make_request("/paymentReminders/", method="POST", data=data)
        if response_data:
            obj = PaymentReminder(response_data, self)
            self._cache.set(PaymentReminder, obj.id, obj)
            return obj
        return None

    def update_payment_reminder(self, object_id: int, data: Dict[str, Any]) -> Optional[PaymentReminder]:
        return self._put_full_update(PaymentReminder, "/paymentReminders", object_id, data)

    # ------------------------------------------------------------------
    # Sales Document Positions
    # ------------------------------------------------------------------

    def get_sales_document_position(self, object_id: int) -> Optional[SalesDocumentPosition]:
        return self._get_object(SalesDocumentPosition, "/salesDocumentPositions", object_id)

    def get_sales_document_position_list(self) -> List[SalesDocumentPosition]:
        return self._get_object_list(SalesDocumentPosition, "/salesDocumentPositions/")

    def create_sales_document_position(self, data: Dict[str, Any]) -> Optional[SalesDocumentPosition]:
        response_data = self._make_request("/salesDocumentPositions/", method="POST", data=data)
        if response_data:
            obj = SalesDocumentPosition(response_data, self)
            self._cache.set(SalesDocumentPosition, obj.id, obj)
            return obj
        return None

    def update_sales_document_position(self, object_id: int, data: Dict[str, Any]) -> Optional[SalesDocumentPosition]:
        return self._put_full_update(SalesDocumentPosition, "/salesDocumentPositions", object_id, data)
