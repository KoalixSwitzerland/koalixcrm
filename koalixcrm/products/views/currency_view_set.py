"""
CurrencyViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.currency import Currency
from ..serializers.currency_serializer import CurrencyJSONSerializer


class CurrencyViewSet(BaseModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyJSONSerializer
