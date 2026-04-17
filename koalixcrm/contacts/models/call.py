# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.core.const.status import CALLSTATUS


class Call(models.Model):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              verbose_name=_("Staff"),
                              related_name="db_relcallstaff",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name=_("Description"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    date_due = models.DateTimeField(verbose_name=_("Date due"),
                                    default=datetime.now,
                                    blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         blank=True,
                                         null=True,
                                         verbose_name=_("Last modified by"),
                                         related_name="db_calllstmodified")
    status = models.CharField(verbose_name=_("Status"),
                              max_length=1,
                              choices=CALLSTATUS,
                              default="P")

    def __str__(self):
        return _("Call") + " " + str(self.id)

    class Meta:
        app_label = "contacts"
        db_table = "crm_call"


