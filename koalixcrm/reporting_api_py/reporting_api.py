# -*- coding: utf-8 -*-
"""
Reporting API entry point.

Exposes Reporting REST viewsets for URL routing.
"""
from koalixcrm.reporting.views.agreement_status_view_set import AgreementStatusViewSet
from koalixcrm.reporting.views.agreement_type_view_set import AgreementTypeViewSet
from koalixcrm.reporting.views.agreement_view_set import AgreementViewSet
from koalixcrm.reporting.views.estimation_status_view_set import EstimationStatusViewSet
from koalixcrm.reporting.views.estimation_view_set import EstimationViewSet
from koalixcrm.reporting.views.generic_project_link_view_set import (
    GenericProjectLinkViewSet,
)
from koalixcrm.reporting.views.generic_task_link_view_set import GenericTaskLinkViewSet
from koalixcrm.reporting.views.human_resource_view_set import HumanResourceViewSet
from koalixcrm.reporting.views.project_link_type_view_set import ProjectLinkTypeViewSet
from koalixcrm.reporting.views.project_status_view_set import ProjectStatusViewSet
from koalixcrm.reporting.views.project_view_set import ProjectViewSet
from koalixcrm.reporting.views.reporting_period_status_view_set import (
    ReportingPeriodStatusViewSet,
)
from koalixcrm.reporting.views.reporting_period_view_set import ReportingPeriodViewSet
from koalixcrm.reporting.views.resource_manager_view_set import ResourceManagerViewSet
from koalixcrm.reporting.views.resource_price_view_set import ResourcePriceViewSet
from koalixcrm.reporting.views.resource_type_view_set import ResourceTypeViewSet
from koalixcrm.reporting.views.resource_view_set import ResourceViewSet
from koalixcrm.reporting.views.task_link_type_view_set import TaskLinkTypeViewSet
from koalixcrm.reporting.views.task_status_view_set import TaskStatusViewSet
from koalixcrm.reporting.views.task_view_set import TaskViewSet
from koalixcrm.reporting.views.work_view_set import WorkViewSet

__all__ = [
    'TaskViewSet',
    'TaskStatusViewSet',
    'ProjectViewSet',
    'ProjectStatusViewSet',
    'AgreementViewSet',
    'WorkViewSet',
    'EstimationViewSet',
    'EstimationStatusViewSet',
    'HumanResourceViewSet',
    'ResourceViewSet',
    'ResourceTypeViewSet',
    'ResourceManagerViewSet',
    'ResourcePriceViewSet',
    'ReportingPeriodViewSet',
    'ReportingPeriodStatusViewSet',
    'AgreementStatusViewSet',
    'AgreementTypeViewSet',
    'ProjectLinkTypeViewSet',
    'TaskLinkTypeViewSet',
    'GenericProjectLinkViewSet',
    'GenericTaskLinkViewSet',
]
