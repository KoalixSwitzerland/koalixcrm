# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import gettext as _
from koalixcrm.contacts.models.person import Person
from koalixcrm.contacts.models.contact import ContactPersonAssociation


class CompaniesInlineAdmin(admin.TabularInline):
    model = ContactPersonAssociation
    extra = 0
    show_change_link = True


class OptionPerson(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'pre_name',
                    'email',
                    'role',
                    'get_companies',)
    fieldsets = (('', {'fields': ('prefix',
                                  'name',
                                  'pre_name',
                                  'role',
                                  'email',
                                  'phone',)}),)
    allow_add = True
    inlines = [CompaniesInlineAdmin]

    def get_companies(self, obj):
        items = []
        for c in obj.companies.all():
            items.append(c.name)
        return ','.join(items)

    get_companies.short_description = _("Works at")


admin.site.register(Person, OptionPerson)
