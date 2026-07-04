# -*- coding: utf-8 -*-
"""BillOfMaterialsViewSet + BomItemViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.bill_of_materials import BillOfMaterials
from koalixcrm.products.models.bom_item import BomItem
from koalixcrm.products.serializers.bill_of_materials_serializer import (
    BillOfMaterialsJSONSerializer,
    BomItemJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class BillOfMaterialsViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = BillOfMaterialsJSONSerializer
    queryset = BillOfMaterials.objects.all()


class BomItemViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = BomItemJSONSerializer
    queryset = BomItem.objects.all()
