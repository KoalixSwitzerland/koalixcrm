# -*- coding: utf-8 -*-
"""ServiceProfileViewSet for koalixcrm products"""
from __future__ import annotations

from koalixcrm.products.models.service_profile import ServiceProfile
from koalixcrm.products.serializers.service_profile_serializer import (
    ServiceProfileJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ServiceProfileViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ServiceProfileJSONSerializer
    queryset = ServiceProfile.objects.all()
