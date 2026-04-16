"""
ContactEmailAddressViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.contact import EmailAddressForContact
from koalixcrm.contacts.serializers.contact_serializer import ContactEmailAddressJSONSerializer


class ContactEmailAddressViewSet(BaseModelViewSet):
    queryset = EmailAddressForContact.objects.all()
    serializer_class = ContactEmailAddressJSONSerializer
    filterset_fields = ['person']
