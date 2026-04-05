# -*- coding: utf-8 -*-
"""KoalixCRM Reporting API Client."""
from typing import Any, Dict, List, Optional

from koalixcrm.shared.api_client import BaseAPIClient
from koalixcrm.reporting_api_py.dto.project import Project
from koalixcrm.reporting_api_py.dto.project_status import ProjectStatus
from koalixcrm.reporting_api_py.dto.task import Task
from koalixcrm.reporting_api_py.dto.task_status import TaskStatus
from koalixcrm.reporting_api_py.dto.work import Work
from koalixcrm.reporting_api_py.dto.agreement import Agreement
from koalixcrm.reporting_api_py.dto.agreement_status import AgreementStatus
from koalixcrm.reporting_api_py.dto.agreement_type import AgreementType
from koalixcrm.reporting_api_py.dto.estimation import Estimation
from koalixcrm.reporting_api_py.dto.estimation_status import EstimationStatus
from koalixcrm.reporting_api_py.dto.human_resource import HumanResource
from koalixcrm.reporting_api_py.dto.resource import Resource
from koalixcrm.reporting_api_py.dto.resource_type import ResourceType
from koalixcrm.reporting_api_py.dto.resource_manager import ResourceManager
from koalixcrm.reporting_api_py.dto.resource_price import ResourcePrice
from koalixcrm.reporting_api_py.dto.reporting_period import ReportingPeriod
from koalixcrm.reporting_api_py.dto.reporting_period_status import ReportingPeriodStatus
from koalixcrm.reporting_api_py.dto.project_link_type import ProjectLinkType
from koalixcrm.reporting_api_py.dto.task_link_type import TaskLinkType
from koalixcrm.reporting_api_py.dto.generic_project_link import GenericProjectLink
from koalixcrm.reporting_api_py.dto.generic_task_link import GenericTaskLink


class KoalixCRMReportingAPIClient(BaseAPIClient):
    """API client for the koalixcrm Reporting application."""

    api_path_env_var = 'KOALIXCRM_REPORTING_API_PATH'
    api_path_default = ''

    # --- Project ---

    def get_project(self, object_id: int) -> Optional[Project]:
        return self._get_object(Project, "/projects", object_id)

    def get_project_list(self) -> List[Project]:
        return self._get_object_list(Project, "/projects/")

    def create_project(self, data: Dict[str, Any]) -> Optional[Project]:
        response_data = self._make_request("/projects/", method="POST", data=data)
        if response_data:
            obj = Project(response_data, self)
            self._cache.set(Project, obj.id, obj)
            return obj
        return None

    def update_project(self, object_id: int, data: Dict[str, Any]) -> Optional[Project]:
        return self._put_full_update(Project, "/projects", object_id, data)

    # --- ProjectStatus ---

    def get_project_status(self, object_id: int) -> Optional[ProjectStatus]:
        return self._get_object(ProjectStatus, "/projectStatus", object_id)

    def get_project_status_list(self) -> List[ProjectStatus]:
        return self._get_object_list(ProjectStatus, "/projectStatus/")

    def create_project_status(self, data: Dict[str, Any]) -> Optional[ProjectStatus]:
        response_data = self._make_request("/projectStatus/", method="POST", data=data)
        if response_data:
            obj = ProjectStatus(response_data, self)
            self._cache.set(ProjectStatus, obj.id, obj)
            return obj
        return None

    def update_project_status(self, object_id: int, data: Dict[str, Any]) -> Optional[ProjectStatus]:
        return self._put_full_update(ProjectStatus, "/projectStatus", object_id, data)

    # --- Task ---

    def get_task(self, object_id: int) -> Optional[Task]:
        return self._get_object(Task, "/tasks", object_id)

    def get_task_list(self) -> List[Task]:
        return self._get_object_list(Task, "/tasks/")

    def create_task(self, data: Dict[str, Any]) -> Optional[Task]:
        response_data = self._make_request("/tasks/", method="POST", data=data)
        if response_data:
            obj = Task(response_data, self)
            self._cache.set(Task, obj.id, obj)
            return obj
        return None

    def update_task(self, object_id: int, data: Dict[str, Any]) -> Optional[Task]:
        return self._put_full_update(Task, "/tasks", object_id, data)

    # --- TaskStatus ---

    def get_task_status(self, object_id: int) -> Optional[TaskStatus]:
        return self._get_object(TaskStatus, "/taskstatus", object_id)

    def get_task_status_list(self) -> List[TaskStatus]:
        return self._get_object_list(TaskStatus, "/taskstatus/")

    def create_task_status(self, data: Dict[str, Any]) -> Optional[TaskStatus]:
        response_data = self._make_request("/taskstatus/", method="POST", data=data)
        if response_data:
            obj = TaskStatus(response_data, self)
            self._cache.set(TaskStatus, obj.id, obj)
            return obj
        return None

    def update_task_status(self, object_id: int, data: Dict[str, Any]) -> Optional[TaskStatus]:
        return self._put_full_update(TaskStatus, "/taskstatus", object_id, data)

    # --- Work ---

    def get_work(self, object_id: int) -> Optional[Work]:
        return self._get_object(Work, "/works", object_id)

    def get_work_list(self) -> List[Work]:
        return self._get_object_list(Work, "/works/")

    def create_work(self, data: Dict[str, Any]) -> Optional[Work]:
        response_data = self._make_request("/works/", method="POST", data=data)
        if response_data:
            obj = Work(response_data, self)
            self._cache.set(Work, obj.id, obj)
            return obj
        return None

    def update_work(self, object_id: int, data: Dict[str, Any]) -> Optional[Work]:
        return self._put_full_update(Work, "/works", object_id, data)

    # --- Agreement ---

    def get_agreement(self, object_id: int) -> Optional[Agreement]:
        return self._get_object(Agreement, "/agreements", object_id)

    def get_agreement_list(self) -> List[Agreement]:
        return self._get_object_list(Agreement, "/agreements/")

    def create_agreement(self, data: Dict[str, Any]) -> Optional[Agreement]:
        response_data = self._make_request("/agreements/", method="POST", data=data)
        if response_data:
            obj = Agreement(response_data, self)
            self._cache.set(Agreement, obj.id, obj)
            return obj
        return None

    def update_agreement(self, object_id: int, data: Dict[str, Any]) -> Optional[Agreement]:
        return self._put_full_update(Agreement, "/agreements", object_id, data)

    # --- AgreementStatus ---

    def get_agreement_status(self, object_id: int) -> Optional[AgreementStatus]:
        return self._get_object(AgreementStatus, "/agreementStatus", object_id)

    def get_agreement_status_list(self) -> List[AgreementStatus]:
        return self._get_object_list(AgreementStatus, "/agreementStatus/")

    def create_agreement_status(self, data: Dict[str, Any]) -> Optional[AgreementStatus]:
        response_data = self._make_request("/agreementStatus/", method="POST", data=data)
        if response_data:
            obj = AgreementStatus(response_data, self)
            self._cache.set(AgreementStatus, obj.id, obj)
            return obj
        return None

    def update_agreement_status(self, object_id: int, data: Dict[str, Any]) -> Optional[AgreementStatus]:
        return self._put_full_update(AgreementStatus, "/agreementStatus", object_id, data)

    # --- AgreementType ---

    def get_agreement_type(self, object_id: int) -> Optional[AgreementType]:
        return self._get_object(AgreementType, "/agreementTypes", object_id)

    def get_agreement_type_list(self) -> List[AgreementType]:
        return self._get_object_list(AgreementType, "/agreementTypes/")

    def create_agreement_type(self, data: Dict[str, Any]) -> Optional[AgreementType]:
        response_data = self._make_request("/agreementTypes/", method="POST", data=data)
        if response_data:
            obj = AgreementType(response_data, self)
            self._cache.set(AgreementType, obj.id, obj)
            return obj
        return None

    def update_agreement_type(self, object_id: int, data: Dict[str, Any]) -> Optional[AgreementType]:
        return self._put_full_update(AgreementType, "/agreementTypes", object_id, data)

    # --- Estimation ---

    def get_estimation(self, object_id: int) -> Optional[Estimation]:
        return self._get_object(Estimation, "/estimations", object_id)

    def get_estimation_list(self) -> List[Estimation]:
        return self._get_object_list(Estimation, "/estimations/")

    def create_estimation(self, data: Dict[str, Any]) -> Optional[Estimation]:
        response_data = self._make_request("/estimations/", method="POST", data=data)
        if response_data:
            obj = Estimation(response_data, self)
            self._cache.set(Estimation, obj.id, obj)
            return obj
        return None

    def update_estimation(self, object_id: int, data: Dict[str, Any]) -> Optional[Estimation]:
        return self._put_full_update(Estimation, "/estimations", object_id, data)

    # --- EstimationStatus ---

    def get_estimation_status(self, object_id: int) -> Optional[EstimationStatus]:
        return self._get_object(EstimationStatus, "/estimationStatus", object_id)

    def get_estimation_status_list(self) -> List[EstimationStatus]:
        return self._get_object_list(EstimationStatus, "/estimationStatus/")

    def create_estimation_status(self, data: Dict[str, Any]) -> Optional[EstimationStatus]:
        response_data = self._make_request("/estimationStatus/", method="POST", data=data)
        if response_data:
            obj = EstimationStatus(response_data, self)
            self._cache.set(EstimationStatus, obj.id, obj)
            return obj
        return None

    def update_estimation_status(self, object_id: int, data: Dict[str, Any]) -> Optional[EstimationStatus]:
        return self._put_full_update(EstimationStatus, "/estimationStatus", object_id, data)

    # --- HumanResource ---

    def get_human_resource(self, object_id: int) -> Optional[HumanResource]:
        return self._get_object(HumanResource, "/humanResources", object_id)

    def get_human_resource_list(self) -> List[HumanResource]:
        return self._get_object_list(HumanResource, "/humanResources/")

    def create_human_resource(self, data: Dict[str, Any]) -> Optional[HumanResource]:
        response_data = self._make_request("/humanResources/", method="POST", data=data)
        if response_data:
            obj = HumanResource(response_data, self)
            self._cache.set(HumanResource, obj.id, obj)
            return obj
        return None

    def update_human_resource(self, object_id: int, data: Dict[str, Any]) -> Optional[HumanResource]:
        return self._put_full_update(HumanResource, "/humanResources", object_id, data)

    # --- Resource ---

    def get_resource(self, object_id: int) -> Optional[Resource]:
        return self._get_object(Resource, "/resources", object_id)

    def get_resource_list(self) -> List[Resource]:
        return self._get_object_list(Resource, "/resources/")

    def create_resource(self, data: Dict[str, Any]) -> Optional[Resource]:
        response_data = self._make_request("/resources/", method="POST", data=data)
        if response_data:
            obj = Resource(response_data, self)
            self._cache.set(Resource, obj.id, obj)
            return obj
        return None

    def update_resource(self, object_id: int, data: Dict[str, Any]) -> Optional[Resource]:
        return self._put_full_update(Resource, "/resources", object_id, data)

    # --- ResourceType ---

    def get_resource_type(self, object_id: int) -> Optional[ResourceType]:
        return self._get_object(ResourceType, "/resourceTypes", object_id)

    def get_resource_type_list(self) -> List[ResourceType]:
        return self._get_object_list(ResourceType, "/resourceTypes/")

    def create_resource_type(self, data: Dict[str, Any]) -> Optional[ResourceType]:
        response_data = self._make_request("/resourceTypes/", method="POST", data=data)
        if response_data:
            obj = ResourceType(response_data, self)
            self._cache.set(ResourceType, obj.id, obj)
            return obj
        return None

    def update_resource_type(self, object_id: int, data: Dict[str, Any]) -> Optional[ResourceType]:
        return self._put_full_update(ResourceType, "/resourceTypes", object_id, data)

    # --- ResourceManager ---

    def get_resource_manager(self, object_id: int) -> Optional[ResourceManager]:
        return self._get_object(ResourceManager, "/resourceManagers", object_id)

    def get_resource_manager_list(self) -> List[ResourceManager]:
        return self._get_object_list(ResourceManager, "/resourceManagers/")

    def create_resource_manager(self, data: Dict[str, Any]) -> Optional[ResourceManager]:
        response_data = self._make_request("/resourceManagers/", method="POST", data=data)
        if response_data:
            obj = ResourceManager(response_data, self)
            self._cache.set(ResourceManager, obj.id, obj)
            return obj
        return None

    def update_resource_manager(self, object_id: int, data: Dict[str, Any]) -> Optional[ResourceManager]:
        return self._put_full_update(ResourceManager, "/resourceManagers", object_id, data)

    # --- ResourcePrice ---

    def get_resource_price(self, object_id: int) -> Optional[ResourcePrice]:
        return self._get_object(ResourcePrice, "/resourcePrices", object_id)

    def get_resource_price_list(self) -> List[ResourcePrice]:
        return self._get_object_list(ResourcePrice, "/resourcePrices/")

    def create_resource_price(self, data: Dict[str, Any]) -> Optional[ResourcePrice]:
        response_data = self._make_request("/resourcePrices/", method="POST", data=data)
        if response_data:
            obj = ResourcePrice(response_data, self)
            self._cache.set(ResourcePrice, obj.id, obj)
            return obj
        return None

    def update_resource_price(self, object_id: int, data: Dict[str, Any]) -> Optional[ResourcePrice]:
        return self._put_full_update(ResourcePrice, "/resourcePrices", object_id, data)

    # --- ReportingPeriod ---

    def get_reporting_period(self, object_id: int) -> Optional[ReportingPeriod]:
        return self._get_object(ReportingPeriod, "/reportingPeriods", object_id)

    def get_reporting_period_list(self) -> List[ReportingPeriod]:
        return self._get_object_list(ReportingPeriod, "/reportingPeriods/")

    def create_reporting_period(self, data: Dict[str, Any]) -> Optional[ReportingPeriod]:
        response_data = self._make_request("/reportingPeriods/", method="POST", data=data)
        if response_data:
            obj = ReportingPeriod(response_data, self)
            self._cache.set(ReportingPeriod, obj.id, obj)
            return obj
        return None

    def update_reporting_period(self, object_id: int, data: Dict[str, Any]) -> Optional[ReportingPeriod]:
        return self._put_full_update(ReportingPeriod, "/reportingPeriods", object_id, data)

    # --- ReportingPeriodStatus ---

    def get_reporting_period_status(self, object_id: int) -> Optional[ReportingPeriodStatus]:
        return self._get_object(ReportingPeriodStatus, "/reportingPeriodStatus", object_id)

    def get_reporting_period_status_list(self) -> List[ReportingPeriodStatus]:
        return self._get_object_list(ReportingPeriodStatus, "/reportingPeriodStatus/")

    def create_reporting_period_status(self, data: Dict[str, Any]) -> Optional[ReportingPeriodStatus]:
        response_data = self._make_request("/reportingPeriodStatus/", method="POST", data=data)
        if response_data:
            obj = ReportingPeriodStatus(response_data, self)
            self._cache.set(ReportingPeriodStatus, obj.id, obj)
            return obj
        return None

    def update_reporting_period_status(self, object_id: int, data: Dict[str, Any]) -> Optional[ReportingPeriodStatus]:
        return self._put_full_update(ReportingPeriodStatus, "/reportingPeriodStatus", object_id, data)

    # --- ProjectLinkType ---

    def get_project_link_type(self, object_id: int) -> Optional[ProjectLinkType]:
        return self._get_object(ProjectLinkType, "/projectLinkTypes", object_id)

    def get_project_link_type_list(self) -> List[ProjectLinkType]:
        return self._get_object_list(ProjectLinkType, "/projectLinkTypes/")

    def create_project_link_type(self, data: Dict[str, Any]) -> Optional[ProjectLinkType]:
        response_data = self._make_request("/projectLinkTypes/", method="POST", data=data)
        if response_data:
            obj = ProjectLinkType(response_data, self)
            self._cache.set(ProjectLinkType, obj.id, obj)
            return obj
        return None

    def update_project_link_type(self, object_id: int, data: Dict[str, Any]) -> Optional[ProjectLinkType]:
        return self._put_full_update(ProjectLinkType, "/projectLinkTypes", object_id, data)

    # --- TaskLinkType ---

    def get_task_link_type(self, object_id: int) -> Optional[TaskLinkType]:
        return self._get_object(TaskLinkType, "/taskLinkTypes", object_id)

    def get_task_link_type_list(self) -> List[TaskLinkType]:
        return self._get_object_list(TaskLinkType, "/taskLinkTypes/")

    def create_task_link_type(self, data: Dict[str, Any]) -> Optional[TaskLinkType]:
        response_data = self._make_request("/taskLinkTypes/", method="POST", data=data)
        if response_data:
            obj = TaskLinkType(response_data, self)
            self._cache.set(TaskLinkType, obj.id, obj)
            return obj
        return None

    def update_task_link_type(self, object_id: int, data: Dict[str, Any]) -> Optional[TaskLinkType]:
        return self._put_full_update(TaskLinkType, "/taskLinkTypes", object_id, data)

    # --- GenericProjectLink ---

    def get_generic_project_link(self, object_id: int) -> Optional[GenericProjectLink]:
        return self._get_object(GenericProjectLink, "/genericProjectLinks", object_id)

    def get_generic_project_link_list(self) -> List[GenericProjectLink]:
        return self._get_object_list(GenericProjectLink, "/genericProjectLinks/")

    def create_generic_project_link(self, data: Dict[str, Any]) -> Optional[GenericProjectLink]:
        response_data = self._make_request("/genericProjectLinks/", method="POST", data=data)
        if response_data:
            obj = GenericProjectLink(response_data, self)
            self._cache.set(GenericProjectLink, obj.id, obj)
            return obj
        return None

    def update_generic_project_link(self, object_id: int, data: Dict[str, Any]) -> Optional[GenericProjectLink]:
        return self._put_full_update(GenericProjectLink, "/genericProjectLinks", object_id, data)

    # --- GenericTaskLink ---

    def get_generic_task_link(self, object_id: int) -> Optional[GenericTaskLink]:
        return self._get_object(GenericTaskLink, "/genericTaskLinks", object_id)

    def get_generic_task_link_list(self) -> List[GenericTaskLink]:
        return self._get_object_list(GenericTaskLink, "/genericTaskLinks/")

    def create_generic_task_link(self, data: Dict[str, Any]) -> Optional[GenericTaskLink]:
        response_data = self._make_request("/genericTaskLinks/", method="POST", data=data)
        if response_data:
            obj = GenericTaskLink(response_data, self)
            self._cache.set(GenericTaskLink, obj.id, obj)
            return obj
        return None

    def update_generic_task_link(self, object_id: int, data: Dict[str, Any]) -> Optional[GenericTaskLink]:
        return self._put_full_update(GenericTaskLink, "/genericTaskLinks", object_id, data)
