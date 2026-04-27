"""
ProductViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.product import Product
from ..serializers.product_serializer import ProductJSONSerializer


class ProductViewSet(BaseModelViewSet):
    serializer_class = ProductJSONSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return Product.objects.filter(workspace=active)
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
