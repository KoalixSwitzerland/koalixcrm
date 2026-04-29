from __future__ import annotations

from rest_framework import serializers

from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.djangoUserExtension.serializers.template_set_rest import (
    TemplateSetJSONSerializer,
)


class OptionUserExtensionJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    default_template_set = TemplateSetJSONSerializer(required=False)
    default_currency = CurrencyJSONSerializer(required=False)

    class Meta:
        model = UserExtension
        fields = ('id',
                  'default_template_set',
                  'default_currency')
