# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _

from koalixcrm.plugin import *

class Visit(models.Model):
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relvisitstaff", null=True)
    description = models.TextField(verbose_name=_("Description"))
    default_customer = models.ForeignKey("Customer", verbose_name=_("Default Customer"), null=True, blank=True)
    default_supplier = models.ForeignKey("Supplier", verbose_name=_("Default Supplier"), null=True, blank=True)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet", verbose_name=_("Default Template Set"), null=True, blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"), related_name="db_visitlstmodified")
    
    def __str__(self):
        return _("Call") + " " + str(self.id)

class OptionVisit(admin.ModelAdmin):
    list_display = ('id',)