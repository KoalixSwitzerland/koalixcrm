# -*- coding: utf-8 -*-
"""UnitOfMeasureConversionViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)
from koalixcrm.products.serializers.unit_of_measure_conversion_serializer import (
    UnitOfMeasureConversionJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class UnitOfMeasureConversionViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = UnitOfMeasureConversionJSONSerializer
    queryset = UnitOfMeasureConversion.objects.all()
