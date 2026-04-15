# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension, OptionUserExtension
from koalixcrm.djangoUserExtension.models.template_set import TemplateSet, OptionTemplateSet

admin.site.register(UserExtension, OptionUserExtension)
admin.site.register(TemplateSet, OptionTemplateSet)
