# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.crm.contact.contact import Contact, PhoneAddressForContact, PostalAddressForContact, \
    EmailAddressForContact
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.phone_address import PhoneAddress


class PhoneNumberJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneAddress
        fields = ('phone',)


class ContactPhoneNumberJSONSerializer(PhoneNumberJSONSerializer):
    class Meta:
        model = PhoneAddressForContact
        fields = PhoneNumberJSONSerializer.Meta.fields + ('purpose',)


class PostalAddressJSONSerializer(serializers.HyperlinkedModelSerializer):
    preName = serializers.CharField(source='pre_name')
    addressLine1 = serializers.CharField(source='address_line_1')
    addressLine2 = serializers.CharField(source='address_line_2')
    addressLine3 = serializers.CharField(source='address_line_3')
    addressLine4 = serializers.CharField(source='address_line_4')
    zipCode = serializers.IntegerField(source='zip_code')

    class Meta:
        model = PhoneAddress
        fields = ('prefix',
                  'name',
                  'preName',
                  'addressLine1',
                  'addressLine2',
                  'addressLine3',
                  'addressLine4',
                  'zipCode',
                  'town',
                  'state',
                  'country')


class ContactPostalAddressJSONSerializer(PostalAddressJSONSerializer):
    class Meta:
        model = PostalAddressForContact
        fields = PostalAddressJSONSerializer.Meta.fields + ('purpose',)


class EmailAddressJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ('email',)


class ContactEmailAddressJSONSerializer(EmailAddressJSONSerializer):
    class Meta:
        model = EmailAddressForContact
        fields = EmailAddressJSONSerializer.Meta.fields + ('purpose',)


class ContactJSONSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField('get_town')
    stockDetails = serializers.SerializerMethodField('get_stock_details')

    class Meta:
        model = Contact
        fields = ('name',
                  'state',
                  'city')

    @staticmethod
    def get_postal_address(obj):
        return PostalAddressForContact.objects.filter(person=obj.id).first()

    def get_state(self, obj):
        address = self.get_postal_address(obj)
        return address.state if address is not None else None

    def get_town(self, obj):
        address = self.get_postal_address(obj)
        return address.town if address is not None else None
