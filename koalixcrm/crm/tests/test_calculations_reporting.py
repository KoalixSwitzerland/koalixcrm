from django.test import TestCase
from django.test import LiveServerTestCase
from koalixcrm.crm.models import Project
from koalixcrm.crm.models import ReportingPeriod
from koalixcrm.crm.models import Customer
from koalixcrm.crm.models import Currency
from koalixcrm.crm.models import Task
from koalixcrm.crm.models import TaskStatus
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.djangoUserExtension.models import TemplateSet
from koalixcrm.crm.models import Work
from koalixcrm.crm.models import EmployeeAssignmentToTask
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_billing_cycle import StandardCustomerBillingCycleFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import pytest
from koalixcrm.crm.tests.test_support_functions import *


class ReportingCalculationsTest(TestCase):
    def setUp(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        start_date = (datetime_now - datetime.timedelta(days=30)).date()
        end_date_first_task = (datetime_now + datetime.timedelta(days=30)).date()
        end_date_second_task = (datetime_now + datetime.timedelta(days=60)).date()
        date_now = datetime_now.date()

        self.test_billing_cycle = StandardCustomerBillingCycleFactory.create()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        test_task_status = TaskStatus.objects.create(
            title="planned",
            description="This represents the state when something has been planned but not yet started",
            is_done=False
        )
        Task.objects.create(
            title="Test Task",
            planned_start_date=start_date,
            planned_end_date=end_date_first_task,
            project=self.test_reporting_period.project,
            description="This is a simple test task",
            status=test_task_status,
            last_status_change=date_now
        )
        Task.objects.create(
            title="2nd Test Task",
            planned_start_date=start_date,
            planned_end_date=end_date_second_task,
            project=self.test_reporting_period.project,
            description="This is an other simple test task",
            status=test_task_status,
            last_status_change=date_now
        )

    @pytest.mark.back_end_tests
    def test_calculation_of_reported_hours(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        datetime_later_1 = datetime.datetime(2024, 1, 1, 2, 00)
        datetime_later_2 = datetime.datetime(2024, 1, 1, 3, 30)
        datetime_later_3 = datetime.datetime(2024, 1, 1, 5, 45)
        datetime_later_4 = datetime.datetime(2024, 1, 1, 6, 15)
        date_now = datetime_now.date()
        test_task_first = Task.objects.get(title="Test Task")
        test_task_second = Task.objects.get(title="2nd Test Task")
        self.assertEqual(
            (test_task_first.planned_duration()).__str__(), "60")
        self.assertEqual(
            (test_task_first.planned_effort()).__str__(), "0")
        self.assertEqual(
            (test_task_second.planned_duration()).__str__(), "90")
        self.assertEqual(
            (test_task_second.planned_effort()).__str__(), "0")
        test_employee = UserExtension.objects.get(user=self.test_user)
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="2.00",
            task=test_task_first
        )
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="1.50",
            task=test_task_first
        )
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="4.75",
            task=test_task_second
        )
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="3.25",
            task=test_task_second
        )
        self.assertEqual(
            (test_task_first.planned_effort()).__str__(), "3.50")
        self.assertEqual(
            (test_task_first.effective_effort(reporting_period=None)).__str__(), "0.0")
        self.assertEqual(
            (test_task_second.planned_effort()).__str__(), "8.00")
        self.assertEqual(
            (test_task_second.effective_effort(reporting_period=None)).__str__(), "0.0")
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_1,
            short_description="Not really relevant",
            description="Performed some hard work",
            task=test_task_first,
            reporting_period=self.test_reporting_period
        )
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_later_1,
            stop_time=datetime_later_2,
            short_description="Not really relevant 2nd part",
            description="Performed some hard work 2nd part",
            task=test_task_first,
            reporting_period=self.test_reporting_period
        )
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_3,
            short_description="Not really relevant",
            description="Performed some hard work",
            task=test_task_second,
            reporting_period=self.test_reporting_period
        )
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later_4,
            short_description="Not really relevant 2nd part",
            description="Performed some hard work 2nd part",
            task=test_task_second,
            reporting_period=self.test_reporting_period
        )
        self.assertEqual(
            (test_task_first.effective_effort(reporting_period=None)).__str__(), "3.5")
        self.assertEqual(
            (test_task_second.effective_effort(reporting_period=None)).__str__(), "12.0")
        self.assertEqual(
            (self.test_reporting_period.project.effective_effort(reporting_period=None)).__str__(), "15.5")
        self.assertEqual(
            (self.test_reporting_period.project.planned_effort()).__str__(), "11.50")


class ReportingCalculationsUITest(LiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.set_headless(headless=True)
        self.selenium = webdriver.Firefox(firefox_options=firefox_options)
        prepare_test = ReportingCalculationsTest()
        prepare_test.setUp()

    def tearDown(self):
        self.selenium.quit()

    @pytest.mark.front_end_tests
    def test_registration_of_work(self):
        selenium = self.selenium
        # login
        selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/time_tracking/'))
        # the browser will be redirected to the login page
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'id_username'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        username = selenium.find_element_by_xpath('//*[@id="id_username"]')
        password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        submit_button = selenium.find_element_by_xpath('/html/body/div/article/div/div/form/div/ul/li/input')
        username.send_keys("admin")
        password.send_keys("admin")
        submit_button.send_keys(Keys.RETURN)
        # after the login, the browser is redirected to the target url /koalixcrm/crm/reporting/time_tracking
        try:
            element_present = EC.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-project"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-task"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-date"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-start_time"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-stop_time"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-description"]')
        assert_when_element_does_not_exist(self, 'save')
        # check existence of a second form before pressing add more
        assert_when_element_exists(self, '//*[@id="id_form-1-project"]')
        add_more_button = selenium.find_element_by_xpath('//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        # check existence of a second form before pressing add more
        assert_when_element_does_not_exist(self, '//*[@id="id_form-1-project"]')
