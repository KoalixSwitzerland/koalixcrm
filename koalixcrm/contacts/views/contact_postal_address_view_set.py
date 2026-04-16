"""
ContactPostalAddressViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.contact import PostalAddressForContact
from koalixcrm.contacts.serializers.contact_serializer import ContactPostalAddressJSONSerializer


class ContactPostalAddressViewSet(BaseModelViewSet):
    queryset = PostalAddressForContact.objects.all()
    serializer_class = ContactPostalAddressJSONSerializer
    filterset_fields = ['person']
