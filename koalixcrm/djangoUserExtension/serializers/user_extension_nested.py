# -*- coding: utf-8 -*-
"""
Nested JSON serializer for :class:`UserExtension`.

Exposed at ``GET /api/user_extensions/{id}/``. The Java PDF worker reads this
endpoint once per export job (via ``CommercialDocument.staff``) to render the
"company" block of the XSL-FO document — name, postal/phone/email addresses
of the issuing user — plus the user's default currency.

Shape is additive over the legacy :class:`OptionUserExtensionJSONSerializer`:
the legacy one stays in place for the existing Python clients.
"""
from __future__ import annotations

from typing import Any

from django.contrib.auth.models import User
from rest_framework import serializers

from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.models.user_extension import (
    UserAddressAssignment,
    UserEmailAssignment,
    UserExtension,
    UserPhoneAssignment,
)


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserAddressAssignmentSerializer(serializers.ModelSerializer):
    street = serializers.CharField(source='address.street', read_only=True)
    number = serializers.CharField(source='address.number', read_only=True)
    additional_address_line_1 = serializers.CharField(source='address.additional_address_line_1', read_only=True)
    additional_address_line_2 = serializers.CharField(source='address.additional_address_line_2', read_only=True)
    additional_address_line_3 = serializers.CharField(source='address.additional_address_line_3', read_only=True)
    zip_code = serializers.CharField(source='address.zip_code', read_only=True)
    town = serializers.CharField(source='address.town', read_only=True)
    state = serializers.CharField(source='address.state', read_only=True)
    country = serializers.CharField(source='address.country', read_only=True)
    subdivision_code = serializers.CharField(source='address.subdivision_code', read_only=True)

    class Meta:
        model = UserAddressAssignment
        fields = (
            "id",
            "purpose",
            "is_primary",
            "valid_from",
            "valid_to",
            "street",
            "number",
            "additional_address_line_1",
            "additional_address_line_2",
            "additional_address_line_3",
            "zip_code",
            "town",
            "state",
            "country",
            "subdivision_code",
        )


class UserPhoneAssignmentSerializer(serializers.ModelSerializer):
    phone_e164 = serializers.CharField(source='phone_number.phone_e164', read_only=True)

    class Meta:
        model = UserPhoneAssignment
        fields = ("id", "purpose", "is_primary", "valid_from", "valid_to", "phone_e164")


class UserEmailAssignmentSerializer(serializers.ModelSerializer):
    email_address = serializers.EmailField(source='email.email', read_only=True)

    class Meta:
        model = UserEmailAssignment
        fields = ("id", "purpose", "is_primary", "valid_from", "valid_to", "email_address")


class UserExtensionNestedSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    default_currency = CurrencyJSONSerializer(read_only=True)
    postal_addresses = serializers.SerializerMethodField()
    phone_addresses = serializers.SerializerMethodField()
    email_addresses = serializers.SerializerMethodField()

    class Meta:
        model = UserExtension
        fields = (
            "id",
            "user",
            "default_template_set",
            "default_currency",
            "postal_addresses",
            "phone_addresses",
            "email_addresses",
        )

    def get_postal_addresses(self, instance: UserExtension) -> list[dict[str, Any]]:
        rows = UserAddressAssignment.objects.filter(user=instance.user_id)
        return UserAddressAssignmentSerializer(rows, many=True).data

    def get_phone_addresses(self, instance: UserExtension) -> list[dict[str, Any]]:
        rows = UserPhoneAssignment.objects.filter(user=instance.user_id)
        return UserPhoneAssignmentSerializer(rows, many=True).data

    def get_email_addresses(self, instance: UserExtension) -> list[dict[str, Any]]:
        rows = UserEmailAssignment.objects.filter(user=instance.user_id)
        return UserEmailAssignmentSerializer(rows, many=True).data
