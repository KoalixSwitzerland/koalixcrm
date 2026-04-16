# -*- coding: utf-8 -*-
"""
Deeply-nested JSON serializers for the commercial-document types.

Consumed by the Java PDF worker: a single GET returns everything the
XslFo builders need — customer / supplier contact details, positions with
product type and tax, document-level totals, and a pre-computed tax summary.

Additive over the shallow legacy serializers (``InvoiceJSONSerializer`` etc.):
those stay in place for existing Python clients.
"""
from collections import OrderedDict
from decimal import Decimal

from rest_framework import serializers

from koalixcrm.contacts.models.contact import (
    EmailAddressForContact,
    PhoneAddressForContact,
    PostalAddressForContact,
)
from koalixcrm.contracts.models.commercial_document import CommercialDocument
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


class ContactPostalAddressNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddressForContact
        fields = (
            "id",
            "purpose",
            "prefix",
            "pre_name",
            "name",
            "address_line_1",
            "address_line_2",
            "address_line_3",
            "address_line_4",
            "zip_code",
            "town",
            "state",
            "country",
            "subdivision_code",
        )


class ContactPhoneAddressNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneAddressForContact
        fields = ("id", "purpose", "phone")


class ContactEmailAddressNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddressForContact
        fields = ("id", "purpose", "email")


class ContactNestedSerializer(serializers.Serializer):
    """
    Serializer for a ``Contact`` row (shared by Customer and Supplier) with
    nested address lists. Works by taking either a Customer/Supplier instance
    or a plain Contact instance — all three are ``Contact`` subclasses.
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    postal_addresses = serializers.SerializerMethodField()
    phone_addresses = serializers.SerializerMethodField()
    email_addresses = serializers.SerializerMethodField()

    def get_postal_addresses(self, obj):
        rows = PostalAddressForContact.objects.filter(person=obj.id)
        return ContactPostalAddressNestedSerializer(rows, many=True).data

    def get_phone_addresses(self, obj):
        rows = PhoneAddressForContact.objects.filter(person=obj.id)
        return ContactPhoneAddressNestedSerializer(rows, many=True).data

    def get_email_addresses(self, obj):
        rows = EmailAddressForContact.objects.filter(person=obj.id)
        return ContactEmailAddressNestedSerializer(rows, many=True).data


class ProductTypeNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_type_identifier = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    default_unit = OptionUnitJSONSerializer(read_only=True)
    tax = OptionTaxJSONSerializer(read_only=True)
    tax_rate = serializers.SerializerMethodField()

    def get_tax_rate(self, obj):
        if obj.tax is None:
            return None
        return str(obj.tax.get_tax_rate())


class PositionNestedSerializer(serializers.ModelSerializer):
    """One line item in a commercial document, with product/tax info inlined."""

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
            "last_pricing_date",
            "last_calculated_price",
            "last_calculated_tax",
            "overwrite_product_price",
        )


def _compute_tax_summary(positions):
    """
    Aggregate positions by tax rate.

    Returns a list of ``{"rate": "8.1", "taxable_amount": "...", "tax_amount": "..."}``
    ordered by tax rate ascending. Positions without a ProductType/Tax are
    grouped under an ``"unknown"`` rate entry so they are not silently dropped.
    """
    buckets = OrderedDict()
    for p in positions:
        rate_key = "unknown"
        if p.product_type is not None and p.product_type.tax is not None:
            rate_key = str(p.product_type.tax.get_tax_rate())
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
    """
    Base for subclass-specific nested serializers.

    ``type`` helps the Java worker pick the right :class:`XmlBuilder`. ``items``
    are ordered by ``position_number``. ``user_extension`` is a sub-resource
    (bare id) so the worker fetches it separately only when needed.
    """

    type = serializers.SerializerMethodField()
    customer = ContactNestedSerializer(read_only=True)
    currency = CurrencyJSONSerializer(read_only=True)
    items = serializers.SerializerMethodField()
    tax_summary = serializers.SerializerMethodField()
    user_extension = serializers.SerializerMethodField()

    class Meta:
        model = CommercialDocument
        fields = (
            "id",
            "type",
            "contract",
            "customer",
            "staff",
            "currency",
            "external_reference",
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
            "user_extension",
        )

    def get_type(self, obj):
        return type(obj).__name__

    def _positions(self, obj):
        return list(
            CommercialDocumentPosition.objects.filter(commercial_document=obj.id).order_by(
                "position_number"
            )
        )

    def get_items(self, obj):
        return PositionNestedSerializer(self._positions(obj), many=True).data

    def get_tax_summary(self, obj):
        return _compute_tax_summary(self._positions(obj))

    def get_user_extension(self, obj):
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
    """DeliveryNote in the migration doc's terminology."""

    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = DespatchAdvice
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "tracking_reference",
            "status",
        )


class PurchaseOrderNestedSerializer(_BaseCommercialDocumentNestedSerializer):
    """Purchase orders carry a ``supplier`` (not ``customer``)."""

    supplier = ContactNestedSerializer(read_only=True)

    class Meta(_BaseCommercialDocumentNestedSerializer.Meta):
        model = PurchaseOrder
        fields = _BaseCommercialDocumentNestedSerializer.Meta.fields + (
            "supplier",
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
