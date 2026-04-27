"""
UnitViewSet for koalixcrm settings
"""
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.unit_serializer import UnitJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitJSONSerializer
