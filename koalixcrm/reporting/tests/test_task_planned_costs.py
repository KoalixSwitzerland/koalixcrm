import pytest
from django.test import TestCase

from koalixcrm.contacts.tests.factories.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)
from koalixcrm.contacts.tests.factories.customer_factory import StandardCustomerFactory
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.djangoUserExtension.tests.factories.user_extension_factory import (
    StandardUserExtensionFactory,
)
from koalixcrm.reporting.tests.factories.estimation_factory import StandardEstimationToTaskFactory
from koalixcrm.reporting.tests.factories.human_resource_factory import (
    StandardHumanResourceFactory,
)
from koalixcrm.reporting.tests.factories.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from koalixcrm.reporting.tests.factories.resource_price_factory import (
    StandardResourcePriceFactory,
)
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory


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
            party_group=self.test_customer_group,
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
