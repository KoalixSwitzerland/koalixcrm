# -*- coding: utf-8 -*-
"""KoalixCRM Reporting API Client."""
from __future__ import annotations

from typing import Any

from koalixcrm.reporting_api_py.dto.agreement import Agreement
from koalixcrm.reporting_api_py.dto.agreement_status import AgreementStatus
from koalixcrm.reporting_api_py.dto.agreement_type import AgreementType
from koalixcrm.reporting_api_py.dto.estimation import Estimation
from koalixcrm.reporting_api_py.dto.estimation_status import EstimationStatus
from koalixcrm.reporting_api_py.dto.generic_project_link import GenericProjectLink
from koalixcrm.reporting_api_py.dto.generic_task_link import GenericTaskLink
from koalixcrm.reporting_api_py.dto.human_resource import HumanResource
from koalixcrm.reporting_api_py.dto.project import Project
from koalixcrm.reporting_api_py.dto.project_link_type import ProjectLinkType
from koalixcrm.reporting_api_py.dto.project_status import ProjectStatus
from koalixcrm.reporting_api_py.dto.reporting_period import ReportingPeriod
from koalixcrm.reporting_api_py.dto.reporting_period_status import ReportingPeriodStatus
from koalixcrm.reporting_api_py.dto.resource import Resource
from koalixcrm.reporting_api_py.dto.resource_manager import ResourceManager
from koalixcrm.reporting_api_py.dto.resource_price import ResourcePrice
from koalixcrm.reporting_api_py.dto.resource_type import ResourceType
from koalixcrm.reporting_api_py.dto.task import Task
from koalixcrm.reporting_api_py.dto.task_link_type import TaskLinkType
from koalixcrm.reporting_api_py.dto.task_status import TaskStatus
from koalixcrm.reporting_api_py.dto.work import Work
from koalixcrm.shared.api_client import BaseAPIClient


class KoalixCRMReportingAPIClient(BaseAPIClient):
    """API client for the koalixcrm Reporting application."""

    api_path_env_var = 'KOALIXCRM_REPORTING_API_PATH'
    api_path_default = '/koalixcrm_reporting/api/v1/'
    uses_workspace_id = True

    # --- Project ---

    def get_project(self, object_id: int) -> Project | None:
        return self._get_object(Project, "/projects", object_id)

    def get_project_list(self) -> list[Project]:
        return self._get_object_list(Project, "/projects/")

    def create_project(self, data: dict[str, Any]) -> Project | None:
        response_data = self._make_request("/projects/", method="POST", data=data)
        if response_data:
            obj = Project(response_data, self)
            self._cache.set(Project, obj.id, obj)
            return obj
        return None

    def update_project(self, object_id: int, data: dict[str, Any]) -> Project | None:
        return self._put_full_update(Project, "/projects", object_id, data)

    # --- ProjectStatus ---

    def get_project_status(self, object_id: int) -> ProjectStatus | None:
        return self._get_object(ProjectStatus, "/project-status", object_id)

    def get_project_status_list(self) -> list[ProjectStatus]:
        return self._get_object_list(ProjectStatus, "/project-status/")

    def create_project_status(self, data: dict[str, Any]) -> ProjectStatus | None:
        response_data = self._make_request("/project-status/", method="POST", data=data)
        if response_data:
            obj = ProjectStatus(response_data, self)
            self._cache.set(ProjectStatus, obj.id, obj)
            return obj
        return None

    def update_project_status(self, object_id: int, data: dict[str, Any]) -> ProjectStatus | None:
        return self._put_full_update(ProjectStatus, "/project-status", object_id, data)

    # --- Task ---

    def get_task(self, object_id: int) -> Task | None:
        return self._get_object(Task, "/tasks", object_id)

    def get_task_list(self) -> list[Task]:
        return self._get_object_list(Task, "/tasks/")

    def create_task(self, data: dict[str, Any]) -> Task | None:
        response_data = self._make_request("/tasks/", method="POST", data=data)
        if response_data:
            obj = Task(response_data, self)
            self._cache.set(Task, obj.id, obj)
            return obj
        return None

    def update_task(self, object_id: int, data: dict[str, Any]) -> Task | None:
        return self._put_full_update(Task, "/tasks", object_id, data)

    # --- TaskStatus ---

    def get_task_status(self, object_id: int) -> TaskStatus | None:
        return self._get_object(TaskStatus, "/task-status", object_id)

    def get_task_status_list(self) -> list[TaskStatus]:
        return self._get_object_list(TaskStatus, "/task-status/")

    def create_task_status(self, data: dict[str, Any]) -> TaskStatus | None:
        response_data = self._make_request("/task-status/", method="POST", data=data)
        if response_data:
            obj = TaskStatus(response_data, self)
            self._cache.set(TaskStatus, obj.id, obj)
            return obj
        return None

    def update_task_status(self, object_id: int, data: dict[str, Any]) -> TaskStatus | None:
        return self._put_full_update(TaskStatus, "/task-status", object_id, data)

    # --- Work ---

    def get_work(self, object_id: int) -> Work | None:
        return self._get_object(Work, "/works", object_id)

    def get_work_list(self) -> list[Work]:
        return self._get_object_list(Work, "/works/")

    def create_work(self, data: dict[str, Any]) -> Work | None:
        response_data = self._make_request("/works/", method="POST", data=data)
        if response_data:
            obj = Work(response_data, self)
            self._cache.set(Work, obj.id, obj)
            return obj
        return None

    def update_work(self, object_id: int, data: dict[str, Any]) -> Work | None:
        return self._put_full_update(Work, "/works", object_id, data)

    # --- Agreement ---

    def get_agreement(self, object_id: int) -> Agreement | None:
        return self._get_object(Agreement, "/agreements", object_id)

    def get_agreement_list(self) -> list[Agreement]:
        return self._get_object_list(Agreement, "/agreements/")

    def create_agreement(self, data: dict[str, Any]) -> Agreement | None:
        response_data = self._make_request("/agreements/", method="POST", data=data)
        if response_data:
            obj = Agreement(response_data, self)
            self._cache.set(Agreement, obj.id, obj)
            return obj
        return None

    def update_agreement(self, object_id: int, data: dict[str, Any]) -> Agreement | None:
        return self._put_full_update(Agreement, "/agreements", object_id, data)

    # --- AgreementStatus ---

    def get_agreement_status(self, object_id: int) -> AgreementStatus | None:
        return self._get_object(AgreementStatus, "/agreement-status", object_id)

    def get_agreement_status_list(self) -> list[AgreementStatus]:
        return self._get_object_list(AgreementStatus, "/agreement-status/")

    def create_agreement_status(self, data: dict[str, Any]) -> AgreementStatus | None:
        response_data = self._make_request("/agreement-status/", method="POST", data=data)
        if response_data:
            obj = AgreementStatus(response_data, self)
            self._cache.set(AgreementStatus, obj.id, obj)
            return obj
        return None

    def update_agreement_status(self, object_id: int, data: dict[str, Any]) -> AgreementStatus | None:
        return self._put_full_update(AgreementStatus, "/agreement-status", object_id, data)

    # --- AgreementType ---

    def get_agreement_type(self, object_id: int) -> AgreementType | None:
        return self._get_object(AgreementType, "/agreement-types", object_id)

    def get_agreement_type_list(self) -> list[AgreementType]:
        return self._get_object_list(AgreementType, "/agreement-types/")

    def create_agreement_type(self, data: dict[str, Any]) -> AgreementType | None:
        response_data = self._make_request("/agreement-types/", method="POST", data=data)
        if response_data:
            obj = AgreementType(response_data, self)
            self._cache.set(AgreementType, obj.id, obj)
            return obj
        return None

    def update_agreement_type(self, object_id: int, data: dict[str, Any]) -> AgreementType | None:
        return self._put_full_update(AgreementType, "/agreement-types", object_id, data)

    # --- Estimation ---

    def get_estimation(self, object_id: int) -> Estimation | None:
        return self._get_object(Estimation, "/estimations", object_id)

    def get_estimation_list(self) -> list[Estimation]:
        return self._get_object_list(Estimation, "/estimations/")

    def create_estimation(self, data: dict[str, Any]) -> Estimation | None:
        response_data = self._make_request("/estimations/", method="POST", data=data)
        if response_data:
            obj = Estimation(response_data, self)
            self._cache.set(Estimation, obj.id, obj)
            return obj
        return None

    def update_estimation(self, object_id: int, data: dict[str, Any]) -> Estimation | None:
        return self._put_full_update(Estimation, "/estimations", object_id, data)

    # --- EstimationStatus ---

    def get_estimation_status(self, object_id: int) -> EstimationStatus | None:
        return self._get_object(EstimationStatus, "/estimation-status", object_id)

    def get_estimation_status_list(self) -> list[EstimationStatus]:
        return self._get_object_list(EstimationStatus, "/estimation-status/")

    def create_estimation_status(self, data: dict[str, Any]) -> EstimationStatus | None:
        response_data = self._make_request("/estimation-status/", method="POST", data=data)
        if response_data:
            obj = EstimationStatus(response_data, self)
            self._cache.set(EstimationStatus, obj.id, obj)
            return obj
        return None

    def update_estimation_status(self, object_id: int, data: dict[str, Any]) -> EstimationStatus | None:
        return self._put_full_update(EstimationStatus, "/estimation-status", object_id, data)

    # --- HumanResource ---

    def get_human_resource(self, object_id: int) -> HumanResource | None:
        return self._get_object(HumanResource, "/human-resources", object_id)

    def get_human_resource_list(self) -> list[HumanResource]:
        return self._get_object_list(HumanResource, "/human-resources/")

    def create_human_resource(self, data: dict[str, Any]) -> HumanResource | None:
        response_data = self._make_request("/human-resources/", method="POST", data=data)
        if response_data:
            obj = HumanResource(response_data, self)
            self._cache.set(HumanResource, obj.id, obj)
            return obj
        return None

    def update_human_resource(self, object_id: int, data: dict[str, Any]) -> HumanResource | None:
        return self._put_full_update(HumanResource, "/human-resources", object_id, data)

    # --- Resource ---

    def get_resource(self, object_id: int) -> Resource | None:
        return self._get_object(Resource, "/resources", object_id)

    def get_resource_list(self) -> list[Resource]:
        return self._get_object_list(Resource, "/resources/")

    def create_resource(self, data: dict[str, Any]) -> Resource | None:
        response_data = self._make_request("/resources/", method="POST", data=data)
        if response_data:
            obj = Resource(response_data, self)
            self._cache.set(Resource, obj.id, obj)
            return obj
        return None

    def update_resource(self, object_id: int, data: dict[str, Any]) -> Resource | None:
        return self._put_full_update(Resource, "/resources", object_id, data)

    # --- ResourceType ---

    def get_resource_type(self, object_id: int) -> ResourceType | None:
        return self._get_object(ResourceType, "/resource-types", object_id)

    def get_resource_type_list(self) -> list[ResourceType]:
        return self._get_object_list(ResourceType, "/resource-types/")

    def create_resource_type(self, data: dict[str, Any]) -> ResourceType | None:
        response_data = self._make_request("/resource-types/", method="POST", data=data)
        if response_data:
            obj = ResourceType(response_data, self)
            self._cache.set(ResourceType, obj.id, obj)
            return obj
        return None

    def update_resource_type(self, object_id: int, data: dict[str, Any]) -> ResourceType | None:
        return self._put_full_update(ResourceType, "/resource-types", object_id, data)

    # --- ResourceManager ---

    def get_resource_manager(self, object_id: int) -> ResourceManager | None:
        return self._get_object(ResourceManager, "/resource-managers", object_id)

    def get_resource_manager_list(self) -> list[ResourceManager]:
        return self._get_object_list(ResourceManager, "/resource-managers/")

    def create_resource_manager(self, data: dict[str, Any]) -> ResourceManager | None:
        response_data = self._make_request("/resource-managers/", method="POST", data=data)
        if response_data:
            obj = ResourceManager(response_data, self)
            self._cache.set(ResourceManager, obj.id, obj)
            return obj
        return None

    def update_resource_manager(self, object_id: int, data: dict[str, Any]) -> ResourceManager | None:
        return self._put_full_update(ResourceManager, "/resource-managers", object_id, data)

    # --- ResourcePrice ---

    def get_resource_price(self, object_id: int) -> ResourcePrice | None:
        return self._get_object(ResourcePrice, "/resource-prices", object_id)

    def get_resource_price_list(self) -> list[ResourcePrice]:
        return self._get_object_list(ResourcePrice, "/resource-prices/")

    def create_resource_price(self, data: dict[str, Any]) -> ResourcePrice | None:
        response_data = self._make_request("/resource-prices/", method="POST", data=data)
        if response_data:
            obj = ResourcePrice(response_data, self)
            self._cache.set(ResourcePrice, obj.id, obj)
            return obj
        return None

    def update_resource_price(self, object_id: int, data: dict[str, Any]) -> ResourcePrice | None:
        return self._put_full_update(ResourcePrice, "/resource-prices", object_id, data)

    # --- ReportingPeriod ---

    def get_reporting_period(self, object_id: int) -> ReportingPeriod | None:
        return self._get_object(ReportingPeriod, "/reporting-periods", object_id)

    def get_reporting_period_list(self) -> list[ReportingPeriod]:
        return self._get_object_list(ReportingPeriod, "/reporting-periods/")

    def create_reporting_period(self, data: dict[str, Any]) -> ReportingPeriod | None:
        response_data = self._make_request("/reporting-periods/", method="POST", data=data)
        if response_data:
            obj = ReportingPeriod(response_data, self)
            self._cache.set(ReportingPeriod, obj.id, obj)
            return obj
        return None

    def update_reporting_period(self, object_id: int, data: dict[str, Any]) -> ReportingPeriod | None:
        return self._put_full_update(ReportingPeriod, "/reporting-periods", object_id, data)

    # --- ReportingPeriodStatus ---

    def get_reporting_period_status(self, object_id: int) -> ReportingPeriodStatus | None:
        return self._get_object(ReportingPeriodStatus, "/reporting-period-status", object_id)

    def get_reporting_period_status_list(self) -> list[ReportingPeriodStatus]:
        return self._get_object_list(ReportingPeriodStatus, "/reporting-period-status/")

    def create_reporting_period_status(self, data: dict[str, Any]) -> ReportingPeriodStatus | None:
        response_data = self._make_request("/reporting-period-status/", method="POST", data=data)
        if response_data:
            obj = ReportingPeriodStatus(response_data, self)
            self._cache.set(ReportingPeriodStatus, obj.id, obj)
            return obj
        return None

    def update_reporting_period_status(self, object_id: int, data: dict[str, Any]) -> ReportingPeriodStatus | None:
        return self._put_full_update(ReportingPeriodStatus, "/reporting-period-status", object_id, data)

    # --- ProjectLinkType ---

    def get_project_link_type(self, object_id: int) -> ProjectLinkType | None:
        return self._get_object(ProjectLinkType, "/project-link-types", object_id)

    def get_project_link_type_list(self) -> list[ProjectLinkType]:
        return self._get_object_list(ProjectLinkType, "/project-link-types/")

    def create_project_link_type(self, data: dict[str, Any]) -> ProjectLinkType | None:
        response_data = self._make_request("/project-link-types/", method="POST", data=data)
        if response_data:
            obj = ProjectLinkType(response_data, self)
            self._cache.set(ProjectLinkType, obj.id, obj)
            return obj
        return None

    def update_project_link_type(self, object_id: int, data: dict[str, Any]) -> ProjectLinkType | None:
        return self._put_full_update(ProjectLinkType, "/project-link-types", object_id, data)

    # --- TaskLinkType ---

    def get_task_link_type(self, object_id: int) -> TaskLinkType | None:
        return self._get_object(TaskLinkType, "/task-link-types", object_id)

    def get_task_link_type_list(self) -> list[TaskLinkType]:
        return self._get_object_list(TaskLinkType, "/task-link-types/")

    def create_task_link_type(self, data: dict[str, Any]) -> TaskLinkType | None:
        response_data = self._make_request("/task-link-types/", method="POST", data=data)
        if response_data:
            obj = TaskLinkType(response_data, self)
            self._cache.set(TaskLinkType, obj.id, obj)
            return obj
        return None

    def update_task_link_type(self, object_id: int, data: dict[str, Any]) -> TaskLinkType | None:
        return self._put_full_update(TaskLinkType, "/task-link-types", object_id, data)

    # --- GenericProjectLink ---

    def get_generic_project_link(self, object_id: int) -> GenericProjectLink | None:
        return self._get_object(GenericProjectLink, "/generic-project-links", object_id)

    def get_generic_project_link_list(self) -> list[GenericProjectLink]:
        return self._get_object_list(GenericProjectLink, "/generic-project-links/")

    def create_generic_project_link(self, data: dict[str, Any]) -> GenericProjectLink | None:
        response_data = self._make_request("/generic-project-links/", method="POST", data=data)
        if response_data:
            obj = GenericProjectLink(response_data, self)
            self._cache.set(GenericProjectLink, obj.id, obj)
            return obj
        return None

    def update_generic_project_link(self, object_id: int, data: dict[str, Any]) -> GenericProjectLink | None:
        return self._put_full_update(GenericProjectLink, "/generic-project-links", object_id, data)

    # --- GenericTaskLink ---

    def get_generic_task_link(self, object_id: int) -> GenericTaskLink | None:
        return self._get_object(GenericTaskLink, "/generic-task-links", object_id)

    def get_generic_task_link_list(self) -> list[GenericTaskLink]:
        return self._get_object_list(GenericTaskLink, "/generic-task-links/")

    def create_generic_task_link(self, data: dict[str, Any]) -> GenericTaskLink | None:
        response_data = self._make_request("/generic-task-links/", method="POST", data=data)
        if response_data:
            obj = GenericTaskLink(response_data, self)
            self._cache.set(GenericTaskLink, obj.id, obj)
            return obj
        return None

    def update_generic_task_link(self, object_id: int, data: dict[str, Any]) -> GenericTaskLink | None:
        return self._put_full_update(GenericTaskLink, "/generic-task-links", object_id, data)
