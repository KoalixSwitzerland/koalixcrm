import datetime
import pytz
from django.test import TestCase
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.crm.factories.factory_task_status import DoneTaskStatusFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_estimation import StandardHumanResourceEstimationToTaskFactory


class TaskUpdateLastStatusUpdate(TestCase):

    def setUp(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        datetime_now = pytz.timezone("UTC").localize(datetime_now, is_dst=None)
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
        self.assertEquals(previous_last_status_change, datetime.date(2024, 6, 15))
        self.assertEqual(self.test_1st_task.last_status_change, datetime.date.today())
