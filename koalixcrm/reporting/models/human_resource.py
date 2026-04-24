# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.models.work import Work


class HumanResource(Resource):
    user = models.ForeignKey(UserExtension,
                             on_delete=models.CASCADE,
                             verbose_name=_("User"))

    def __str__(self):
        return self.user.__str__()

    def resource_contribution_project(self, date_from, date_to):
        works = Work.objects.filter(human_resource=self,
                                    date__range=(date_from, date_to))
        projects = []
        for work in works:
            if work.task.project not in projects:
                projects.append(work.task.project)
        return projects

    class Meta:
        app_label = "reporting"
        db_table = "crm_humanresource"
