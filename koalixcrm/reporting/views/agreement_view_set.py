"""
AgreementViewSet for koalixcrm reporting
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin

from ..models.agreement import Agreement
from ..serializers.agreement_serializer import AgreementJSONSerializer


class AgreementViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementJSONSerializer
