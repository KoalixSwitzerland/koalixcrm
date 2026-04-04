"""
TaxViewSet for koalixcrm products
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.tax import Tax
from ..serializers.tax_serializer import TaxJSONSerializer


class TaxViewSet(BaseModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxJSONSerializer
