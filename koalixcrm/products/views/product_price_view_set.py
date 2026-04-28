"""
ProductPriceViewSet for koalixcrm products
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.product_price import ProductPrice
from ..serializers.product_price_serializer import ProductPriceJSONSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.serializers import BaseSerializer


class ProductPriceViewSet(BaseModelViewSet):
    serializer_class = ProductPriceJSONSerializer
    queryset = ProductPrice.objects.all()

    def get_queryset(self) -> QuerySet[ProductPrice]:
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return ProductPrice.objects.filter(workspace=active)
        if self.request.user.is_superuser:
            return ProductPrice.objects.all()
        return ProductPrice.objects.none()

    def perform_create(self, serializer: BaseSerializer) -> None:
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
