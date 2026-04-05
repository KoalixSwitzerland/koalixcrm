# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.crm.contact.person import Person


class PersonJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
