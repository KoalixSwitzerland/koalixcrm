# -*- coding: utf-8 -*-
"""
RetentionPolicyViewSet for koalixcrm stock
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.retention_policy import RetentionPolicy
from koalixcrm.stock.serializers.retention_policy_serializer import RetentionPolicyJSONSerializer


class RetentionPolicyViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = RetentionPolicyJSONSerializer
    queryset = RetentionPolicy.objects.all()
