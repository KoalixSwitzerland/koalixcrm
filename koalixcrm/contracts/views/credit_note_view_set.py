# -*- coding: utf-8 -*-
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
