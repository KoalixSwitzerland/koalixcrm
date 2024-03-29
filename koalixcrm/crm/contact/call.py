# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils import timezone
from koalixcrm.crm.const.status import *


class Call(models.Model):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              verbose_name=_("Staff"),
                              related_name="db_relcallstaff",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name=_("Description"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    date_due = models.DateTimeField(verbose_name=_("Date due"),
                                    default=datetime.now,
                                    blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         blank=True,
                                         null=True,
                                         verbose_name=_("Last modified by"),
                                         related_name="db_calllstmodified")
    status = models.CharField(verbose_name=_("Status"),
                              max_length=1,
                              choices=CALLSTATUS,
                              default="P")

    def __str__(self):
        return _("Call") + " " + str(self.id)


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
