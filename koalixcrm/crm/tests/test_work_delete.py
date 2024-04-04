import datetime
import pytest
from django.test import TestCase
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_work import StandardWorkFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_reporting_period_status import DoneReportingPeriodStatusFactory
from koalixcrm.crm.factories.factory_estimation import StandardHumanResourceEstimationToTaskFactory
from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.crm.exceptions import ReportingPeriodDoneDeleteNotPossible


class TestWorkDelete(TestCase):
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
        self.human_resource = StandardHumanResourceFactory.create()
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
    def test_work_delete(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        datetime_later_1 = make_date_utc(datetime.datetime(2024, 1, 1, 2, 00))
        datetime_later_2 = make_date_utc(datetime.datetime(2024, 1, 1, 3, 30))
        self.datetime_later_3 = make_date_utc(datetime.datetime(2024, 1, 1, 5, 45))
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
        work_cannot_be_deleted = StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=date_now,
            start_time=datetime_now,
            stop_time=self.datetime_later_3,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        work_can_be_deleted = StandardWorkFactory.create(
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
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "12")
        work_can_be_deleted.delete()
        self.assertEqual(
            (self.test_1st_task.effective_effort(reporting_period=None)).__str__(), "3.5")
        self.assertEqual(
            (self.test_2nd_task.effective_effort(reporting_period=None)).__str__(), "5.75")
        status_done = DoneReportingPeriodStatusFactory.create()
        self.test_reporting_period.status = status_done
        with pytest.raises(ReportingPeriodDoneDeleteNotPossible):
            work_cannot_be_deleted.delete()
        with pytest.raises(ReportingPeriodDoneDeleteNotPossible):
            work_cannot_be_deleted.stop_time = self.datetime_later_3
            work_cannot_be_deleted.save()

