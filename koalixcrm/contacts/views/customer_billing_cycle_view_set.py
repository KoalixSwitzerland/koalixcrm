"""
CustomerBillingCycleViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts.serializers.customer_billing_cycle_serializer import CustomerBillingCycleJSONSerializer


class CustomerBillingCycleViewSet(BaseModelViewSet):
    queryset = CustomerBillingCycle.objects.all()
    serializer_class = CustomerBillingCycleJSONSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return qs.filter(workspace=active)
        if not self.request.user.is_superuser:
            return qs.none()
        return qs

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
