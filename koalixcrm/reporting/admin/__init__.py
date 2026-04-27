# -*- coding: utf-8 -*-

from django.contrib import admin

from koalixcrm.reporting.admin.agreement_status_admin import AgreementStatusAdminView
from koalixcrm.reporting.admin.agreement_type_admin import AgreementTypeAdminView
from koalixcrm.reporting.admin.estimation_status_admin import EstimationStatusAdminView
from koalixcrm.reporting.admin.human_resource_admin import HumanResourceAdminView
from koalixcrm.reporting.admin.project_admin import ProjectAdminView
from koalixcrm.reporting.admin.project_link_type_admin import OptionProjectLinkType
from koalixcrm.reporting.admin.project_status_admin import OptionProjectStatus
from koalixcrm.reporting.admin.reporting_period_admin import ReportingPeriodAdmin
from koalixcrm.reporting.admin.reporting_period_status_admin import (
    OptionReportingPeriodStatus,
)
from koalixcrm.reporting.admin.resource_manager_admin import ResourceManagerAdminView
from koalixcrm.reporting.admin.resource_type_admin import ResourceTypeAdminView
from koalixcrm.reporting.admin.task_admin import TaskAdminView
from koalixcrm.reporting.admin.task_link_type_admin import OptionTaskLinkType
from koalixcrm.reporting.admin.task_status_admin import OptionTaskStatus
from koalixcrm.reporting.admin.work_admin import WorkAdminView
from koalixcrm.reporting.models.agreement_status import AgreementStatus
from koalixcrm.reporting.models.agreement_type import AgreementType
from koalixcrm.reporting.models.estimation_status import EstimationStatus
from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.models.project_link_type import ProjectLinkType
from koalixcrm.reporting.models.project_status import ProjectStatus
from koalixcrm.reporting.models.reporting_period import ReportingPeriod
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus
from koalixcrm.reporting.models.resource_manager import ResourceManager
from koalixcrm.reporting.models.resource_type import ResourceType
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.models.task_link_type import TaskLinkType
from koalixcrm.reporting.models.task_status import TaskStatus
from koalixcrm.reporting.models.work import Work

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

# Extend Contract admin to include reporting inlines
from koalixcrm.contracts.admin.contract_admin import OptionContract
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.reporting.admin.generic_project_link_admin import (
    InlineGenericProjectLinkAdmin,
)

admin.site.unregister(Contract)


class ExtendedContractAdmin(OptionContract):
    inlines = OptionContract.inlines + [InlineGenericProjectLinkAdmin]


admin.site.register(Contract, ExtendedContractAdmin)
