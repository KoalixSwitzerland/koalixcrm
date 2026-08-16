# -*- coding: utf-8 -*-
"""Read-only DRF endpoint for `AttributeValidationRule` (ADR-0020: rules
are exposed to the frontend read-only alongside `AttributeSet` metadata;
the backend is the sole writer)."""
from __future__ import annotations

from rest_framework import viewsets

from koalixcrm.products.models.attribute_validation_rule import AttributeValidationRule
from koalixcrm.products.serializers.attribute_validation_rule_serializer import (
    AttributeValidationRuleJSONSerializer,
)
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class AttributeValidationRuleViewSet(WorkspaceScopedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = AttributeValidationRuleJSONSerializer
    queryset = AttributeValidationRule.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        attribute_set_id = self.request.query_params.get('attribute_set')
        if attribute_set_id is not None:
            qs = qs.filter(attribute_set_id=attribute_set_id)
        return qs
