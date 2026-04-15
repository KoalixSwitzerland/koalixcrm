# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.credit_note import CreditNote
from koalixcrm.contracts.serializers.credit_note_serializer import CreditNoteJSONSerializer


class CreditNoteViewSet(BaseModelViewSet):
    queryset = CreditNote.objects.all()
    serializer_class = CreditNoteJSONSerializer
