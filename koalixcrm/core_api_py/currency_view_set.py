"""
CurrencyViewSet for koalixcrm settings
"""
from koalixcrm.core.models.currency import Currency
from koalixcrm.core.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class CurrencyViewSet(BaseModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyJSONSerializer
