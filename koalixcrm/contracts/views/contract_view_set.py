"""
ContractViewSet for koalixcrm contract_object_management
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.contract import Contract
from ..serializers.contract_serializer import ContractJSONSerializer
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class ContractViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    """Contracts are workspace-scoped; the mixin owns the filter and the stamp.

    It used to carry its own copy of both, including a superuser branch that
    returned every workspace's contracts and a ``get_or_create('Default
    Workspace')`` on the write path. REQ-0028 removes both: the object filter
    applies to unrestricted actors too (AC-9), and no code path invents a
    tenant (AC-10).
    """

    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer
