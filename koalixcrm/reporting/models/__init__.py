# -*- coding: utf-8 -*-

from koalixcrm.reporting.models.agreement import Agreement, AgreementInlineAdminView
from koalixcrm.reporting.models.agreement_status import AgreementStatus, AgreementStatusAdminView
from koalixcrm.reporting.models.agreement_type import AgreementType, AgreementTypeAdminView
from koalixcrm.reporting.models.estimation import Estimation, EstimationInlineAdminView
from koalixcrm.reporting.models.estimation_status import EstimationStatus, EstimationStatusAdminView
from koalixcrm.reporting.models.generic_project_link import GenericProjectLink, GenericLinkInlineAdminView, InlineGenericProjectLink
from koalixcrm.reporting.models.generic_task_link import GenericTaskLink, InlineGenericTaskLink
from koalixcrm.reporting.models.human_resource import HumanResource, HumanResourceAdminView
from koalixcrm.reporting.models.project import Project, ProjectAdminView, ProjectInlineAdminView
from koalixcrm.reporting.models.project_link_type import ProjectLinkType, OptionProjectLinkType
from koalixcrm.reporting.models.project_status import ProjectStatus, OptionProjectStatus
from koalixcrm.reporting.models.reporting_period import ReportingPeriod, ReportingPeriodAdmin, ReportingPeriodInlineAdminView
from koalixcrm.reporting.models.reporting_period_status import ReportingPeriodStatus, OptionReportingPeriodStatus
from koalixcrm.reporting.models.resource import Resource
from koalixcrm.reporting.models.resource_manager import ResourceManager, ResourceManagerAdminView
from koalixcrm.reporting.models.resource_price import ResourcePrice, ResourcePriceInlineAdminView
from koalixcrm.reporting.models.resource_type import ResourceType, ResourceTypeAdminView
from koalixcrm.reporting.models.task import Task, TaskAdminView, TaskInlineAdminView
from koalixcrm.reporting.models.task_link_type import TaskLinkType, OptionTaskLinkType
from koalixcrm.reporting.models.task_status import TaskStatus, OptionTaskStatus
from koalixcrm.reporting.models.work import Work, WorkAdminView, WorkInlineAdminView
