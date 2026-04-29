# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension


class ResourceManager(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserExtension,
                             on_delete=models.CASCADE,
                             verbose_name=_("User"))

    class Meta:
        app_label = "reporting"
        db_table = "crm_resourcemanager"
