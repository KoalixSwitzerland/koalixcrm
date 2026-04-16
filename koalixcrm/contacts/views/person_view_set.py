# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.person import Person
from koalixcrm.contacts.serializers.person_serializer import PersonJSONSerializer


class PersonViewSet(BaseModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonJSONSerializer
