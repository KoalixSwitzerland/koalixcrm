# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Work(models.Model):
    employee = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    date =models.DateField(verbose_name=_("Date"), blank=False, null=False)
    start_time = models.TimeField(verbose_name=_("Start Time"), blank=False, null=False)
    stop_time = models.TimeField(verbose_name=_("Stop Time"), blank=False, null=False)
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=300, blank=False, null=False)
    description = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    task = models.ForeignKey("Task", verbose_name=_('Task'), blank=False, null=False)
    work_category = models.ForeignKey("WorkCategory", verbose_name=_('Work Category'), blank=False, null=False)

    @staticmethod
    def get_sum_of_effort(task):
        Work.objects.filter(task=task)


    def __str__(self):
        return _("Work") + ": " + str(self.id) + " " + _("from Person") + ": " + str(self.employee.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Work')
        verbose_name_plural = _('Work')


