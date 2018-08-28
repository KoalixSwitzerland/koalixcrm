# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from koalixcrm.accounting.accounting.accounting_period import AccountingPeriod
from koalixcrm.accounting.accounting.booking import Booking
from koalixcrm.accounting.models import Account
from koalixcrm.accounting.rest.account_rest import OptionAccountJSONSerializer
from koalixcrm.accounting.rest.accounting_period_rest import OptionAccountingPeriodJSONSerializer


class UserJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username')


class BookingJSONSerializer(serializers.HyperlinkedModelSerializer):
    fromAccount = OptionAccountJSONSerializer(source='from_account', allow_null=False)
    toAccount = OptionAccountJSONSerializer(source='to_account', allow_null=False)
    bookingDate = serializers.DateTimeField(source='booking_date', format="%Y-%m-%dT%H:%M", input_formats=None,
                                            allow_null=False)
    bookingReference = serializers.CharField(source='booking_reference', allow_null=True)
    accountingPeriod = OptionAccountingPeriodJSONSerializer(source='accounting_period', allow_null=False)
    staff = UserJSONSerializer(allow_null=False)

    class Meta:
        model = Booking
        fields = ('id',
                  'fromAccount',
                  'toAccount',
                  'description',
                  'amount',
                  'bookingDate',
                  'staff',
                  'bookingReference',
                  'accountingPeriod')
        depth = 1

    def create(self, validated_data):
        booking = Booking()
        booking.description = validated_data['description']
        booking.amount = validated_data['amount']
        booking.booking_date = validated_data['booking_date']
        booking.booking_reference = validated_data['booking_reference']

        # Deserialize from staff
        staff = validated_data.pop('staff')
        if staff:
            if staff.get('id', None):
                user = User.objects.get(id=staff.get('id', None))

                booking.staff = user
                booking.last_modified_by = user
            else:
                booking.staff = None

        # Deserialize from account
        from_account = validated_data.pop('from_account')
        if from_account:
            if from_account.get('id', None):
                booking.from_account = Account.objects.get(id=from_account.get('id', None))
            else:
                booking.from_account = None

        # Deserialize to account
        to_account = validated_data.pop('to_account')
        if to_account:
            if to_account.get('id', None):
                booking.to_account = Account.objects.get(id=to_account.get('id', None))
            else:
                booking.to_account = None

        # Deserialize to accounting period
        accounting_period = validated_data.pop('accounting_period')
        if accounting_period:
            if accounting_period.get('id', None):
                booking.accounting_period = AccountingPeriod.objects.get(id=accounting_period.get('id', None))
            else:
                booking.accounting_period = None

        booking.save()
        return booking

    def update(self, instance, validated_data):
        instance.description = validated_data['description']
        instance.amount = validated_data['amount']
        instance.booking_date = validated_data['booking_date']
        instance.booking_reference = validated_data['booking_reference']

        # Deserialize from staff
        staff = validated_data.pop('staff')
        if staff:
            if staff.get('id', instance.staff):
                instance.staff = User.objects.get(id=staff.get('id', None))
            else:
                instance.staff = instance.staff_id
        else:
            instance.staff = None

        # Deserialize from account
        from_account = validated_data.pop('from_account')
        if from_account:
            if from_account.get('id', instance.from_account):
                instance.from_account = Account.objects.get(id=from_account.get('id', None))
            else:
                instance.from_account = instance.from_account_id
        else:
            instance.from_account = None

        # Deserialize to account
        to_account = validated_data.pop('to_account')
        if to_account:
            if to_account.get('id', instance.to_account):
                user = User.objects.get(id=staff.get('id', None))

                instance.staff = user
                instance.last_modified_by = user
            else:
                instance.to_account = instance.to_account_id
        else:
            instance.to_account = None

        # Deserialize to accounting period
        accounting_period = validated_data.pop('accounting_period')
        if accounting_period:
            if accounting_period.get('id', instance.accounting_period):
                instance.accounting_period = AccountingPeriod.objects.get(id=accounting_period.get('id', None))
            else:
                instance.accounting_period = instance.accounting_period_id
        else:
            instance.accounting_period = None

        instance.save()
        return instance
