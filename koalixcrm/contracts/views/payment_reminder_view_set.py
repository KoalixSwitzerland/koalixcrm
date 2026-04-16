# -*- coding: utf-8 -*-
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.serializers.nested_commercial_document import (
    PaymentReminderNestedSerializer,
)
from koalixcrm.contracts.serializers.payment_reminder_serializer import (
    PaymentReminderJSONSerializer,
)
from koalixcrm.contracts.views.nested_detail_mixin import NestedDetailMixin
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class PaymentReminderViewSet(NestedDetailMixin, BaseModelViewSet):
    queryset = PaymentReminder.objects.all()
    serializer_class = PaymentReminderJSONSerializer
    nested_serializer_class = PaymentReminderNestedSerializer
