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
from koalixcrm.crm.reporting.task import Task


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


class TaskConstructorTest(TestCase):

    @pytest.fixture(autouse=True)
    def freeze_time(self, freeze):
        self._freeze = freeze

    def setUp(self):

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_reporting_period = StandardReportingPeriodFactory.create()

    def test_task_constructor(self):
        self._freeze.freeze(datetime.date(2024, 6, 2))
        task_minimal_1 = Task.objects.create(
            project=self.test_reporting_period.project,
        )
        task_minimal_1.save()
        self.assertEquals(task_minimal_1.last_status_change, datetime.date(2024, 6, 2))
        self._freeze.freeze(datetime.date(2018, 6, 15))
        task_minimal_2 = Task.objects.create(
            project=self.test_reporting_period.project,
        )
        task_minimal_2.save()
        self.assertEquals(task_minimal_2.last_status_change, datetime.date(2018, 6, 15))
