# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.delivery_note import DeliveryNote
from koalixcrm.contracts.serializers.delivery_note_serializer import DeliveryNoteJSONSerializer


class DeliveryNoteViewSet(BaseModelViewSet):
    queryset = DeliveryNote.objects.all()
    serializer_class = DeliveryNoteJSONSerializer
