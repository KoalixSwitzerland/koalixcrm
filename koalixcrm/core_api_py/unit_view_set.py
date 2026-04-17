"""
UnitViewSet for koalixcrm settings
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.unit_serializer import UnitJSONSerializer


class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitJSONSerializer
