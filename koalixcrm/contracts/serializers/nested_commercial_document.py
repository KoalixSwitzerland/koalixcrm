# -*- coding: utf-8 -*-
"""Deeply-nested JSON serializers for the commercial-document types.

Consumed by the Java PDF worker: a single GET returns everything the
XslFo builders need — party (Organization or Contact) details, positions
with product type and tax, document-level totals, and a pre-computed tax
summary.

v2.0.0 (issue #395 G3): every commercial document now carries a `party`
FK pointing at a Party (Organization or PartyContact). The legacy
`customer` / `supplier` fields on Contract / CommercialDocument /
PurchaseOrder are gone. The nested shape here reflects that — the JSON
field `party` replaces the old `customer` (and the separate `supplier`
field on PurchaseOrder is also gone; POs use the inherited `party`).
"""
from __future__ import annotations

from collections import OrderedDict
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from rest_framework import serializers

if TYPE_CHECKING:
    from koalixcrm.contacts.models.party import Party
    from koalixcrm.contracts.models.commercial_document import CommercialDocument as CommercialDocumentModel

from koalixcrm.contacts.models.address_assignment import AddressAssignment
from koalixcrm.contacts.models.email_assignment import EmailAssignment
from koalixcrm.contacts.models.natural_person import PartyContact
from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.models.phone_assignment import PhoneAssignment
from koalixcrm.contracts.models.commercial_document import (
    CommercialDocument,
    TextParagraphInCommercialDocument,
)
from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.contracts.models.credit_note import CreditNote
from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.core.serializers.tax_serializer import OptionTaxJSONSerializer
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer


class NestedAddressSerializer(serializers.Serializer):
    purpose = serializers.CharField(read_only=True)
    is_primary = serializers.BooleanField(read_only=True)
    street = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    additional_address_line_1 = serializers.SerializerMethodField()
    additional_address_line_2 = serializers.SerializerMethodField()
    additional_address_line_3 = serializers.SerializerMethodField()
    zip_code = serializers.SerializerMethodField()
    town = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    subdivision_code = serializers.SerializerMethodField()

    def _addr(self, obj: Any) -> Any:
        return obj.address

    def get_street(self, obj: Any) -> Any: return self._addr(obj).street
    def get_number(self, obj: Any) -> Any: return self._addr(obj).number
    def get_additional_address_line_1(self, obj: Any) -> Any: return self._addr(obj).additional_address_line_1
    def get_additional_address_line_2(self, obj: Any) -> Any: return self._addr(obj).additional_address_line_2
    def get_additional_address_line_3(self, obj: Any) -> Any: return self._addr(obj).additional_address_line_3
    def get_zip_code(self, obj: Any) -> Any: return self._addr(obj).zip_code
    def get_town(self, obj: Any) -> Any: return self._addr(obj).town
    def get_state(self, obj: Any) -> Any: return self._addr(obj).state
    def get_country(self, obj: Any) -> Any: return self._addr(obj).country
    def get_subdivision_code(self, obj: Any) -> Any: return self._addr(obj).subdivision_code


class NestedPhoneSerializer(serializers.Serializer):
    purpose = serializers.CharField(read_only=True)
    is_primary = serializers.BooleanField(read_only=True)
    phone_e164 = serializers.SerializerMethodField()

    def get_phone_e164(self, obj: Any) -> str:
        return obj.phone.phone_e164


class NestedEmailSerializer(serializers.Serializer):
    purpose = serializers.CharField(read_only=True)
    is_primary = serializers.BooleanField(read_only=True)
    email = serializers.SerializerMethodField()

    def get_email(self, obj: Any) -> str:
        return obj.email.email


class PartyNestedSerializer(serializers.Serializer):
    """A Party (Organization or natural-person Contact) with its assignments.

    The Java PDF worker reads this shape via the nested commercial-document
    endpoints. The `type` field ("organization" / "contact") tells the
    worker which name fields to render; `postal_addresses` / `phone_numbers`
    / `email_addresses` source from the new assignment tables (loose links,
    purpose + validity) rather than from MTI satellite tables as the legacy
    `customer` block did.
    """

    id = serializers.IntegerField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    type = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    postal_addresses = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    email_addresses = serializers.SerializerMethodField()

    def get_type(self, obj: Party) -> str:
        if Organization.objects.filter(party_ptr_id=obj.id).exists():
            return 'organization'
        if PartyContact.objects.filter(party_ptr_id=obj.id).exists():
            return 'contact'
        return 'party'  # bare Party (shouldn't happen for documents)

    def get_organization(self, obj: Party) -> dict[str, Any] | None:
        org = Organization.objects.filter(party_ptr_id=obj.id).first()
        if not org:
            return None
        return {
            'legal_name': org.legal_name,
            'legal_form': org.legal_form,
            'registration_number': org.registration_number,
            'legal_seat_country': org.legal_seat_country,
        }

    def get_contact(self, obj: Party) -> dict[str, Any] | None:
        contact = PartyContact.objects.filter(party_ptr_id=obj.id).first()
        if not contact:
            return None
        return {
            'prefix': contact.prefix,
            'given_name': contact.given_name,
            'family_name': contact.family_name,
        }

    def get_postal_addresses(self, obj: Party) -> list[dict[str, Any]]:
        rows = AddressAssignment.objects.filter(party=obj).select_related('address')
        return NestedAddressSerializer(rows, many=True).data

    def get_phone_numbers(self, obj: Party) -> list[dict[str, Any]]:
        rows = PhoneAssignment.objects.filter(party=obj).select_related('phone')
        return NestedPhoneSerializer(rows, many=True).data

    def get_email_addresses(self, obj: Party) -> list[dict[str, Any]]:
        rows = EmailAssignment.objects.filter(party=obj).select_related('email')
        return NestedEmailSerializer(rows, many=True).data


class ProductTypeNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_type_identifier = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    default_unit = OptionUnitJSONSerializer(read_only=True)
    tax = OptionTaxJSONSerializer(read_only=True)
    tax_rate = serializers.SerializerMethodField()

    def get_tax_rate(self, obj: Any) -> str | None:
        if obj.tax is None:
            return None
        return str(obj.tax.get_tax_rate())


class PositionNestedSerializer(serializers.ModelSerializer):
    product_type = ProductTypeNestedSerializer(read_only=True)
    unit = OptionUnitJSONSerializer(read_only=True)

    class Meta:
        model = CommercialDocumentPosition
        fields = (
            "id",
            "position_number",
            "description",
            "quantity",
            "unit",
            "product_type",
            "discount",
            "position_price_per_unit",
            "position_tax_rate",
            "last_pricing_date",
            "last_calculated_price",
            "last_calculated_tax",
            "overwrite_product_price",
        )


def _compute_tax_summary(positions: list[CommercialDocumentPosition]) -> list[dict[str, str]]:
    """Aggregate positions by tax rate. Returns a list ordered by rate."""
    buckets: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for p in positions:
        rate_key = "unknown"
        if p.product_type is not None and p.product_type.tax is not None:
            rate_key = str(p.product_type.tax.get_tax_rate())
        elif p.position_tax_rate is not None:
            rate_key = str(p.position_tax_rate)
        entry = buckets.setdefault(
            rate_key, {"rate": rate_key, "taxable_amount": Decimal(0), "tax_amount": Decimal(0)}
        )
        if p.last_calculated_price is not None:
            entry["taxable_amount"] += Decimal(p.last_calculated_price)
        if p.last_calculated_tax is not None:
            entry["tax_amount"] += Decimal(p.last_calculated_tax)
    return [
        {
            "rate": entry["rate"],
            "taxable_amount": str(entry["taxable_amount"]),
            "tax_amount": str(entry["tax_amount"]),
        }
        for entry in buckets.values()
    ]


class _BaseCommercialDocumentNestedSerializer(serializers.ModelSerializer):
    """Base for subclass-specific nested serializers.

    `type` helps the Java worker pick the right XmlBuilder. `items` are
    ordered by `position_number`. `user_extension` is a sub-resource
    (bare id) so the worker fetches it separately only when needed.
    """

    type = serializers.SerializerMethodField()
    party = PartyNestedSerializer(read_only=True)
    currency = CurrencyJSONSerializer(read_only=True)
    items = serializers.SerializerMethodField()
    tax_summary = serializers.SerializerMethodField()
    text_paragraphs = serializers.SerializerMethodField()
    user_extension = serializers.SerializerMethodField()

    class Meta:
        model = CommercialDocument
        fields = (
            "id",
            "type",
            "contract",
            "party",
            "staff",
            "currency",
            "party_reference",
            "ext_business_appl_references",
            "description",
            "discount",
            "last_pricing_date",
            "last_calculated_price",
            "last_calculated_tax",
            "date_of_creation",
            "last_modification",
            "custom_date_field",
            "template_set",
            "items",
            "tax_summary",
            "text_paragraphs",
            "user_extension",
        )

    def get_type(self, obj: CommercialDocumentModel) -> str:
        return type(obj).__name__

    def _positions(self, obj: CommercialDocumentModel) -> list[CommercialDocumentPosition]:
        return list(
            CommercialDocumentPosition.objects.filter(commercial_document=obj.id).order_by(
                "position_number"
            )
        )

    def get_items(self, obj: CommercialDocumentModel) -> list[dict[str, Any]]:
        return PositionNestedSerializer(self._positions(obj), many=True).data

    def get_tax_summary(self, obj: CommercialDocumentModel) -> list[dict[str, str]]:
        return _compute_tax_summary(self._positions(obj))

    def get_text_paragraphs(self, obj: CommercialDocumentModel) -> list[dict[str, str]]:
        """Intro / mid / closing free-text blocks (purpose BS / AS / AT …).

        The Java worker emits each as `<text_paragraph purpose="…">…` and the
        XSL-FO templates switch on the purpose to place them around the
        positions table.
        """
        rows = TextParagraphInCommercialDocument.objects.filter(
            commercial_document=obj.id
        ).order_by("id")
        return [
            {"purpose": row.purpose, "text_paragraph": row.text_paragraph}
            for row in rows
        ]

    def get_user_extension(self, obj: CommercialDocumentModel) -> int | None:
        if obj.staff_id is None:
            return None
        from koalixcrm.djangoUserExtension.models.user_extension import UserExtension

        extension = UserExtension.objects.filter(user_id=obj.staff_id).first()
        return extension.id if extension is not None else None


class InvoiceNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = Invoice
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "payable_until",
            "payment_bank_reference",
            "status",
        )


class QuotationNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = Quotation
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "valid_until",
            "status",
        )


class DespatchAdviceNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = DespatchAdvice
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "tracking_reference",
            "status",
        )


class PurchaseOrderNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    """Purchase orders carry the supplier in the inherited `party` field — no
    separate `supplier` block in v2.0.0 (the legacy PurchaseOrder.supplier FK
    was dropped in #395 G3)."""

    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = PurchaseOrder
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "status",
        )


class PaymentReminderNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = PaymentReminder
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "payable_until",
            "payment_bank_reference",
            "iteration_number",
            "status",
        )


class CreditNoteNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = CreditNote
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "corrects_invoice",
            "issue_date",
            "reason",
            "status",
        )
