"""
ProductTypeViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.product_type import ProductType
from ..serializers.product_type_serializer import ProductJSONSerializer


class ProductTypeViewSet(BaseModelViewSet):
    serializer_class = ProductJSONSerializer
    queryset = ProductType.objects.all()

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return ProductType.objects.filter(workspace=active)
        if self.request.user.is_superuser:
            return ProductType.objects.all()
        return ProductType.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
