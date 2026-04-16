"""
CurrencyTransformViewSet for koalixcrm settings
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.currency_transform import CurrencyTransform
from ..serializers.currency_transform_serializer import CurrencyTransformJSONSerializer


class CurrencyTransformViewSet(BaseModelViewSet):
    queryset = CurrencyTransform.objects.all()
    serializer_class = CurrencyTransformJSONSerializer
