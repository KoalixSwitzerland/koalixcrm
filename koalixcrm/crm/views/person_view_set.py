# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.serializers.person_serializer import PersonJSONSerializer


class PersonViewSet(BaseModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonJSONSerializer
