"""
ProductViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.product import Product
from ..serializers.product_serializer import ProductJSONSerializer


class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductJSONSerializer
