# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin


class ResourceType(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=300,
                             blank=False,
                             null=False)
    description = models.TextField(verbose_name=_("Text"),
                                   blank=True,
                                   null=True)

    def __str__(self):
        return str(self.id) + " " + str(self.title)

    class Meta:
        app_label = "crm"
        verbose_name = _('Resource Link Type')
        verbose_name_plural = _('Resource Link Type')


class ResourceTypeAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'description')

    fieldsets = (
        (_('ResourceType'), {
            'fields': ('title',
                       'description')
        }),
    )
    save_as = True
