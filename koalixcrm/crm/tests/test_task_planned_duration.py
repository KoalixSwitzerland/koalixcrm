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
from koalixcrm.crm.factories.factory_estimation import StandardHumanResourceEstimationToTaskFactory
from koalixcrm.global_support_functions import make_date_utc


class TaskPlannedDuration(TestCase):
    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date_first_task = (datetime_now + datetime.timedelta(days=30)).date()
        end_date_second_task = (datetime_now + datetime.timedelta(days=60)).date()

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_reporting_period.project)
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory(task=self.test_1st_task,
                                                                                date_from=start_date,
                                                                                date_until=end_date_first_task)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_reporting_period.project)
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory(task=self.test_2nd_task,
                                                                                date_from=start_date,
                                                                                date_until=end_date_second_task)

    @pytest.mark.back_end_tests
    def test_task_planned_duration(self):
        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.planned_costs()).__str__(), "0.00")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.planned_costs()).__str__(), "0.00")
