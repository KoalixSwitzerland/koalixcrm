import pytest
from selenium.webdriver.support.ui import Select
from koalixcrm.test.test_support_functions import *
from koalixcrm.test.UITests import UITests
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory


class TimeTrackingAddRow(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)

    def tearDown(self):
        super().tearDown()

    @pytest.mark.front_end_tests
    def test_add_new_row(self):
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
        username = selenium.find_element('xpath', '//*[@id="id_username"]')
        password = selenium.find_element('xpath', '//*[@id="id_password"]')
        submit_button = selenium.find_element('xpath', '/html/body/div/article/div/div/form/div/ul/li/input')
        username.send_keys("admin")
        password.send_keys("admin")
        submit_button.send_keys(Keys.RETURN)
        time.sleep(5)
        selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/time_tracking/'))
        # after the login, the browser is redirected to the target url /koalixcrm/crm/reporting/time_tracking
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_next_steps'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        # Because the user is not equipped with a corresponding human_resource, the user must receive an exception
        # screen giving im the possibility to select what he wants to do next
        # In this test_step it is checked whether the form contains the required fields. the test will then select
        # to return to the start page instead of defining a new human resource

        fail_when_element_does_not_exist(self, '//*[@id="id_next_steps"]')
        fail_when_element_does_not_exist(self, '//*[@name="confirm_selection"]')
        submit_button = selenium.find_element('xpath', '/html/body/div/article/div/form/table/tbody/tr[3]/td/input[2]')
        selection = Select(selenium.find_element('xpath', '//*[@id="id_next_steps"]'))
        selection.select_by_value("return_to_start")
        submit_button.send_keys(Keys.RETURN)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'grp-content-title'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        assert_when_element_is_not_equal_to(self, 'grp-content-title', "<h1>Site administration</h1>")

        # Because the user is still not equipped with a corresponding human_resource, the user must
        # receive an exception screen giving im the possibility to select what he wants to do next
        # In this test_step it is checked whether the form contains the required fields. the test will then select
        # to return to the start page instead of defining a new human resource

        selenium.get('%s%s' % (self.live_server_url, '/koalixcrm/crm/reporting/time_tracking/'))
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_next_steps'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        fail_when_element_does_not_exist(self, '//*[@id="id_next_steps"]')
        fail_when_element_does_not_exist(self, '//*[@name="confirm_selection"]')
        submit_button = selenium.find_element('xpath', '/html/body/div/article/div/form/table/tbody/tr[3]/td/input[2]')
        selection = Select(selenium.find_element('xpath', '//*[@id="id_next_steps"]'))
        selection.select_by_value("create_human_resource")
        submit_button.send_keys(Keys.RETURN)
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'grp-content-title'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        assert_when_element_is_not_equal_to(self, 'grp-content-title', "<h1>Add human resource</h1>")

        # This test is passed here, other testcase are performed to ensure proper functionality of this view
        # when the human resource is properly set"
