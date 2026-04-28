"""
TaxViewSet for koalixcrm settings
"""

from __future__ import annotations

from koalixcrm.core.models.tax import Tax
from koalixcrm.core.serializers.tax_serializer import TaxJSONSerializer
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class TaxViewSet(BaseModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxJSONSerializer
