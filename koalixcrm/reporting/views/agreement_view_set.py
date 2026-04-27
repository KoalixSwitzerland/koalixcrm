"""
AgreementViewSet for koalixcrm reporting
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.agreement import Agreement
from ..serializers.agreement_serializer import AgreementJSONSerializer


class AgreementViewSet(BaseModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementJSONSerializer
