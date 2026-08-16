# -*- coding: utf-8 -*-
"""`AttributeDefinition` is hybrid-scoped — see `AttributeGroupViewSet`
docstring for why `WorkspaceScopedViewSetMixin` is not used here."""
from __future__ import annotations

from koalixcrm.products.models.attribute_definition import AttributeDefinition
from koalixcrm.products.serializers.attribute_definition_serializer import (
    AttributeDefinitionJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AttributeDefinitionViewSet(BaseModelViewSet):
    serializer_class = AttributeDefinitionJSONSerializer
    queryset = AttributeDefinition.objects.all()
