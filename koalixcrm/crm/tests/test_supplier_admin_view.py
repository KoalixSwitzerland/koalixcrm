# -*- coding: utf-8 -*-
import pytest
from koalixcrm.test.test_support_functions import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.test.UITests import UITests


class TestSupplierAdminView(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()

    def tearDown(self):
        super().tearDown()

    @pytest.mark.front_end_tests
    def test_supplier_admin(self):
        # login
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/crm/supplier/'))
        # the browser will be redirected to the login page
        timeout = 10
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
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/crm/supplier/'))
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID,
                                                                               '/html/body/div/article/header/ul/li/a'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/crm/supplier/add'))

        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_name'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        name = self.selenium.find_element('xpath', '//*[@id="id_name"]')
        name.send_keys("This is the name of a supplier")
        submit_button = self.selenium.find_element('xpath', '/html/body/div/article/div/form/div/footer/ul/li[1]/input')
        submit_button.send_keys(Keys.RETURN)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID,
                                                                               '/html/body/div/article/header/ul/li/a'))
            WebDriverWait(self.selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        supplier = Supplier.objects.get(name="This is the name of a supplier")
        self.assertEqual(type(supplier), Supplier)

