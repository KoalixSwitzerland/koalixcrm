# -*- coding: utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def fail_when_element_does_not_exist(testcase, xpath):
    try:
        testcase.selenium.find_element('xpath', xpath)
    except NoSuchElementException:
        testcase.assertTrue(False, xpath+" should exist but it does not")
        pass


def fail_when_element_exists(testcase, xpath):
    try:
        testcase.selenium.find_element('xpath', xpath)
        testcase.assertTrue(False, xpath+" should not exist but it does")
    except NoSuchElementException:
        pass

def assert_when_element_is_not_equal_to(testcase, xpath, string):
    try:
        element = testcase.selenium.find_element('xpath', xpath)
        if element.text != string:
            print("issue")
    except NoSuchElementException:
        return


def create_sales_document_from_reference(test_case,
                                         timeout,
                                         reference_type,
                                         reference_id,
                                         document_type,
                                         action_name,
                                         template_name,
                                         template_to_select):
    selenium = test_case.selenium
    selenium.get('%s%s' % (test_case.live_server_url, '/admin/crm/'+reference_type+'/'))
    time.sleep(1)
    fail_when_element_does_not_exist(test_case,
                                       '/html/body/div/article/div/form/section/div/table/tbody/tr/td[1]/input')
    fail_when_element_does_not_exist(test_case, '/html/body/div/article/div/form/footer/ul/li/div/select')
    fail_when_element_does_not_exist(test_case, '/html/body/div/article/div/form/footer/ul/li/div/button')
    contract_1 = selenium.find_element('xpath', 
        '/html/body/div/article/div/form/section/div/table/tbody/tr/td[1]/input')
    if not contract_1.is_selected():
        contract_1.send_keys(Keys.SPACE)
    action_create_offer = selenium.find_element('xpath', 
        '/html/body/div/article/div/form/footer/ul/li/div/select/option[@value="'+action_name+'"]')
    action_create_offer.click()
    ok_button = selenium.find_element('xpath', '/html/body/div/article/div/form/footer/ul/li/div/button')
    ok_button.send_keys(Keys.RETURN)
    time.sleep(1)
    try:
        element_present = expected_conditions.presence_of_element_located((By.ID, 'id_title'))
        WebDriverWait(selenium, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    fail_when_element_does_not_exist(test_case, '/html/body/div/article/ul/li')
    document_type_template = selenium.find_element('xpath', 
        '//*[@id="id_'+template_name+'"]/option[@value="' +
        template_to_select.id.__str__() + '"]')
    document_type_template.click()
    save_button = selenium.find_element('xpath', '/html/body/div/article/div/form/div/footer/ul/li[2]/input')
    save_button.send_keys(Keys.RETURN)
    time.sleep(1)
    selenium.get('%s%s' % (test_case.live_server_url, '/admin/crm/'+reference_type+'/'))
    contract_1 = selenium.find_element('xpath', 
        '/html/body/div/article/div/form/section/div/table/tbody/tr/td[1]/input')
    if not contract_1.is_selected():
        contract_1.send_keys(Keys.SPACE)
    action_create_sales_document = selenium.find_element('xpath', 
        '/html/body/div/article/div/form/footer/ul/li/div/select/option[@value="'+action_name+'"]')
    action_create_sales_document.click()
    ok_button = selenium.find_element('xpath', '/html/body/div/article/div/form/footer/ul/li/div/button')
    ok_button.send_keys(Keys.RETURN)
    time.sleep(1)
    try:
        element_present = expected_conditions.presence_of_element_located((By.ID, 'id_title'))
        WebDriverWait(selenium, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    sales_documents = document_type.objects.filter(contract=test_case.test_contract)
    for sales_document in sales_documents:
        if sales_document.id != reference_id:
            test_case.assertEqual(type(sales_document), document_type)
