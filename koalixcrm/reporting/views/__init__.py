# -*- coding: utf-8 -*-
from __future__ import annotations

from .agreement_status_view_set import AgreementStatusViewSet
from .agreement_type_view_set import AgreementTypeViewSet
from .agreement_view_set import AgreementViewSet
from .estimation_status_view_set import EstimationStatusViewSet
from .estimation_view_set import EstimationViewSet
from .generic_project_link_view_set import GenericProjectLinkViewSet
from .generic_task_link_view_set import GenericTaskLinkViewSet
from .human_resource_view_set import HumanResourceViewSet
from .project_link_type_view_set import ProjectLinkTypeViewSet
from .project_status_view_set import ProjectStatusViewSet
from .project_view_set import ProjectViewSet
from .reporting_period_status_view_set import ReportingPeriodStatusViewSet
from .reporting_period_view_set import ReportingPeriodViewSet
from .resource_manager_view_set import ResourceManagerViewSet
from .resource_price_view_set import ResourcePriceViewSet
from .resource_type_view_set import ResourceTypeViewSet
from .resource_view_set import ResourceViewSet
from .task_link_type_view_set import TaskLinkTypeViewSet
from .task_status_view_set import TaskStatusViewSet
from .task_view_set import TaskViewSet
from .work_view_set import WorkViewSet

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
