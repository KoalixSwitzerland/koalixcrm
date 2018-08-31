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
from koalixcrm.crm.factories.factory_work import StandardWorkFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.test_support_functions import make_date_utc


class TaskEffectiveEffort(TestCase):
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
                                                        planned_start_date=start_date,
                                                        planned_end_date=end_date_first_task,
                                                        project=self.test_reporting_period.project)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        planned_start_date=start_date,
                                                        planned_end_date=end_date_second_task,
                                                        project=self.test_reporting_period.project)

    @pytest.mark.back_end_tests
    def test_effective_effort(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        datetime_later_1 = make_date_utc(datetime.datetime(2024, 1, 1, 2, 00))
        datetime_later_2 = make_date_utc(datetime.datetime(2024, 1, 1, 3, 30))
        datetime_later_3 = make_date_utc(datetime.datetime(2024, 1, 1, 5, 45))
        datetime_later_4 = make_date_utc(datetime.datetime(2024, 1, 1, 6, 15))
        date_now = datetime_now.date()
        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.planned_costs()).__str__(), "0")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.planned_costs()).__str__(), "0")
        StandardWorkFactory.create(
            employee=self.test_user_extension,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_1,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            employee=self.test_user_extension,
            date=date_now,
            start_time=datetime_later_1,
            stop_time=datetime_later_2,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            employee=self.test_user_extension,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_3,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            employee=self.test_user_extension,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_4,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        self.assertEqual(
            (self.test_1st_task.effective_effort(reporting_period=None)).__str__(), "3.5")
        self.assertEqual(
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "12.0")
