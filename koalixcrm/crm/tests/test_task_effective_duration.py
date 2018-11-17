import datetime
import pytest
from django.test import TestCase
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_work import StandardWorkFactory
from koalixcrm.crm.factories.factory_task_status import DoneTaskStatusFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.test_support_functions import make_date_utc
from koalixcrm.crm.factories.factory_estimation import StandardHumanResourceEstimationToTaskFactory


@pytest.fixture()
def freeze(monkeypatch):
    """ Now() manager patches date return a fixed, settable, value
        (freezes date)
    """
    original = datetime.date

    class FreezeMeta(type):
        def __instancecheck__(self, instance):
            if instance.isinstance(original) or instance.isinstance(Freeze):
                return True

    class Freeze(datetime.datetime):
        __metaclass__ = FreezeMeta

        @classmethod
        def freeze(cls, val):
            cls.frozen = val

        @classmethod
        def today(cls):
            return cls.frozen

        @classmethod
        def delta(cls, timedelta=None, **kwargs):
            """ Moves time fwd/bwd by the delta"""
            from datetime import timedelta as td
            if not timedelta:
                timedelta = td(**kwargs)
            cls.frozen += timedelta

    monkeypatch.setattr(datetime, 'date', Freeze)
    Freeze.freeze(original.today())
    return Freeze


class TaskEffectiveDuration(TestCase):

    @pytest.fixture(autouse=True)
    def freeze_time(self, freeze):
        self._freeze = freeze

    def setUp(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        start_date = (datetime_now - datetime.timedelta(days=30))
        end_date_first_task = (datetime_now + datetime.timedelta(days=30))
        end_date_second_task = (datetime_now + datetime.timedelta(days=60))

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
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
    def test_effective_duration(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        datetime_later_1 = make_date_utc(datetime.datetime(2024, 1, 2, 2, 00))
        datetime_later_2 = make_date_utc(datetime.datetime(2024, 1, 2, 3, 30))
        datetime_later_3 = make_date_utc(datetime.datetime(2024, 1, 4, 5, 45))
        datetime_later_4 = make_date_utc(datetime.datetime(2024, 1, 4, 6, 15))
        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "0")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "0")

        new_status = DoneTaskStatusFactory.create()
        self._freeze.freeze(datetime.date(2024, 2, 2))
        self.test_1st_task.status = new_status
        self.test_1st_task.save()
        self._freeze.freeze(datetime.date(2024, 2, 5))
        self.test_2nd_task.status = new_status
        self.test_2nd_task.save()

        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "62")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "65")

        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_now,
            start_time=datetime_now,
            stop_time=datetime_later_1,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_later_2,
            start_time=datetime_later_1,
            stop_time=datetime_later_2,
            task=self.test_1st_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_now,
            start_time=datetime_now,
            stop_time=datetime_later_3,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )
        StandardWorkFactory.create(
            human_resource=self.human_resource,
            date=datetime_later_4,
            start_time=datetime_now,
            stop_time=datetime_later_4,
            task=self.test_2nd_task,
            reporting_period=self.test_reporting_period
        )

        self.assertEqual(
            (self.test_1st_task.planned_duration()).__str__(), "60")
        self.assertEqual(
            (self.test_1st_task.effective_duration()).__str__(), "1")
        self.assertEqual(
            (self.test_2nd_task.planned_duration()).__str__(), "90")
        self.assertEqual(
            (self.test_2nd_task.effective_duration()).__str__(), "3")
