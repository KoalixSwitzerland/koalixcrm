"""
CustomerViewSet for koalixcrm crm
"""
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.customer import Customer
from koalixcrm.crm.serializers.customer_serializer import CustomerJSONSerializer
from koalixcrm.crm.views.renderer import XSLFORenderer


class CustomerViewSet(BaseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerJSONSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer, XMLRenderer, XSLFORenderer]
