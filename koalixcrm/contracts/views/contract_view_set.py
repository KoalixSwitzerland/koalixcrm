"""
ContractViewSet for koalixcrm contract_object_management
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.contract import Contract
from ..serializers.contract_serializer import ContractJSONSerializer


class ContractViewSet(BaseModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return Contract.objects.all()
        if active is not None:
            return Contract.objects.filter(workspace=active)
        return Contract.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
