# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import EmployeeAssignmentToTask
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory


class StandardEmployeeAssignmentToTaskFactory(factory.Factory):
    class Meta:
        model = EmployeeAssignmentToTask

    employee = factory.SubFactory(StaffUserFactory)
    planned_effort = "112.50"
    task = factory.SubFactory(StandardTaskFactory)
