# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.contact import Contact
from koalixcrm.crm.serializers.contact_serializer import ContactJSONSerializer


class ContactViewSet(BaseModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactJSONSerializer
