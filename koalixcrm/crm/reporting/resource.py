# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Resource(models.Model):
    resource_manager = models.ForeignKey("ResourceManager",
                                         verbose_name=_("Manager"),
                                         blank=True,
                                         null=True)
    resource_type = models.ForeignKey("ResourceType",
                                      verbose_name=_("Resource Type"),
                                      blank=True,
                                      null=True)
