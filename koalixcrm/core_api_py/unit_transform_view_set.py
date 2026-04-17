"""
UnitTransformViewSet for koalixcrm settings
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.core.models.unit_transform import UnitTransform
from koalixcrm.core.serializers.unit_transform_serializer import UnitTransformJSONSerializer


class UnitTransformViewSet(BaseModelViewSet):
    queryset = UnitTransform.objects.all()
    serializer_class = UnitTransformJSONSerializer
