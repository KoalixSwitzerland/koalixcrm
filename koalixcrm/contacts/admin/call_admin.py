# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils import timezone
from koalixcrm.contacts.models.contact import CallForContact, VisitForContact


class CallOverdueFilter(admin.SimpleListFilter):
    title = _('Is call overdue')
    parameter_name = 'date_due'

    def lookups(self, request, model_admin):
        return (
            ('overdue', _('Overdue')),
            ('planned', _('Planned')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'planned':
            return queryset.filter(date_due__gt=timezone.now())
        elif self.value() == 'overdue':
            return queryset.filter(date_due__lt=timezone.now()).exclude(status__in=['F', 'S'])
        else:
            return queryset


class OptionCall(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'date_due',
                    'purpose',
                    'status',
                    'cperson',
                    'is_call_overdue',
                    'get_contact_name')
    fieldsets = (('', {'fields': ('staff',
                                  'description',
                                  'date_due',
                                  'purpose',
                                  'company',
                                  'cperson',
                                  'status')}),)
    list_filter = [CallOverdueFilter]

    @staticmethod
    def get_contact_name(obj):
        return obj.company.name

    get_contact_name.short_description = _("Company")

    @staticmethod
    def is_call_overdue(obj):
        if obj.date_due < timezone.now() and obj.status not in ['F', 'S']:
            overdue = True
        else:
            overdue = False
        return overdue

    is_call_overdue.short_description = _("Is call overdue")


class OptionVisit(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'cperson',
                    'date_due',
                    'purpose',
                    'get_contact_name',
                    'status',
                    'ref_call',)
    fieldsets = (('', {'fields': ('staff',
                                  'description',
                                  'date_due',
                                  'purpose',
                                  'company',
                                  'cperson',
                                  'status')}),)

    @staticmethod
    def get_contact_name(obj):
        return obj.company.name

    get_contact_name.short_description = _("Company")


admin.site.register(CallForContact, OptionCall)
admin.site.register(VisitForContact, OptionVisit)
