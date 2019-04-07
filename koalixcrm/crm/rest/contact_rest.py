# -*- coding: utf-8 -*-
from rest_framework import serializers

from koalixcrm.crm.contact.contact import Contact, PhoneAddressForContact, PostalAddressForContact, \
    EmailAddressForContact
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.postal_address import PostalAddress


class PhoneAddressJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneAddress
        fields = ('phone',)


class ContactPhoneAddressJSONSerializer(PhoneAddressJSONSerializer):
    contactId = serializers.PrimaryKeyRelatedField(source='person_id', queryset=Contact.objects.all())

    class Meta:
        model = PhoneAddressForContact
        fields = PhoneAddressJSONSerializer.Meta.fields + ('id', 'purpose', 'contactId')

    def create(self, validated_data):
        contact_phone_address = PhoneAddressForContact()

        contact = validated_data.pop('person_id')
        contact_phone_address.person_id = contact.id
        contact_phone_address.purpose = validated_data['purpose']
        contact_phone_address.phone = validated_data['phone']

        contact_phone_address.save()
        return contact_phone_address

    def update(self, contact_phone_address, validated_data):
        contact = validated_data.pop('person_id')
        contact_phone_address.person_id = contact.id
        contact_phone_address.purpose = validated_data['purpose']
        contact_phone_address.prefix = validated_data['phone']

        contact_phone_address.save()

        return contact_phone_address


class EmailAddressJSONSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ('email',)


class ContactEmailAddressJSONSerializer(EmailAddressJSONSerializer):
    contactId = serializers.PrimaryKeyRelatedField(source='person_id', queryset=Contact.objects.all())

    class Meta:
        model = EmailAddressForContact
        fields = EmailAddressJSONSerializer.Meta.fields + ('id', 'purpose', 'contactId')

    def create(self, validated_data):
        contact_email_address = EmailAddressForContact()

        contact = validated_data.pop('person_id')
        contact_email_address.person_id = contact.id
        contact_email_address.purpose = validated_data['purpose']
        contact_email_address.email = validated_data['email']

        contact_email_address.save()
        return contact_email_address

    def update(self, contact_email_address, validated_data):
        contact = validated_data.pop('person_id')
        contact_email_address.person_id = contact.id
        contact_email_address.purpose = validated_data['purpose']
        contact_email_address.email = validated_data['email']

        contact_email_address.save()

        return contact_email_address


class ContactJSONSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField('get_town')

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


class PostalAddressJSONSerializer(serializers.HyperlinkedModelSerializer):
    givenName = serializers.CharField(source='pre_name', allow_null=True)
    familyName = serializers.CharField(source='name', allow_null=True)
    addressLine1 = serializers.CharField(source='address_line_1', allow_null=True)
    addressLine2 = serializers.CharField(source='address_line_2', allow_null=True)
    addressLine3 = serializers.CharField(source='address_line_3', allow_null=True)
    addressLine4 = serializers.CharField(source='address_line_4', allow_null=True)
    zipCode = serializers.IntegerField(source='zip_code',  allow_null=True)
    city = serializers.CharField(source='town',  allow_null=True)

    class Meta:
        model = PostalAddress
        fields = ('prefix',
                  'familyName',
                  'givenName',
                  'addressLine1',
                  'addressLine2',
                  'addressLine3',
                  'addressLine4',
                  'zipCode',
                  'city',
                  'state',
                  'country')


class ContactPostalAddressJSONSerializer(PostalAddressJSONSerializer):
    contactId = serializers.PrimaryKeyRelatedField(source='person_id', queryset=Contact.objects.all())

    class Meta:
        model = PostalAddressForContact
        fields = PostalAddressJSONSerializer.Meta.fields + ('id', 'purpose', 'contactId')

    def create(self, validated_data):
        contact_postal_address = PostalAddressForContact()

        contact = validated_data.pop('person_id')
        contact_postal_address.person_id = contact.id
        contact_postal_address.purpose = validated_data['purpose']
        contact_postal_address.prefix = validated_data['prefix']
        contact_postal_address.name = validated_data['name']
        contact_postal_address.name = validated_data['pre_name']
        contact_postal_address.address_line_1 = validated_data['address_line_1']
        contact_postal_address.address_line_2 = validated_data['address_line_2']
        contact_postal_address.address_line_3 = validated_data['address_line_3']
        contact_postal_address.address_line_4 = validated_data['address_line_4']
        contact_postal_address.zip_code = validated_data['zip_code']
        contact_postal_address.town = validated_data['town']
        contact_postal_address.state = validated_data['state']
        contact_postal_address.country = validated_data['country']

        contact_postal_address.save()
        return contact_postal_address

    def update(self, contact_postal_address, validated_data):
        contact = validated_data.pop('person_id')
        contact_postal_address.person_id = contact.id
        contact_postal_address.purpose = validated_data['purpose']
        contact_postal_address.prefix = validated_data['prefix']
        contact_postal_address.name = validated_data['name']
        contact_postal_address.pre_name = validated_data['pre_name']
        contact_postal_address.address_line_1 = validated_data['address_line_1']
        contact_postal_address.address_line_2 = validated_data['address_line_2']
        contact_postal_address.address_line_3 = validated_data['address_line_3']
        contact_postal_address.address_line_4 = validated_data['address_line_4']
        contact_postal_address.zip_code = validated_data['zip_code']
        contact_postal_address.town = validated_data['town']
        contact_postal_address.state = validated_data['state']
        contact_postal_address.country = validated_data['country']

        contact_postal_address.save()

        return contact_postal_address

