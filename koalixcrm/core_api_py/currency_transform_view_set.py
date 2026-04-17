"""
CurrencyTransformViewSet for koalixcrm settings
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.core.models.currency_transform import CurrencyTransform
from koalixcrm.core.serializers.currency_transform_serializer import CurrencyTransformJSONSerializer


class CurrencyTransformViewSet(BaseModelViewSet):
    queryset = CurrencyTransform.objects.all()
    serializer_class = CurrencyTransformJSONSerializer
