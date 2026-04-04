# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.crm.reporting.task import Task, TaskAdminView
from koalixcrm.crm.reporting.task_link_type import TaskLinkType, OptionTaskLinkType
from koalixcrm.crm.reporting.task_status import TaskStatus, OptionTaskStatus
from koalixcrm.crm.reporting.estimation_status import EstimationStatus, EstimationStatusAdminView
from koalixcrm.crm.reporting.agreement_status import AgreementStatus, AgreementStatusAdminView
from koalixcrm.crm.reporting.agreement_type import AgreementType, AgreementTypeAdminView
from koalixcrm.crm.reporting.resource_type import ResourceType, ResourceTypeAdminView
from koalixcrm.crm.reporting.human_resource import HumanResource, HumanResourceAdminView
from koalixcrm.crm.reporting.resource_manager import ResourceManager, ResourceManagerAdminView
from koalixcrm.crm.reporting.project import Project, ProjectAdminView
from koalixcrm.crm.reporting.project_link_type import ProjectLinkType, OptionProjectLinkType
from koalixcrm.crm.reporting.project_status import ProjectStatus, OptionProjectStatus
from koalixcrm.crm.reporting.work import Work, WorkAdminView
from koalixcrm.crm.reporting.reporting_period import ReportingPeriod, ReportingPeriodAdmin
from koalixcrm.crm.reporting.reporting_period_status import ReportingPeriodStatus, OptionReportingPeriodStatus

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
