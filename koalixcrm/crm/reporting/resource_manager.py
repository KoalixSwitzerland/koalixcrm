# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from koalixcrm.djangoUserExtension.user_extension.user_extension import UserExtension
from django.utils.translation import ugettext as _


class ResourceManager(models.Model):
    user = models.ForeignKey(UserExtension,
                             on_delete=models.CASCADE,
                             verbose_name=_("User"))


class ResourceManagerAdminView(admin.ModelAdmin):
    list_display = ('id',
                    'user',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('user',)
        }),
    )
