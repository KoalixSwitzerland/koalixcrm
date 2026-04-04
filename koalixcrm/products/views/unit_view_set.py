"""
UnitViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.unit import Unit
from ..serializers.unit_serializer import UnitJSONSerializer


class UnitViewSet(BaseModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitJSONSerializer
