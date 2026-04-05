"""
ContractViewSet for koalixcrm contract_object_management
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from ..models.contract import Contract
from ..serializers.contract_serializer import ContractJSONSerializer


class ContractViewSet(BaseModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer
