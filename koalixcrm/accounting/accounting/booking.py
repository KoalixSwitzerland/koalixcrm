# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from rest_framework import serializers
from koalixcrm.accounting.accounting.account import AccountMinimalJSONSerializer
from koalixcrm.accounting.models import Account


class Booking(models.Model):
    from_account = models.ForeignKey('Account', verbose_name=_("From Account"), related_name="db_booking_fromaccount")
    to_account = models.ForeignKey('Account', verbose_name=_("To Account"), related_name="db_booking_toaccount")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(verbose_name=_("Description"), max_length=120, null=True, blank=True)
    booking_reference = models.ForeignKey('crm.Invoice', verbose_name=_("Booking Reference"), null=True, blank=True)
    booking_date = models.DateTimeField(verbose_name=_("Booking at"))
    accounting_period = models.ForeignKey('AccountingPeriod', verbose_name=_("AccountingPeriod"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Reference Staff"), related_name="db_booking_refstaff")
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                         verbose_name=_("Last modified by"), related_name="db_booking_lstmodified")

    def booking_date_only(self):
        return self.booking_date.date()

    booking_date_only.short_description = _("Date");

    def __str__(self):
        return self.from_account.__str__() + " " + self.to_account.__str__() + " " + self.amount.__str__()

    class Meta:
        app_label = "accounting"
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')


class OptionBooking(admin.ModelAdmin):
    list_display = ('from_account',
                    'to_account',
                    'amount',
                    'booking_date_only',
                    'staff')
    fieldsets = ((_('Basic'), {'fields': ('from_account',
                                          'to_account',
                                          'amount',
                                          'booking_date',
                                          'staff',
                                          'description',
                                          'booking_reference',
                                          'accounting_period')}),)
    save_as = True

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()


class InlineBookings(admin.TabularInline):
    model = Booking
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('from_account',
                       'to_account',
                       'description',
                       'amount',
                       'booking_date',
                       'staff',
                       'booking_reference',)
        }),
    )
    allow_add = False


class BookingJSONSerializer(serializers.HyperlinkedModelSerializer):
    fromAccount = AccountMinimalJSONSerializer(source='from_account', allow_null=False)
    toAccount = AccountMinimalJSONSerializer(source='to_account', allow_null=False)
    bookingDate = serializers.DateField(source='booking_date', allow_null=False)
    booking_reference = serializers.DateField(source='booking_date', allow_null=False)

    class Meta:
        model = Booking
        fields = ('id',
                  'fromAccount',
                  'toAccount',
                  'description',
                  'amount',
                  'bookingDate',
                  'staff',
                  'bookingReference')
        depth = 1

    def create(self, validated_data):
        booking = Booking()
        booking.description = validated_data['description']
        booking.amount = validated_data['description']
        booking.bookingDate = validated_data['booking_date']
        booking.staff = validated_data['staff']
        booking.bookingReference = validated_data['booking_reference']

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

        booking.save()
        return booking

    def update(self, instance, validated_data):
        instance.description = validated_data['description']
        instance.amount = validated_data['description']
        instance.bookingDate = validated_data['booking_date']
        instance.staff = validated_data['staff']
        instance.bookingReference = validated_data['booking_reference']

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
                instance.to_account = Account.objects.get(id=to_account.get('id', None))
            else:
                instance.to_account = instance.to_account_id
        else:
            instance.to_account = None

        instance.save()
        return instance
