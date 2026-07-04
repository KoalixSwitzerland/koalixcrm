# -*- coding: utf-8 -*-
"""
LocationViewSet for koalixcrm stock
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.location import Location
from koalixcrm.stock.serializers.location_serializer import LocationJSONSerializer


class LocationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = LocationJSONSerializer
    queryset = Location.objects.all()
