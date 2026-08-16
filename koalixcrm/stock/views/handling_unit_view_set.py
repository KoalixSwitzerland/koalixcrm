# -*- coding: utf-8 -*-
"""
HandlingUnitViewSet for koalixcrm stock
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.handling_unit import HandlingUnit
from koalixcrm.stock.serializers.handling_unit_serializer import HandlingUnitJSONSerializer


class HandlingUnitViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = HandlingUnitJSONSerializer
    queryset = HandlingUnit.objects.all()
