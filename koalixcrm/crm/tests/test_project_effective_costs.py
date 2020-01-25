import datetime
import pytest
from django.test import TestCase
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.crm.factories.factory_work import StandardWorkFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.factories.factory_resource_price import StandardResourcePriceFactory
from koalixcrm.crm.factories.factory_estimation import StandardHumanResourceEstimationToTaskFactory
from koalixcrm.crm.factories.factory_agreement import StandardAgreementToTaskFactory
from koalixcrm.crm.factories.factory_project import StandardProjectFactory
from koalixcrm.global_support_functions import make_date_utc


class TaskEffectiveCostsWithAgreement(TestCase):
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
        self.human_resource_two = StandardHumanResourceFactory.create()
        self.resource_price = StandardResourcePriceFactory.create(
            resource=self.human_resource,
            unit=self.test_unit,
            currency=self.test_currency,
            customer_group=self.test_customer_group,
            price="120",
        )
        self.resource_price_agreement = StandardResourcePriceFactory.create(
            resource=self.human_resource_two,
            unit=self.test_unit,
            currency=self.test_currency,
            customer_group=self.test_customer_group,
            price="90",
        )
        self.test_project = StandardProjectFactory.create()
        self.test_reporting_period = StandardReportingPeriodFactory.create(
            project=self.test_project
        )
        self.test_1st_task = StandardTaskFactory.create(
            title="1st Test Task",
            project=self.test_project
        )
        self.agreement_1st_task = StandardAgreementToTaskFactory(
            amount="3.50",
            task=self.test_1st_task,
            resource=self.human_resource,
            unit=self.test_unit,
            costs=self.resource_price_agreement
        )
        self.estimation_1st_task = StandardHumanResourceEstimationToTaskFactory(
            resource=self.human_resource,
            task=self.test_1st_task,
            date_from=start_date,
            date_until=end_date_first_task,
            amount=20
        )
        self.test_2nd_task = StandardTaskFactory.create(
            title="2nd Test Task",
            project=self.test_project
        )
        self.estimation_2nd_task = StandardHumanResourceEstimationToTaskFactory(
            resource=self.human_resource,
            task=self.test_2nd_task,
            date_from=start_date,
            date_until=end_date_second_task,
            amount=30
        )

    @pytest.mark.back_end_tests
    def test_project_effective_costs(self):
        datetime_now = make_date_utc(datetime.datetime(2024, 1, 1, 0, 00))
        datetime_later_1 = make_date_utc(datetime.datetime(2024, 1, 1, 2, 00))
        datetime_later_2 = make_date_utc(datetime.datetime(2024, 1, 1, 3, 30))
        datetime_later_3 = make_date_utc(datetime.datetime(2024, 1, 1, 5, 45))
        datetime_later_4 = make_date_utc(datetime.datetime(2024, 1, 1, 6, 15))
        date_now = datetime_now.date()
        self.assertEqual(
            (self.test_project.planned_costs()).__str__(), "6000.0000")
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
            (self.test_project.effective_costs(reporting_period=None, confirmed=False)).__str__(), "1755.00")
