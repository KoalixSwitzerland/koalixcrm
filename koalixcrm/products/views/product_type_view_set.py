"""
ProductTypeViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.product_type import ProductType
from ..serializers.product_type_serializer import ProductJSONSerializer


class ProductTypeViewSet(BaseModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductJSONSerializer
