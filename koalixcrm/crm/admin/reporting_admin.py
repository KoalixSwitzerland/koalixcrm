# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.reporting.models.task import Task, TaskAdminView
from koalixcrm.reporting.models.task_link_type import TaskLinkType, OptionTaskLinkType
from koalixcrm.reporting.models.task_status import TaskStatus, OptionTaskStatus
from koalixcrm.reporting.models.estimation_status import EstimationStatus, EstimationStatusAdminView
from koalixcrm.reporting.models.agreement_status import AgreementStatus, AgreementStatusAdminView
from koalixcrm.reporting.models.agreement_type import AgreementType, AgreementTypeAdminView
from koalixcrm.reporting.models.resource_type import ResourceType, ResourceTypeAdminView
from koalixcrm.reporting.models.human_resource import HumanResource, HumanResourceAdminView
from koalixcrm.reporting.models.resource_manager import ResourceManager, ResourceManagerAdminView
from koalixcrm.reporting.models.project import Project, ProjectAdminView
from koalixcrm.reporting.models.project_link_type import ProjectLinkType, OptionProjectLinkType
from koalixcrm.reporting.models.project_status import ProjectStatus, OptionProjectStatus
from koalixcrm.reporting.models.work import Work, WorkAdminView
from koalixcrm.reporting.models.reporting_period import ReportingPeriod, ReportingPeriodAdmin
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus, OptionReportingPeriodStatus

admin.site.register(Task, TaskAdminView)
admin.site.register(TaskLinkType, OptionTaskLinkType)
admin.site.register(TaskStatus, OptionTaskStatus)
admin.site.register(EstimationStatus, EstimationStatusAdminView)
admin.site.register(AgreementStatus, AgreementStatusAdminView)
admin.site.register(AgreementType, AgreementTypeAdminView)
admin.site.register(Work, WorkAdminView)
admin.site.register(HumanResource, HumanResourceAdminView)
admin.site.register(ResourceType, ResourceTypeAdminView)
admin.site.register(ResourceManager, ResourceManagerAdminView)
admin.site.register(Project, ProjectAdminView)
admin.site.register(ProjectLinkType, OptionProjectLinkType)
admin.site.register(ProjectStatus, OptionProjectStatus)
admin.site.register(ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(ReportingPeriodStatus, OptionReportingPeriodStatus)
