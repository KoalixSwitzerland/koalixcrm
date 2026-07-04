# -*- coding: utf-8 -*-
"""ADR-0007/REQ-0016, ADR-0019: `ServiceProfile` kind-gating at the
serializer layer, mirroring `ServiceProfile.clean()`."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from koalixcrm.products.models.choices import ServiceBillingModel
from koalixcrm.products.models.service_profile import ServiceProfile
from koalixcrm.products.services.product_kind_policy import check_gate


class ServiceProfileJSONSerializer(serializers.ModelSerializer):
    billing_model = serializers.ChoiceField(choices=ServiceBillingModel.choices)

    class Meta:
        model = ServiceProfile
        fields = ('id', 'product', 'billing_model', 'default_duration', 'deliverable', 'sla_reference')

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        product = attrs.get('product') or (self.instance.product if self.instance else None)
        if product is not None:
            try:
                check_gate("ServiceProfile", product.kind)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.messages) from exc
        return attrs
