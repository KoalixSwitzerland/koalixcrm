"""
ContactPostalAddressViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.contact import PostalAddressForContact
from koalixcrm.crm.serializers.contact_serializer import ContactPostalAddressJSONSerializer


class ContactPostalAddressViewSet(BaseModelViewSet):
    queryset = PostalAddressForContact.objects.all()
    serializer_class = ContactPostalAddressJSONSerializer
    filterset_fields = ['person']
