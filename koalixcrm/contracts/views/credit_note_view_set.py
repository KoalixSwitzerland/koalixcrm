# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db.models import QuerySet
from rest_framework.serializers import BaseSerializer

from koalixcrm.contracts.models.credit_note import CreditNote
from koalixcrm.contracts.serializers.credit_note_serializer import (
    CreditNoteJSONSerializer,
)
from koalixcrm.contracts.serializers.nested_commercial_document import (
    CreditNoteNestedSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class CreditNoteViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteJSONSerializer
    nested_serializer_class = CreditNoteNestedSerializer

    def get_queryset(self) -> QuerySet[CreditNote]:
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return CreditNote.objects.all()
        if active is not None:
            return CreditNote.objects.filter(workspace=active)
        return CreditNote.objects.none()

    def perform_create(self, serializer: BaseSerializer) -> None:
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
