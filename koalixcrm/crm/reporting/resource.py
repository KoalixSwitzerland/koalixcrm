# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _


class Resource(models.Model):
    id = models.BigAutoField(primary_key=True)
    resource_manager = models.ForeignKey("ResourceManager",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Manager"),
                                         blank=True,
                                         null=True)
    resource_type = models.ForeignKey("ResourceType",
                                      on_delete=models.CASCADE,
                                      verbose_name=_("Resource Type"),
                                      blank=True,
                                      null=True)

    def __str__(self):
        from koalixcrm.crm.reporting.human_resource import HumanResource
        human_resource = HumanResource.objects.get(id=self.id)
        if human_resource:
            return human_resource.__str__()
        else:
            return "Resource"

