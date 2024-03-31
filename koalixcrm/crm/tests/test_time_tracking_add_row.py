import pytest
from koalixcrm.test.test_support_functions import *
from koalixcrm.crm.factories.factory_user import AdminUserFactory
from koalixcrm.crm.factories.factory_customer import StandardCustomerFactory
from koalixcrm.crm.factories.factory_customer_group import StandardCustomerGroupFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_human_resource import StandardHumanResourceFactory
from koalixcrm.djangoUserExtension.factories.factory_user_extension import StandardUserExtensionFactory
from koalixcrm.test.UITests import UITests


class TimeTrackingAddRow(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_customer = StandardCustomerFactory.create(is_member_of=(self.test_customer_group,))
        self.test_currency = StandardCurrencyFactory.create()
        self.test_user_extension = StandardUserExtensionFactory.create(user=self.test_user)
        self.test_human_resource = StandardHumanResourceFactory.create(user=self.test_user_extension)

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
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        # find the form element
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-project"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-task"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_0"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_start_1"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_0"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-datetime_stop_1"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-worked_hours"]')
        fail_when_element_does_not_exist(self, '//*[@id="id_form-0-description"]')
        fail_when_element_does_not_exist(self, '//*[@name="save"]')
        # check existence of a second form before pressing add more
        fail_when_element_exists(self, '//*[@id="id_form-1-project"]')
        add_more_button = selenium.find_element('xpath', '//*[@id="add_more"]')
        add_more_button.send_keys(Keys.RETURN)
        # check existence of a second form after pressing add more
        fail_when_element_does_not_exist(self, '//*[@id="id_form-1-project"]')
