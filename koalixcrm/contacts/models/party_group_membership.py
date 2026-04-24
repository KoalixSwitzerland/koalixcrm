# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.contacts.models.party_group import PartyGroup
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class PartyGroupMembership(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE,
        related_name='group_memberships',
        verbose_name=_("Party"),
    )
    party_group = models.ForeignKey(
        PartyGroup, on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_("Party group"),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_partygroupmembership"
        verbose_name = _("Party group membership")
        verbose_name_plural = _("Party group memberships")

    def __str__(self):
        return f"{self.party_id}@{self.party_group_id}"
