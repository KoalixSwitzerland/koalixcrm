"""Per-app REST API routes for koalixcrm Reporting.

Mounted at ``/koalixcrm_reporting/api/v1/<workspace_id>/`` from
``projectsettings/urls.py`` once CR-R2 of CR-002 lands. Until then this
module is inert — importing it has no effect on the running URL conf.

Note: this module is **not** named ``urls.py`` because ``koalixcrm/reporting/urls.py``
already serves the legacy server-rendered reporting views (mounted at
``/koalixcrm/crm/reporting/``). See CR-002 §3.5.
"""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from koalixcrm.reporting_api_py.reporting_api import (
    AgreementStatusViewSet,
    AgreementTypeViewSet,
    AgreementViewSet,
    EstimationStatusViewSet,
    EstimationViewSet,
    GenericProjectLinkViewSet,
    GenericTaskLinkViewSet,
    HumanResourceViewSet,
    ProjectLinkTypeViewSet,
    ProjectStatusViewSet,
    ProjectViewSet,
    ReportingPeriodStatusViewSet,
    ReportingPeriodViewSet,
    ResourceManagerViewSet,
    ResourcePriceViewSet,
    ResourceTypeViewSet,
    ResourceViewSet,
    TaskLinkTypeViewSet,
    TaskStatusViewSet,
    TaskViewSet,
    WorkViewSet,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-status', ProjectStatusViewSet, basename='project-status')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-status', TaskStatusViewSet, basename='task-status')
router.register(r'agreements', AgreementViewSet, basename='agreement')
router.register(r'works', WorkViewSet, basename='work')
router.register(r'estimations', EstimationViewSet, basename='estimation')
router.register(r'estimation-status', EstimationStatusViewSet, basename='estimation-status')
router.register(r'human-resources', HumanResourceViewSet, basename='human-resource')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'resource-types', ResourceTypeViewSet, basename='resource-type')
router.register(r'resource-managers', ResourceManagerViewSet, basename='resource-manager')
router.register(r'resource-prices', ResourcePriceViewSet, basename='resource-price')
router.register(r'reporting-periods', ReportingPeriodViewSet, basename='reporting-period')
router.register(r'reporting-period-status', ReportingPeriodStatusViewSet, basename='reporting-period-status')
router.register(r'agreement-status', AgreementStatusViewSet, basename='agreement-status')
router.register(r'agreement-types', AgreementTypeViewSet, basename='agreement-type')
router.register(r'project-link-types', ProjectLinkTypeViewSet, basename='project-link-type')
router.register(r'task-link-types', TaskLinkTypeViewSet, basename='task-link-type')
router.register(r'generic-project-links', GenericProjectLinkViewSet, basename='generic-project-link')
router.register(r'generic-task-links', GenericTaskLinkViewSet, basename='generic-task-link')

urlpatterns = router.urls
