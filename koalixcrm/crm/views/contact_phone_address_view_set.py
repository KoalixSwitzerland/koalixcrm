"""
ContactPhoneAddressViewSet for koalixcrm crm
"""
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.contact import PhoneAddressForContact
from koalixcrm.crm.serializers.contact_serializer import ContactPhoneAddressJSONSerializer


class ContactPhoneAddressViewSet(BaseModelViewSet):
    queryset = PhoneAddressForContact.objects.all()
    serializer_class = ContactPhoneAddressJSONSerializer
    filterset_fields = ['person']
