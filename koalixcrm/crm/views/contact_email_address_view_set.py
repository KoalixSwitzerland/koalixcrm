"""
ContactEmailAddressViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.contact import EmailAddressForContact
from koalixcrm.crm.serializers.contact_serializer import ContactEmailAddressJSONSerializer


class ContactEmailAddressViewSet(BaseModelViewSet):
    queryset = EmailAddressForContact.objects.all()
    serializer_class = ContactEmailAddressJSONSerializer
    filterset_fields = ['person']
