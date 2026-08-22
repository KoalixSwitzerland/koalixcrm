"""
CustomerBillingCycleViewSet for koalixcrm crm
"""
from __future__ import annotations

from koalixcrm.contacts.models.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.contacts.serializers.customer_billing_cycle_serializer import (
    CustomerBillingCycleJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class CustomerBillingCycleViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    queryset = CustomerBillingCycle.objects.all()
    serializer_class = CustomerBillingCycleJSONSerializer
