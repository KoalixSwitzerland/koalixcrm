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
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'firstName',
            'lastName')


class BookingJSONSerializer(serializers.HyperlinkedModelSerializer):

    fromAccount = OptionAccountJSONSerializer(source='from_account', allow_null=False)
    toAccount = OptionAccountJSONSerializer(source='to_account', allow_null=False)
    bookingDate = serializers.DateTimeField(source='booking_date', format="%Y-%m-%dT%H:%M", input_formats=None,
                                            allow_null=False)
    bookingReference = serializers.CharField(source='booking_reference', allow_null=True)
    accountingPeriod = OptionAccountingPeriodJSONSerializer(source='accounting_period', allow_null=False)
    staff = UserJSONSerializer(required=False, allow_null=True)

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
        request = self.context.get('request')
        koalixcrm_user = request.META.get('HTTP_KOALIXCRM_USER')
        user = User.objects.get(username=koalixcrm_user)
        booking.staff = user
        booking.last_modified_by = user

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

    def update(self, booking, validated_data):
        booking.description = validated_data['description']
        booking.amount = validated_data['amount']
        booking.booking_date = validated_data['booking_date']
        booking.booking_reference = validated_data['booking_reference']

        # Deserialize from staff
        request = self.context.get('request')
        koalixcrm_user = request.META.get('HTTP_KOALIXCRM_USER')
        user = User.objects.get(username=koalixcrm_user)
        booking.staff = user

        # Deserialize from account
        from_account = validated_data.pop('from_account')
        if from_account:
            if from_account.get('id', booking.from_account):
                booking.from_account = Account.objects.get(id=from_account.get('id', None))
            else:
                booking.from_account = booking.from_account_id
        else:
            booking.from_account = None

        # Deserialize to account
        to_account = validated_data.pop('to_account')
        if to_account:
            if to_account.get('id', booking.to_account):
                booking.to_account = Account.objects.get(id=to_account.get('id', None))
            else:
                booking.to_account = booking.to_account_id
        else:
            booking.to_account = None

        # Deserialize to accounting period
        accounting_period = validated_data.pop('accounting_period')
        if accounting_period:
            if accounting_period.get('id', booking.accounting_period):
                booking.accounting_period = AccountingPeriod.objects.get(id=accounting_period.get('id', None))
            else:
                booking.accounting_period = booking.accounting_period_id
        else:
            booking.accounting_period = None

        booking.save()
        return booking
