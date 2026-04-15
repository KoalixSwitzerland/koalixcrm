"""
ProductPriceViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.product_price import ProductPrice
from ..serializers.product_price_serializer import ProductPriceJSONSerializer


class ProductPriceViewSet(BaseModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceJSONSerializer
