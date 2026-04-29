import pytest
from django.test import TestCase

from tests.factories.contacts.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.customer_group_factory import StandardCustomerGroupFactory
from tests.factories.contacts.user_factory import AdminUserFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.djangoUserExtension.factory_user_extension import (
    StandardUserExtensionFactory,
)
from tests.factories.reporting.estimation_factory import StandardEstimationToTaskFactory
from tests.factories.reporting.human_resource_factory import (
    StandardHumanResourceFactory,
)
from tests.factories.reporting.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from tests.factories.reporting.task_factory import StandardTaskFactory


class TaskPlannedEffort(TestCase):
    def setUp(self):
        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_human_resource = StandardHumanResourceFactory.create()
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_reporting_period.project)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_reporting_period.project)

    @pytest.mark.back_end_tests
    def test_task_planned_effort(self):
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="2.00",
                                               task=self.test_1st_task)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="4.75",
                                               task=self.test_2nd_task)
        self.assertEqual(
            (self.test_1st_task.planned_effort()).__str__(), "2.00")
        self.assertEqual(
            (self.test_1st_task.effective_effort(reporting_period=None)).__str__(), "0")
        self.assertEqual(
            (self.test_2nd_task.planned_effort()).__str__(), "4.75")
        self.assertEqual(
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "0")

    @pytest.mark.back_end_tests
    def test_task_planned_effort_old_reporting_period(self):
        self.test_reporting_period.end = '2018-06-16'
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="2.00",
                                               task=self.test_1st_task)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="4.75",
                                               task=self.test_2nd_task)
        self.assertEqual(
            (self.test_1st_task.planned_effort()).__str__(), "2.00")
        self.assertEqual(
            (self.test_1st_task.effective_effort(reporting_period=None)).__str__(), "0")
        self.assertEqual(
            (self.test_2nd_task.planned_effort()).__str__(), "4.75")
        self.assertEqual(
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "0")
