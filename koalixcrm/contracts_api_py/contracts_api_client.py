# -*- coding: utf-8 -*-
"""API client for the koalixcrm Contracts app."""

from __future__ import annotations

from typing import Any

from koalixcrm.contracts_api_py.dto.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.contracts_api_py.dto.contract import Contract
from koalixcrm.contracts_api_py.dto.credit_note import CreditNote
from koalixcrm.contracts_api_py.dto.despatch_advice import DespatchAdvice
from koalixcrm.contracts_api_py.dto.invoice import Invoice
from koalixcrm.contracts_api_py.dto.payment_reminder import PaymentReminder
from koalixcrm.contracts_api_py.dto.purchase_order import PurchaseOrder
from koalixcrm.contracts_api_py.dto.quotation import Quotation
from koalixcrm.contracts_api_py.dto.sales_order import SalesOrder
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMContractsAPIClient(BaseAPIClient):
    """API client for managing contracts, commercial documents, and related entities."""

    api_path_env_var = "KOALIXCRM_CONTRACTS_API_PATH"
    api_path_default = "/koalixcrm_contracts/api/v1/"
    uses_workspace_id = True

    # ------------------------------------------------------------------
    # Contracts
    # ------------------------------------------------------------------

    def get_contract(self, object_id: int) -> Contract | None:
        return self._get_object(Contract, "/contracts", object_id)

    def get_contract_list(self) -> list[Contract]:
        return self._get_object_list(Contract, "/contracts/")

    def create_contract(self, data: dict[str, Any]) -> Contract | None:
        response_data = self._make_request("/contracts/", method="POST", data=data)
        if response_data:
            obj = Contract(response_data, self)
            self._cache.set(Contract, obj.id, obj)
            return obj
        return None

    def update_contract(self, object_id: int, data: dict[str, Any]) -> Contract | None:
        return self._put_full_update(Contract, "/contracts", object_id, data)

    # ------------------------------------------------------------------
    # Invoices
    # ------------------------------------------------------------------

    def get_invoice(self, object_id: int) -> Invoice | None:
        return self._get_object(Invoice, "/invoices", object_id)

    def get_invoice_list(self) -> list[Invoice]:
        return self._get_object_list(Invoice, "/invoices/")

    def create_invoice(self, data: dict[str, Any]) -> Invoice | None:
        response_data = self._make_request("/invoices/", method="POST", data=data)
        if response_data:
            obj = Invoice(response_data, self)
            self._cache.set(Invoice, obj.id, obj)
            return obj
        return None

    def update_invoice(self, object_id: int, data: dict[str, Any]) -> Invoice | None:
        return self._put_full_update(Invoice, "/invoices", object_id, data)

    # ------------------------------------------------------------------
    # Quotations
    # ------------------------------------------------------------------

    def get_quotation(self, object_id: int) -> Quotation | None:
        return self._get_object(Quotation, "/quotations", object_id)

    def get_quotation_list(self) -> list[Quotation]:
        return self._get_object_list(Quotation, "/quotations/")

    def create_quotation(self, data: dict[str, Any]) -> Quotation | None:
        response_data = self._make_request("/quotations/", method="POST", data=data)
        if response_data:
            obj = Quotation(response_data, self)
            self._cache.set(Quotation, obj.id, obj)
            return obj
        return None

    def update_quotation(self, object_id: int, data: dict[str, Any]) -> Quotation | None:
        return self._put_full_update(Quotation, "/quotations", object_id, data)

    # ------------------------------------------------------------------
    # Purchase Orders
    # ------------------------------------------------------------------

    def get_purchase_order(self, object_id: int) -> PurchaseOrder | None:
        return self._get_object(PurchaseOrder, "/purchase-orders", object_id)

    def get_purchase_order_list(self) -> list[PurchaseOrder]:
        return self._get_object_list(PurchaseOrder, "/purchase-orders/")

    def create_purchase_order(self, data: dict[str, Any]) -> PurchaseOrder | None:
        response_data = self._make_request("/purchase-orders/", method="POST", data=data)
        if response_data:
            obj = PurchaseOrder(response_data, self)
            self._cache.set(PurchaseOrder, obj.id, obj)
            return obj
        return None

    def update_purchase_order(self, object_id: int, data: dict[str, Any]) -> PurchaseOrder | None:
        return self._put_full_update(PurchaseOrder, "/purchase-orders", object_id, data)

    # ------------------------------------------------------------------
    # Sales Orders
    # ------------------------------------------------------------------

    def get_sales_order(self, object_id: int) -> SalesOrder | None:
        return self._get_object(SalesOrder, "/sales-orders", object_id)

    def get_sales_order_list(self) -> list[SalesOrder]:
        return self._get_object_list(SalesOrder, "/sales-orders/")

    def create_sales_order(self, data: dict[str, Any]) -> SalesOrder | None:
        response_data = self._make_request("/sales-orders/", method="POST", data=data)
        if response_data:
            obj = SalesOrder(response_data, self)
            self._cache.set(SalesOrder, obj.id, obj)
            return obj
        return None

    def update_sales_order(self, object_id: int, data: dict[str, Any]) -> SalesOrder | None:
        return self._put_full_update(SalesOrder, "/sales-orders", object_id, data)

    # ------------------------------------------------------------------
    # Despatch Advices
    # ------------------------------------------------------------------

    def get_despatch_advice(self, object_id: int) -> DespatchAdvice | None:
        return self._get_object(DespatchAdvice, "/despatch-advices", object_id)

    def get_despatch_advice_list(self) -> list[DespatchAdvice]:
        return self._get_object_list(DespatchAdvice, "/despatch-advices/")

    def create_despatch_advice(self, data: dict[str, Any]) -> DespatchAdvice | None:
        response_data = self._make_request("/despatch-advices/", method="POST", data=data)
        if response_data:
            obj = DespatchAdvice(response_data, self)
            self._cache.set(DespatchAdvice, obj.id, obj)
            return obj
        return None

    def update_despatch_advice(self, object_id: int, data: dict[str, Any]) -> DespatchAdvice | None:
        return self._put_full_update(DespatchAdvice, "/despatch-advices", object_id, data)

    # ------------------------------------------------------------------
    # Payment Reminders
    # ------------------------------------------------------------------

    def get_payment_reminder(self, object_id: int) -> PaymentReminder | None:
        return self._get_object(PaymentReminder, "/payment-reminders", object_id)

    def get_payment_reminder_list(self) -> list[PaymentReminder]:
        return self._get_object_list(PaymentReminder, "/payment-reminders/")

    def create_payment_reminder(self, data: dict[str, Any]) -> PaymentReminder | None:
        response_data = self._make_request("/payment-reminders/", method="POST", data=data)
        if response_data:
            obj = PaymentReminder(response_data, self)
            self._cache.set(PaymentReminder, obj.id, obj)
            return obj
        return None

    def update_payment_reminder(self, object_id: int, data: dict[str, Any]) -> PaymentReminder | None:
        return self._put_full_update(PaymentReminder, "/payment-reminders", object_id, data)

    # ------------------------------------------------------------------
    # Commercial Document Positions
    # ------------------------------------------------------------------

    def get_commercial_document_position(self, object_id: int) -> CommercialDocumentPosition | None:
        return self._get_object(CommercialDocumentPosition, "/commercial-document-positions", object_id)

    def get_commercial_document_position_list(self) -> list[CommercialDocumentPosition]:
        return self._get_object_list(CommercialDocumentPosition, "/commercial-document-positions/")

    def create_commercial_document_position(self, data: dict[str, Any]) -> CommercialDocumentPosition | None:
        response_data = self._make_request("/commercial-document-positions/", method="POST", data=data)
        if response_data:
            obj = CommercialDocumentPosition(response_data, self)
            self._cache.set(CommercialDocumentPosition, obj.id, obj)
            return obj
        return None

    def update_commercial_document_position(
        self, object_id: int, data: dict[str, Any]
    ) -> CommercialDocumentPosition | None:
        return self._put_full_update(CommercialDocumentPosition, "/commercial-document-positions", object_id, data)

    # ------------------------------------------------------------------
    # Credit Notes
    # ------------------------------------------------------------------

    def get_credit_note(self, object_id: int) -> CreditNote | None:
        return self._get_object(CreditNote, "/credit-notes", object_id)

    def get_credit_note_list(self) -> list[CreditNote]:
        return self._get_object_list(CreditNote, "/credit-notes/")

    def create_credit_note(self, data: dict[str, Any]) -> CreditNote | None:
        response_data = self._make_request("/credit-notes/", method="POST", data=data)
        if response_data:
            obj = CreditNote(response_data, self)
            self._cache.set(CreditNote, obj.id, obj)
            return obj
        return None

    def update_credit_note(self, object_id: int, data: dict[str, Any]) -> CreditNote | None:
        return self._put_full_update(CreditNote, "/credit-notes", object_id, data)
