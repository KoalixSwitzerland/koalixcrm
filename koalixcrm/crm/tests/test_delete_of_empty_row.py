# -*- coding: utf-8 -*-
import pytest
import time
import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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


class TimeTrackingWorkEntry(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TimeTrackingWorkEntry, cls).setUpClass()
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.set_headless(headless=True)
        cls.selenium = webdriver.Firefox(firefox_options=firefox_options)
        cls.selenium.implicitly_wait(10)
        cls.test_user = AdminUserFactory.create()
        cls.test_customer_group = StandardCustomerGroupFactory.create()
        cls.test_customer = StandardCustomerFactory.create(is_member_of=(cls.test_customer_group,))
        cls.test_user_extension = StandardUserExtensionFactory.create(user=cls.test_user)
        cls.test_human_resource = StandardHumanResourceFactory.create(user=cls.test_user_extension)
        cls.test_currency = StandardCurrencyFactory.create()
        cls.test_reporting_period = StandardReportingPeriodFactory.create()
        cls.test_1st_task = StandardTaskFactory.create(title="1st Test Task",
                                                       project=cls.test_reporting_period.project,
                                                       )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TimeTrackingWorkEntry, cls).tearDownClass()

    @pytest.mark.front_end_tests
    def test_delete_of_new_blank_row(self):
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
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_0]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_0"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_1]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_1"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-worked_hours"]')
        assert_when_element_does_not_exist(self, '//*[@id="id_form-0-description"]')
        assert_when_element_does_not_exist(self, 'save')
        # check existence of a second form before pressing add more
        assert_when_element_exists(self, '//*[@id="id_form-1-project"]')
        add_more_button = selenium.find_element_by_xpath('//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        time.sleep(1)
        # check existence of a second form after pressing add more
        assert_when_element_does_not_exist(self, '//*[@id="id_form-1-project"]')
        add_more_button = selenium.find_element_by_xpath('//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        delete_form = selenium.find_element_by_id('id_form-1-DELETE')
        if not delete_form.is_selected():
            delete_form.send_keys(Keys.SPACE)
        # check existence of a second form after pressing add more
        assert_when_element_does_not_exist(self, '//*[@id="id_form-2-project"]')
        project = selenium.find_element_by_xpath('//*[@id="id_form-2-project"]')
        datetime_start_date = selenium.find_element_by_xpath('//*[@id="id_form-2-datetime_start_0"]')
        datetime_start_time = selenium.find_element_by_xpath('//*[@id="id_form-2-datetime_start_1"]')
        datetime_stop_date = selenium.find_element_by_xpath('//*[@id="id_form-2-datetime_stop_0"]')
        datetime_stop_time = selenium.find_element_by_xpath('//*[@id="id_form-2-datetime_stop_1"]')
        description = selenium.find_element_by_xpath('//*[@id="id_form-2-description"]')
        project.send_keys(self.test_reporting_period.project.id.__str__())
        datetime_start_date.send_keys(datetime.date.today().__str__())
        datetime_stop_date.send_keys(datetime.date.today().__str__())
        datetime_start_time.send_keys(datetime.time(11, 55).__str__())
        datetime_stop_time.send_keys(datetime.time(12, 55).__str__())
        description.send_keys("This is a test work entered through the front-end")
        task = selenium.find_element_by_xpath('//*[@id="id_form-2-task"]/option[text()="'+self.test_1st_task.title+'"]')
        task.click()
        save_button = selenium.find_element_by_name('save')
        save_button.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-1-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        assert_when_element_does_not_exist(self, '//*[@id="id_form-1-task"]')
        assert_when_element_exists(self, '//*[@id="id_form-2-task"]')
        work = Work.objects.get(description="This is a test work entered through the front-end")
        self.assertEqual(type(work), Work)
        work.delete()
