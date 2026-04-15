import datetime
import pytest
from django.test import TestCase
from tests.factories.crm.user_factory import AdminUserFactory
from tests.factories.crm.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from tests.factories.crm.customer_factory import StandardCustomerFactory
from tests.factories.crm.customer_group_factory import StandardCustomerGroupFactory
from tests.factories.settings.unit_factory import StandardUnitFactory
from tests.factories.settings.currency_factory import StandardCurrencyFactory
from tests.factories.reporting.reporting_period_factory import StandardReportingPeriodFactory
from tests.factories.reporting.human_resource_factory import StandardHumanResourceFactory
from tests.factories.reporting.work_factory import StandardWorkFactory
from tests.factories.reporting.task_factory import StandardTaskFactory
from tests.factories.reporting.resource_price_factory import StandardResourcePriceFactory
from tests.factories.reporting.estimation_factory import StandardHumanResourceEstimationToTaskFactory
from koalixcrm.global_support_functions import make_date_utc


class TaskEffectiveCostsWithoutAgreement(TestCase):
    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date_first_task = (datetime_now + datetime.timedelta(days=30)).date()
        end_date_second_task = (datetime_now + datetime.timedelta(days=60)).date()

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_unit = StandardUnitFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create(
            rounding="0.05"
        )
        self.human_resource = StandardHumanResourceFactory.create()
        self.resource_price = StandardResourcePriceFactory.create(
            resource=self.human_resource,
            unit=self.test_unit,
            currency=self.test_currency,
            customer_group=self.test_customer_group,
            price="120",
        )
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_1st_task = StandardTaskFactory.create(
            title="1st Test Task",
            project=self.test_reporting_period.project
        )
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory(
            task=self.test_1st_task,
            date_from=start_date,
            date_until=end_date_first_task
        )
        self.test_2nd_task = StandardTaskFactory.create(
            title="2nd Test Task",
            project=self.test_reporting_period.project
        )
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory(
            task=self.test_2nd_task,
            date_from=start_date,
            date_until=end_date_second_task
        )

    @pytest.mark.back_end_tests
    def test_task_effective_costs_no_agreement(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        datetime_later_1 = make_date_utc(datetime.datetime(2024, 1, 1, 2, 00))
        datetime_later_2 = make_date_utc(datetime.datetime(2024, 1, 1, 3, 30))
        datetime_later_3 = make_date_utc(datetime.datetime(2024, 1, 1, 5, 45))
        datetime_later_4 = make_date_utc(datetime.datetime(2024, 1, 1, 6, 15))
        date_now = datetime_now.date()
        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.planned_costs()).__str__(), "0.00")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.planned_costs()).__str__(), "0.00")
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_1,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=date_now,
            start_time=datetime_later_1,
            stop_time=datetime_later_2,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_3,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_4,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        self.assertEqual(
            (self.test_1st_task.effective_effort(reporting_period=None)).__str__(), "3.5")
        self.assertEqual(
            (self.test_1st_task.effective_costs(reporting_period=None, confirmed=False)).__str__(), "420.00")
        self.assertEqual(
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "12")
        self.assertEqual(
            (self.test_2nd_task.effective_costs(reporting_period=None, confirmed=False)).__str__(), "1440.00")
