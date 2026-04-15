"""
CustomerBillingCycleViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.customer_billing_cycle import CustomerBillingCycle
from koalixcrm.crm.serializers.customer_billing_cycle_serializer import CustomerBillingCycleJSONSerializer


class CustomerBillingCycleViewSet(BaseModelViewSet):
    queryset = CustomerBillingCycle.objects.all()
    serializer_class = CustomerBillingCycleJSONSerializer
