# -*- coding: utf-8 -*-
from __future__ import annotations

from koalixcrm.reporting.models.generic_task_link import GenericTaskLink
from koalixcrm.reporting.serializers.generic_task_link_serializer import (
    GenericTaskLinkJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class GenericTaskLinkViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = GenericTaskLink.objects.all()
    serializer_class = GenericTaskLinkJSONSerializer
