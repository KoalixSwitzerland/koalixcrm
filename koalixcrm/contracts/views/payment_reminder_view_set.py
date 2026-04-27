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

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return PaymentReminder.objects.all()
        if active is not None:
            return PaymentReminder.objects.filter(workspace=active)
        return PaymentReminder.objects.none()

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
