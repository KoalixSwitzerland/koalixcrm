"""
CustomerGroupViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.customer_group import CustomerGroup
from koalixcrm.contacts.serializers.customer_group_serializer import CustomerGroupJSONSerializer


class CustomerGroupViewSet(BaseModelViewSet):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupJSONSerializer
