# -*- coding: utf-8 -*-
"""
Reporting API entry point.

Exposes Reporting REST viewsets for URL routing.
"""
from koalixcrm.reporting.views.task_view_set import TaskViewSet
from koalixcrm.reporting.views.task_status_view_set import TaskStatusViewSet
from koalixcrm.reporting.views.project_view_set import ProjectViewSet
from koalixcrm.reporting.views.project_status_view_set import ProjectStatusViewSet
from koalixcrm.reporting.views.agreement_view_set import AgreementViewSet

__all__ = [
    'TaskViewSet',
    'TaskStatusViewSet',
    'ProjectViewSet',
    'ProjectStatusViewSet',
    'AgreementViewSet',
]
