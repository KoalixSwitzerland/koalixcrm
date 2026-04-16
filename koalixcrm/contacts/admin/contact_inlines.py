# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.contacts.models.contact import (
    PostalAddressForContact,
    PhoneAddressForContact,
    EmailAddressForContact,
    CallForContact,
    VisitForContact,
    ContactPersonAssociation,
)
from koalixcrm.core.inlinemixin import LimitedAdminInlineMixin


class ContactPostalAddress(admin.StackedInline):
    model = PostalAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('prefix',
                       'pre_name',
                       'name',
                       'address_line_1',
                       'address_line_2',
                       'address_line_3',
                       'address_line_4',
                       'zip_code',
                       'town',
                       'state',
                       'country',
                       'purpose')
        }),
    )
    allow_add = True


class ContactPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContactEmailAddress(admin.TabularInline):
    model = EmailAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class PeopleInlineAdmin(admin.TabularInline):
    model = ContactPersonAssociation
    extra = 0
    show_change_link = True


class ContactCall(LimitedAdminInlineMixin, admin.StackedInline):
    model = CallForContact
    extra = 0
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
                'description',
                'date_due',
                'purpose',
                'status',
                'cperson',)
        }),
    )
    allow_add = True

    def get_filters(self, request, obj):
        return getattr(self, 'filters', ()) if obj is None else (('cperson', dict(companies=obj.id)),)


class ContactVisit(LimitedAdminInlineMixin, admin.StackedInline):
    model = VisitForContact
    extra = 0
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
                'description',
                'date_due',
                'purpose',
                'status',
                'cperson',
                'ref_call',)
        }),
    )
    allow_add = True

    def get_filters(self, request, obj):
        return getattr(self, 'filters', ()) if obj is None else (('cperson', dict(companies=obj.id)),('ref_call', dict(company=obj.id, status='S')))


class StateFilter(admin.SimpleListFilter):
    title = _('State')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        items = []
        for a in PostalAddressForContact.objects.values('state').distinct():
            if a['state']:
                items.append((a['state'], _(a['state'])))
        return (
            items
        )

    def queryset(self, request, queryset):
        if self.value():
            matching_addresses = PostalAddressForContact.objects.filter(state=self.value())
            ids = [a.person.id for a in matching_addresses]
            return queryset.filter(pk__in=ids)
        return queryset


class CityFilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        items = []
        state = request.GET.get('state', None)
        unique_list = PostalAddressForContact.objects.all().order_by('town')
        adjusted_queryset = unique_list if state is None else unique_list.filter(state=state)
        for a in adjusted_queryset.values('town').distinct():
            if a['town']:
                items.append((a['town'], _(a['town'])))
        return (
            items
        )

    def queryset(self, request, queryset):
        if self.value():
            matching_addresses = PostalAddressForContact.objects.filter(town=self.value())
            ids = [(a.person.id) for a in matching_addresses]
            return queryset.filter(pk__in=ids)
        return queryset
