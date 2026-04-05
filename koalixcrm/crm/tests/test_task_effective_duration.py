import datetime
import pytest
from django.test import TestCase
from koalixcrm.crm.factory.customer_billing_cycle_factory import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factory.customer_factory import StandardCustomerFactory
from koalixcrm.crm.factory.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.products.factory.currency_factory import StandardCurrencyFactory
from koalixcrm.reporting.factory.work_factory import StandardWorkFactory
from koalixcrm.reporting.factory.task_status_factory import DoneTaskStatusFactory
from koalixcrm.reporting.factory.reporting_period_factory import StandardReportingPeriodFactory
from koalixcrm.reporting.factory.human_resource_factory import StandardHumanResourceFactory
from koalixcrm.reporting.factory.task_factory import StandardTaskFactory
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.reporting.factory.estimation_factory import StandardHumanResourceEstimationToTaskFactory


class TaskEffectiveDuration(TestCase):

    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime.now())
        start_first_task = (datetime_now - datetime.timedelta(days=30)).date()
        start_second_task = (datetime_now - datetime.timedelta(days=60)).date()
        end_date_first_task = (datetime_now + datetime.timedelta(days=30)).date()
        end_date_second_task = (datetime_now + datetime.timedelta(days=60)).date()

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.human_resource = StandardHumanResourceFactory.create()
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_reporting_period.project)
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory.create(task=self.test_1st_task,
                                                                                       date_from=start_first_task,
                                                                                       date_until=end_date_first_task)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_reporting_period.project)
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory.create(task=self.test_2nd_task,
                                                                                       date_from=start_second_task,
                                                                                       date_until=end_date_second_task)

    @pytest.mark.back_end_tests
    def test_effective_duration(self):
        datetime_now = make_date_utc(datetime.datetime.now())
        datetime_later_2 = datetime_now+datetime.timedelta(days=1)
        datetime_later_4 = datetime_now+datetime.timedelta(days=3)
        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "Task has not yet ended")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "120")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "Task has not yet ended")

        new_status = DoneTaskStatusFactory.create()
        self.test_1st_task.status = new_status
        self.test_1st_task.save()
        self.test_2nd_task.status = new_status
        self.test_2nd_task.save()

        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "30")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "120")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "60")

        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_now.date(),
            worked_hours="1.00",
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_later_2.date(),
            worked_hours="1.00",
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_now.date(),
            worked_hours="1.00",
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_later_4.date(),
            worked_hours="1.00",
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )

        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "1")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "120")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "3")
