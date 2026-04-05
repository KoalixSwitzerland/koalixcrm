"""
CustomerGroupTransformViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.customer_group_transform import CustomerGroupTransform
from ..serializers.customer_group_transform_serializer import CustomerGroupTransformJSONSerializer


class CustomerGroupTransformViewSet(BaseModelViewSet):
    queryset = CustomerGroupTransform.objects.all()
    serializer_class = CustomerGroupTransformJSONSerializer
