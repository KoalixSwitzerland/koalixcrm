# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class Resource(WorkspaceScopedModel):
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

    def __str__(self) -> str:
        from koalixcrm.reporting.models.human_resource import HumanResource
        human_resource = HumanResource.objects.get(id=self.id)
        if human_resource:
            return human_resource.__str__()
        else:
            return "Resource"

    class Meta:
        app_label = "reporting"
        db_table = "crm_resource"
