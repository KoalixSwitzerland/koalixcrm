# -*- coding: utf-8 -*-
import pytest
import datetime
from koalixcrm.test.test_support_functions import *
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.reporting.work import Work
from koalixcrm.test.UITests import UITests
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory


class TimeTrackingWorkEntry(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_human_resource = StandardHumanResourceFactory.create(user=self.test_user_extension)
        self.test_currency = StandardCurrencyFactory.create()
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_1st_task = StandardTaskFactory.create(
            title="1st Test Task",
            project=self.test_reporting_period.project,)

    def tearDown(self):
        super().tearDown()

    @pytest.mark.front_end_tests
    def test_delete_of_new_blank_row(self):
        # login
        self.selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/time_tracking/'))
        # the browser will be redirected to the login page
        timeout = 5
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_username'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        username = self.selenium.find_element('xpath', '//*[@id="id_username"]')
        password = self.selenium.find_element('xpath', '//*[@id="id_password"]')
        submit_button = self.selenium.find_element('xpath', '/html/body/div/article/div/div/form/div/ul/li/input')
        username.send_keys("admin")
        password.send_keys("admin")
        submit_button.send_keys(Keys.RETURN)
        time.sleep(5)
        self.selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/time_tracking/'))
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-project"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-task"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_0"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_0"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_1"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_1"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-worked_hours"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-description"]')
        fail_when_element_does_not_exist(self, '//*[@name="save"]')
        # check existence of a second form before pressing add more
        fail_when_element_exists(self, '//*[@id="id_form-1-project"]')
        add_more_button = self.selenium.find_element('xpath', '//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        time.sleep(1)
        # check existence of a second form after pressing add more
        fail_when_element_does_not_exist(self, '//*[@id="id_form-1-project"]')
        add_more_button = self.selenium.find_element('xpath', '//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        delete_form = expected_conditions.presence_of_element_located((By.ID, 'id_form-1-DELETE'))
        delete_checkbox = self.selenium.find_element(By.ID, 'id_form-1-DELETE')
        if not delete_checkbox.is_selected():
            delete_checkbox.send_keys(Keys.SPACE)
        # check existence of a second form after pressing add more
        fail_when_element_does_not_exist(self, '//*[@id="id_form-2-project"]')
        project = self.selenium.find_element('xpath', '//*[@id="id_form-2-project"]')
        datetime_start_date = self.selenium.find_element('xpath', '//*[@id="id_form-2-datetime_start_0"]')
        datetime_start_time = self.selenium.find_element('xpath', '//*[@id="id_form-2-datetime_start_1"]')
        datetime_stop_date = self.selenium.find_element('xpath', '//*[@id="id_form-2-datetime_stop_0"]')
        datetime_stop_time = self.selenium.find_element('xpath', '//*[@id="id_form-2-datetime_stop_1"]')
        description = self.selenium.find_element('xpath', '//*[@id="id_form-2-description"]')
        project.send_keys(self.test_reporting_period.project.id.__str__())
        datetime_start_date.send_keys(datetime.date.today().__str__())
        datetime_stop_date.send_keys(datetime.date.today().__str__())
        datetime_start_time.send_keys(datetime.time(11, 55).__str__())
        datetime_stop_time.send_keys(datetime.time(12, 55).__str__())
        description.send_keys("This is a test work entered through the front-end")
        task = self.selenium.find_element('xpath', '//*[@id="id_form-2-task"]/option[text()="'+self.test_1st_task.title+'"]')
        task.click()
        save_button = self.selenium.find_element('xpath', '//*[@name="save"]')
        save_button.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-1-project'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        fail_when_element_does_not_exist(self, '//*[@id="id_form-1-task"]')
        fail_when_element_exists(self, '//*[@id="id_form-2-task"]')
        work = Work.objects.get(description="This is a test work entered through the front-end")
        self.assertEqual(type(work), Work)
        work.delete()
