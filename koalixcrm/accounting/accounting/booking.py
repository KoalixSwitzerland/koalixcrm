# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext as _


class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, verbose_name=_("To Account"), related_name="db_booking_toaccount")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(verbose_name=_("Description"), max_length=120, null=True, blank=True)
    booking_reference = models.ForeignKey('crm.Invoice', on_delete=models.CASCADE, verbose_name=_("Booking Reference"), null=True, blank=True)
    booking_date = models.DateTimeField(verbose_name=_("Booking at"))
    accounting_period = models.ForeignKey('AccountingPeriod', on_delete=models.CASCADE, verbose_name=_("AccountingPeriod"))
    staff = models.ForeignKey('auth.User', on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Reference Staff"), related_name="db_booking_refstaff")
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    last_modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, blank=True,
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
