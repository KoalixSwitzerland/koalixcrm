"""
CustomerGroupTransformViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.customer_group_transform import CustomerGroupTransform
from ..serializers.customer_group_transform_serializer import CustomerGroupTransformJSONSerializer


class CustomerGroupTransformViewSet(BaseModelViewSet):
    serializer_class = CustomerGroupTransformJSONSerializer
    queryset = CustomerGroupTransform.objects.all()

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return CustomerGroupTransform.objects.filter(workspace=active)
        if self.request.user.is_superuser:
            return CustomerGroupTransform.objects.all()
        return CustomerGroupTransform.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
