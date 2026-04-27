"""
UnitTransformViewSet for koalixcrm settings
"""
from koalixcrm.core.models.unit_transform import UnitTransform
from koalixcrm.core.serializers.unit_transform_serializer import (
    UnitTransformJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class UnitTransformViewSet(BaseModelViewSet):
    queryset = UnitTransform.objects.all()
    serializer_class = UnitTransformJSONSerializer
