# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.products.models.attribute_set_default import AttributeSetDefault
from koalixcrm.products.serializers.attribute_set_default_serializer import (
    AttributeSetDefaultJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class AttributeSetDefaultViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = AttributeSetDefaultJSONSerializer
    queryset = AttributeSetDefault.objects.all()
