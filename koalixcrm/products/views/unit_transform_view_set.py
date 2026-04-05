"""
UnitTransformViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.unit_transform import UnitTransform
from ..serializers.unit_transform_serializer import UnitTransformJSONSerializer


class UnitTransformViewSet(BaseModelViewSet):
    queryset = UnitTransform.objects.all()
    serializer_class = UnitTransformJSONSerializer
