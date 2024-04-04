import datetime
import pytest
from django.test import TestCase
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_estimation import StandardEstimationToTaskFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_resource_price import StandardResourcePriceFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory


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
