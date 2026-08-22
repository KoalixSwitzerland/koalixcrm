"""
ProductPriceViewSet for koalixcrm products
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.product_price import ProductPrice
from ..serializers.product_price_serializer import ProductPriceJSONSerializer
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ProductPriceViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductPriceJSONSerializer
    queryset = ProductPrice.objects.all()
