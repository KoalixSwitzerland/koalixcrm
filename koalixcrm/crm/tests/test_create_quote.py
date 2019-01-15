# -*- coding: utf-8 -*-
import pytest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from koalixcrm.test_support_functions import *
from koalixcrm.crm.factories.factory_contract import StandardContractFactory
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.reporting.work import Work


class CreateQuoteThroughUI(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(CreateQuoteThroughUI, cls).setUpClass()
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.set_headless(headless=False)
        cls.selenium = webdriver.Firefox(firefox_options=firefox_options)
        cls.selenium.implicitly_wait(10)
        cls.test_user = AdminUserFactory.create()
        cls.test_customer_group = StandardCustomerGroupFactory.create()
        cls.test_contract = StandardContractFactory.create()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreateQuoteThroughUI, cls).tearDownClass()

    @pytest.mark.front_end_tests
    def test_create_quote(self):
        selenium = self.selenium
        # login
        selenium.get('%s%s' % (self.live_server_url, '/admin/crm/contract/'))
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
        # after the login, the browser is redirected to the target url /koalixcrm/crm/contract
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        assert_when_element_does_not_exist(self, '/html/body/div/article/div/form/section/div/table/tbody/tr/td[1]/input')
        assert_when_element_does_not_exist(self, '/html/body/div/article/div/form/footer/ul/li/div/select')
        assert_when_element_does_not_exist(self, '/html/body/div/article/div/form/footer/ul/li/div/button')
        contract_1 = selenium.find_element_by_xpath('/html/body/div/article/div/form/section/div/table/tbody/tr/td[1]/input')
        if not contract_1.is_selected():
            contract_1.send_keys(Keys.SPACE)
        action_create_offer = selenium.find_element_by_xpath('/html/body/div/article/div/form/footer/ul/li/div/select/option[@value="create_quote"]')
        action_create_offer.click()
        ok_button = selenium.find_element_by_xpath('/html/body/div/article/div/form/footer/ul/li/div/button')
        ok_button.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_title'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        assert_when_element_does_not_exist(self, '/html/body/div/article/ul/li')
