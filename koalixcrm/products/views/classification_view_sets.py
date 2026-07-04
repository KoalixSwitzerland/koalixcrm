# -*- coding: utf-8 -*-
"""ViewSets for the global classification taxonomy (ADR-0004). Not
workspace-scoped: `Classification`/`ClassificationNode` are shared master
data across all tenants."""
from __future__ import annotations

from koalixcrm.products.models.classification import Classification, ClassificationNode
from koalixcrm.products.serializers.classification_serializer import (
    ClassificationJSONSerializer,
    ClassificationNodeJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class ClassificationViewSet(BaseModelViewSet):
    serializer_class = ClassificationJSONSerializer
    queryset = Classification.objects.all()


class ClassificationNodeViewSet(BaseModelViewSet):
    serializer_class = ClassificationNodeJSONSerializer
    queryset = ClassificationNode.objects.all()
