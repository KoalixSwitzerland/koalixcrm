# -*- coding: utf-8 -*-
"""`AttributeGroup` is hybrid-scoped (global for GLOBAL scope, workspace for
WORKSPACE scope) — it does not use `WorkspaceScopedViewSetMixin` (which
always stamps a workspace on create); global rows are created with
`workspace=None` directly via the `scope` field."""
from __future__ import annotations

from koalixcrm.products.models.attribute_group import AttributeGroup
from koalixcrm.products.serializers.attribute_group_serializer import (
    AttributeGroupJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AttributeGroupViewSet(BaseModelViewSet):
    serializer_class = AttributeGroupJSONSerializer
    queryset = AttributeGroup.objects.all()
