import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase

from koalixcrm.contacts.tests.factories.customer_billing_cycle_factory import (
    StandardCustomerBillingCycleFactory,
)
from koalixcrm.contacts.tests.factories.customer_factory import StandardCustomerFactory
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.tests.factories.user_extension_factory import (
    StandardUserExtensionFactory,
)
from koalixcrm.reporting.tests.factories.estimation_factory import (
    StandardHumanResourceEstimationToTaskFactory,
)
from koalixcrm.reporting.tests.factories.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory
from koalixcrm.reporting.tests.factories.task_status_factory import DoneTaskStatusFactory


class TaskUpdateLastStatusUpdate(TestCase):

    def setUp(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        datetime_now = datetime_now.replace(tzinfo=ZoneInfo("UTC"))
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
                                                        project=self.test_reporting_period.project,
                                                        last_status_change=datetime.date(2024, 6, 15)
                                                        )
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory.create(task=self.test_1st_task,
                                                                                       date_from=start_date,
                                                                                       date_until=end_date_first_task)
        self.test_2nd_task = StandardTaskFactory.create(title="2nd Test Task",
                                                        project=self.test_reporting_period.project,
                                                        last_status_change=datetime.date(2024, 6, 15))
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory.create(task=self.test_2nd_task,
                                                                                       date_from=start_date,
                                                                                       date_until=end_date_second_task)

    def test_task_last_status_update(self):
        previous_last_status_change = self.test_1st_task.last_status_change
        new_status = DoneTaskStatusFactory.create()
        self.test_1st_task.status = new_status
        self.test_1st_task.save()
        self.assertEqual(previous_last_status_change, datetime.date(2024, 6, 15))
        self.assertEqual(self.test_1st_task.last_status_change, datetime.date.today())
