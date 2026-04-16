import datetime
import pytest
from django.test import TestCase
from tests.factories.contacts.user_factory import AdminUserFactory
from tests.factories.contacts.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.customer_group_factory import StandardCustomerGroupFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.reporting.reporting_period_factory import StandardReportingPeriodFactory
from tests.factories.djangoUserExtension.factory_user_extension import StandardUserExtensionFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.estimation_factory import StandardEstimationToTaskFactory
from tests.factories.reporting.human_resource_factory import StandardHumanResourceFactory
from tests.factories.reporting.resource_price_factory import StandardResourcePriceFactory
from tests.factories.core.unit_factory import StandardUnitFactory


class TaskPlannedEffort(TestCase):
    def setUp(self):
        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_unit = StandardUnitFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_human_resource = StandardHumanResourceFactory.create()
        self.resource_price = StandardResourcePriceFactory.create(
            resource=self.test_human_resource,
            unit=self.test_unit,
            currency=self.test_currency,
            customer_group=self.test_customer_group,
            price="120",
        )
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_reporting_period.project)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_reporting_period.project)

    @pytest.mark.back_end_tests
    def test_task_planned_costs(self):
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="2.00",
                                               task=self.test_1st_task,
                                               reporting_period=self.test_reporting_period)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="4.75",
                                               task=self.test_2nd_task,
                                               reporting_period=self.test_reporting_period)
        self.assertEqual(
            (self.test_1st_task.planned_effort()).__str__(), "2.00")
        self.assertEqual(
            (self.test_1st_task.planned_costs()).__str__(), "240.0000")
        self.assertEqual(
            (self.test_2nd_task.planned_effort()).__str__(), "4.75")
        self.assertEqual(
            (self.test_2nd_task.planned_costs()).__str__(), "570.0000")
