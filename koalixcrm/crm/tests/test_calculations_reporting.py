from django.test import TestCase
from django.test import LiveServerTestCase
from koalixcrm.crm.models import Contract
from koalixcrm.crm.models import Customer
from koalixcrm.crm.models import CustomerGroup
from koalixcrm.crm.models import CustomerBillingCycle
from koalixcrm.crm.models import Currency
from koalixcrm.crm.models import Task
from koalixcrm.crm.models import TaskStatus
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.djangoUserExtension.models import TemplateSet
from koalixcrm.crm.models import Work
from koalixcrm.crm.models import EmployeeAssignmentToTask
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime


class ReportingCalculationsTest(TestCase):
    def setUp(self):
        datetime_now=datetime.datetime(2024, 1, 1, 0, 00)
        start_date=(datetime_now - datetime.timedelta(days=30)).date()
        end_date=(datetime_now + datetime.timedelta(days=30)).date()
        date_now=datetime_now.date()
        test_billing_cycle=CustomerBillingCycle.objects.create(
            name="30 days to pay",
            time_to_payment_date=30,
            payment_reminder_time_to_payment=10
        )
        test_user=User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@admin.com')
        test_customer_group=CustomerGroup.objects.create(
            name="Tripple A"
        )
        test_customer=Customer.objects.create(
            name="John Smith",
            last_modified_by=test_user,
            default_customer_billing_cycle=test_billing_cycle,
        )
        test_customer.is_member_of=[test_customer_group,]
        test_customer.save()
        test_currency=Currency.objects.create(
            description="Swiss Francs",
            short_name="CHF",
            rounding=0.05,
        )
        test_template_set=TemplateSet.objects.create(
            title="Just an empty Template Set"
        )
        UserExtension.objects.create(
            user=test_user,
            defaultTemplateSet = test_template_set,
            defaultCurrency = test_currency
        )
        test_contract=Contract.objects.create(
            staff=test_user,
            description="This is a test contract",
            default_customer=test_customer,
            default_currency=test_currency,
            last_modification=date_now,
            last_modified_by=test_user
        )
        test_task_status=TaskStatus.objects.create(
            title="planned",
            description="This represents the state when something has been planned but not yet started",
            is_done=False
        )
        Task.objects.create(
            short_description="Test Task",
            planned_start_date=start_date,
            planned_end_date=end_date,
            project=test_contract,
            description="This is a simple test task",
            status=test_task_status,
            last_status_change=date_now
        )

    def test_calculate_document_price(self):
        datetime_now = datetime.datetime(2024, 1, 1, 0, 00)
        datetime_later = datetime.datetime(2024, 1, 1, 2, 00)
        datetime_even_later = datetime.datetime(2024, 1, 1, 3, 30)
        date_now = datetime_now.date()
        test_task = Task.objects.get(short_description="Test Task")
        self.assertEqual(
            (test_task.planned_duration()).__str__(), "60 days, 0:00:00")
        self.assertEqual(
            (test_task.planned_effort()).__str__(), "0 h")
        test_user = User.objects.get(username="admin")
        test_employee = UserExtension.objects.get(user=test_user)
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="2.00",
            task=test_task
        )
        EmployeeAssignmentToTask.objects.create(
            employee=test_employee,
            planned_effort="1.50",
            task=test_task
        )
        self.assertEqual(
            (test_task.planned_effort()).__str__(), "3.50 h")
        self.assertEqual(
            (test_task.effective_effort()).__str__(), "0.0 h")
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_now,
            stop_time=datetime_later,
            short_description="Not really relevant",
            description="Performed some hard work",
            task=test_task
        )
        Work.objects.create(
            employee=test_employee,
            date=date_now,
            start_time=datetime_later,
            stop_time=datetime_even_later,
            short_description="Not really relevant 2nd part",
            description="Performed some hard work 2nd part",
            task=test_task
        )
        self.assertEqual(
            (test_task.effective_effort()).__str__(), "3.5 h")


class ReportingCalculationsUITest(LiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.set_headless(headless=True)
        self.selenium = webdriver.Firefox(firefox_options=firefox_options)
        prepare_test = ReportingCalculationsTest()
        prepare_test.setUp()

    def tearDown(self):
        self.selenium.quit()

    def test_registration_of_work(self):
        selenium = self.selenium
        #login
        selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username = selenium.find_element_by_xpath('//*[@id="id_username"]')
        password = selenium.find_element_by_xpath('//*[@id="id_password"]')
        submit_button = selenium.find_element_by_xpath('/html/body/div/article/div/div/form/div/ul/li/input')
        username.send_keys("admin")
        password.send_keys("admin")
        submit_button.send_keys(Keys.RETURN)
        #Opening the link we want to test
        selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/monthlyreport/'))
        #find the form element
        project = selenium.find_element_by_xpath('//*[@id="id_form-0-projects"]')
        task = selenium.find_element_by_xpath('//*[@id="id_form-0-task"]')
        date = selenium.find_element_by_xpath('//*[@id="id_form-0-date"]')
        start_time = selenium.find_element_by_xpath('//*[@id="id_form-0-start_time"]')
        stop_time = selenium.find_element_by_xpath('//*[@id="id_form-0-stop_time"]')
        description = selenium.find_element_by_xpath('//*[@id="id_form-0-description"]')
        save = selenium.find_element_by_name('save')