# -*- coding: utf-8 -*-
import pytest
import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from koalixcrm.test_support_functions import *
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.crm.factories.factory_reporting_period import StandardReportingPeriodFactory
from koalixcrm.crm.factories.factory_task import StandardTaskFactory
from koalixcrm.crm.reporting.work import Work
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory


class TimeTrackingWorkEntry(LiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.set_headless(headless=True)
        self.selenium = webdriver.Firefox(firefox_options=firefox_options)
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_human_resource = StandardHumanResourceFactory.create(user=self.test_user_extension)
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_reporting_period = StandardReportingPeriodFactory.create()
        self.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                        project=self.test_reporting_period.project,
                                                        )

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
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_username'))
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
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-project"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-task"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-date"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-start_time"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-stop_time"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-worked_hours"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-description"]')
        assert_when_element_does_not_exist(self, 'save')
        project = selenium.find_element_by_xpath('//*[@id="id_form-0-project"]')
        task = selenium.find_element_by_xpath('//*[@id="id_form-0-task"]')
        date = selenium.find_element_by_xpath('//*[@id="id_form-0-date"]')
        start_time = selenium.find_element_by_xpath('//*[@id="id_form-0-start_time"]')
        stop_time = selenium.find_element_by_xpath('//*[@id="id_form-0-stop_time"]')
        description = selenium.find_element_by_xpath('//*[@id="id_form-0-description"]')
        project.send_keys(self.test_reporting_period.project.id.__str__())
        date.send_keys(datetime.date.today().__str__())
        start_time.send_keys(datetime.time(11, 55).__str__())
        stop_time.send_keys(datetime.time(12, 55).__str__())
        description.send_keys("This is a test work entered through the front-end")
        task.send_keys(self.test_1st_task.id.__str__())
        save_button = selenium.find_element_by_name('save')
        save_button.send_keys(Keys.RETURN)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-1-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        assert_when_element_does_not_exist(self, '//*[@id="id_form-1-task"]')
        work = Work.objects.get(description="This is a test work entered through the front-end")
        self.assertEqual(type(work), Work)
