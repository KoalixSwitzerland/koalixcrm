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
from rest_framework import serializers

from django.contrib.auth.models import User

from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.models.user_extension import (
    UserExtension,
    UserExtensionEmailAddress,
    UserExtensionPhoneAddress,
    UserExtensionPostalAddress,
)


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class UserExtensionPostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtensionPostalAddress
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


class UserExtensionPhoneAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtensionPhoneAddress
        fields = ("id", "purpose", "phone")


class UserExtensionEmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtensionEmailAddress
        fields = ("id", "purpose", "email")


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

    def get_postal_addresses(self, instance):
        rows = UserExtensionPostalAddress.objects.filter(userExtension=instance)
        return UserExtensionPostalAddressSerializer(rows, many=True).data

    def get_phone_addresses(self, instance):
        rows = UserExtensionPhoneAddress.objects.filter(userExtension=instance)
        return UserExtensionPhoneAddressSerializer(rows, many=True).data

    def get_email_addresses(self, instance):
        rows = UserExtensionEmailAddress.objects.filter(userExtension=instance)
        return UserExtensionEmailAddressSerializer(rows, many=True).data
