# -*- coding: utf-8 -*-
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from tests.e2e.support_functions import *
from tests.e2e.UITests import UITests
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory


class TestProjectAdminView(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()

    def tearDown(self):
        super().tearDown()

    @pytest.mark.front_end_tests
    def test_project_admin(self):
        selenium = self.selenium
        # login
        selenium.get('%s%s' % (self.live_server_url, '/admin/reporting/project/'))
        # the browser will be redirected to the login page
        timeout = 10
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_username'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        username = selenium.find_element('xpath', '//*[@id="id_username"]')
        password = selenium.find_element('xpath', '//*[@id="id_password"]')
        username.send_keys("admin")
        password.send_keys("admin")
        time.sleep(5)
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/reporting/project/'))
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID,
                                                                               '/html/body/div/article/header/ul/li/a'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        selenium.get('%s%s' % (self.live_server_url, '/admin/reporting/project/add'))

        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_project_status'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
