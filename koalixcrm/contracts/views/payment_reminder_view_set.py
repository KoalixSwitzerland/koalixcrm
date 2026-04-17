# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.serializers.payment_reminder_serializer import PaymentReminderJSONSerializer


class PaymentReminderViewSet(BaseModelViewSet):
    queryset = PaymentReminder.objects.all()
    serializer_class = PaymentReminderJSONSerializer
