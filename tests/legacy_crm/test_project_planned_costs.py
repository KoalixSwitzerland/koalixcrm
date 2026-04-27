import datetime

import pytest
from django.test import TestCase

from koalixcrm.global_support_functions import make_date_utc
from tests.factories.contacts.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)
from tests.factories.contacts.customer_factory import StandardCustomerFactory
from tests.factories.contacts.customer_group_factory import StandardCustomerGroupFactory
from tests.factories.contacts.user_factory import AdminUserFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.djangoUserExtension.factory_user_extension import (
    StandardUserExtensionFactory,
)
from tests.factories.reporting.estimation_factory import (
    StandardEstimationToTaskFactory,
    StandardHumanResourceEstimationToTaskFactory,
)
from tests.factories.reporting.human_resource_factory import (
    StandardHumanResourceFactory,
)
from tests.factories.reporting.project_factory import StandardProjectFactory
from tests.factories.reporting.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from tests.factories.reporting.resource_price_factory import (
    StandardResourcePriceFactory,
)
from tests.factories.reporting.task_factory import StandardTaskFactory


class TaskPlannedEffort(TestCase):
    def setUp(self):
        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_unit = StandardUnitFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_project = StandardProjectFactory.create()
        self.test_human_resource = StandardHumanResourceFactory.create()

    @pytest.mark.back_end_tests
    def test_project_planned_costs(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date_first_task = (datetime_now + datetime.timedelta(days=30)).date()
        end_date_second_task = (datetime_now + datetime.timedelta(days=60)).date()
        self.assertEqual(
            (self.test_project.planned_costs()).__str__(), "0")
        self.test_reporting_period = StandardReportingPeriodFactory.create(
            project=self.test_project
        )
        self.assertEqual(
            (self.test_project.planned_costs()).__str__(), "0")
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_project)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_project)
        self.assertEqual(
            (self.test_project.planned_costs()).__str__(), "0")
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory(task=self.test_1st_task,
                                                                                date_from=start_date,
                                                                                date_until=end_date_first_task,
                                                                                amount=0)
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory(task=self.test_2nd_task,
                                                                                date_from=start_date,
                                                                                date_until=end_date_second_task,
                                                                                amount=0)
        self.resource_price = StandardResourcePriceFactory.create(
            resource=self.test_human_resource,
            unit=self.test_unit,
            currency=self.test_currency,
            party_group=self.test_customer_group,
            price="120",
        )
        self.assertEqual(
            (self.test_project.planned_costs()).__str__(), "0.00")
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="2.00",
                                               task=self.test_1st_task,
                                               reporting_period=self.test_reporting_period)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="1.50",
                                               task=self.test_1st_task,
                                               reporting_period=self.test_reporting_period)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="4.75",
                                               task=self.test_2nd_task,
                                               reporting_period=self.test_reporting_period)
        StandardEstimationToTaskFactory.create(resource=self.test_human_resource,
                                               amount="3.25",
                                               task=self.test_2nd_task,
                                               reporting_period=self.test_reporting_period)
        self.assertEqual(
            (self.test_project.planned_costs(reporting_period=self.test_reporting_period)).__str__(), "0")
