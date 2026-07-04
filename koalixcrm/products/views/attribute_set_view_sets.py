# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.products.models.attribute_set import AttributeSet, AttributeSetGroup
from koalixcrm.products.serializers.attribute_set_serializer import (
    AttributeSetGroupJSONSerializer,
    AttributeSetJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class AttributeSetViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = AttributeSetJSONSerializer
    queryset = AttributeSet.objects.all()


class AttributeSetGroupViewSet(BaseModelViewSet):
    serializer_class = AttributeSetGroupJSONSerializer
    queryset = AttributeSetGroup.objects.all()
