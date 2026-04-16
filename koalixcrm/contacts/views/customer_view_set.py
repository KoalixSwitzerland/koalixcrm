"""
CustomerViewSet for koalixcrm crm
"""
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.customer import Customer
from koalixcrm.contacts.serializers.customer_serializer import CustomerJSONSerializer
from koalixcrm.core.views.renderer import XSLFORenderer


class CustomerViewSet(BaseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerJSONSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer, XSLFORenderer]
