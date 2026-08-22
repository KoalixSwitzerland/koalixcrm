"""
CustomerGroupTransformViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.customer_group_transform import CustomerGroupTransform
from ..serializers.customer_group_transform_serializer import (
    CustomerGroupTransformJSONSerializer,
)
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class CustomerGroupTransformViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = CustomerGroupTransformJSONSerializer
    queryset = CustomerGroupTransform.objects.all()
