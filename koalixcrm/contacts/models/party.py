# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.const.party import LANGUAGE_CHOICES


class Party(models.Model):
    id = models.BigAutoField(primary_key=True)
    display_name = models.CharField(max_length=300, verbose_name=_("Display name"))
    default_language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES,
        blank=True, null=True,
        verbose_name=_("Default language"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    last_modified_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        limit_choices_to={'is_staff': True},
        blank=True, null=True,
        verbose_name=_("Last modified by"),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_party"
        verbose_name = _("Party")
        verbose_name_plural = _("Parties")

    def __str__(self):
        return self.display_name
