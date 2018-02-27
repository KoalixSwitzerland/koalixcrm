# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *

from koalixcrm.plugin import *

from django.utils import timezone

class Call(models.Model):
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relcallstaff", null=True)
    description = models.TextField(verbose_name=_("Description"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    date_due = models.DateTimeField(verbose_name=_("Date due"), default=datetime.now, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, null=True,
                                         verbose_name=_("Last modified by"), related_name="db_calllstmodified")
    status = models.CharField(verbose_name=_("Status"), max_length=1, choices=CALLSTATUS, default="P")
    
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
            return queryset.filter(date_due__lt=timezone.now()).exclude(status__in=['F','S'])
        else:
            return queryset

