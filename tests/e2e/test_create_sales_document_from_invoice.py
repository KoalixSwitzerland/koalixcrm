# -*- coding: utf-8 -*-
import os

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.models.quotation import Quotation
from tests.e2e.support_functions import *
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory
from koalixcrm.contracts.tests.factories.contract_factory import StandardContractFactory
from koalixcrm.contracts.tests.factories.invoice_factory import StandardInvoiceFactory
from koalixcrm.djangoUserExtension.tests.factories.document_template_factory import (
    StandardDespatchAdviceTemplateFactory,
    StandardInvoiceTemplateFactory,
    StandardPaymentReminderTemplateFactory,
    StandardPurchaseOrderTemplateFactory,
    StandardQuotationTemplateFactory,
)


class CreateSalesDocumentFromContract(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(CreateSalesDocumentFromContract, cls).setUpClass()
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(options=chrome_options)
        cls.selenium.implicitly_wait(10)
        cls.test_user = AdminUserFactory.create()
        cls.test_customer_group = StandardCustomerGroupFactory.create()
        cls.test_contract = StandardContractFactory.create()
        cls.test_invoice = StandardInvoiceFactory.create(contract=cls.test_contract)
        cls.test_quotation_template = StandardQuotationTemplateFactory.create()
        cls.test_invoice_template = StandardInvoiceTemplateFactory.create()
        cls.test_purchase_order_template = StandardPurchaseOrderTemplateFactory.create()
        cls.test_payment_reminder_template = StandardPaymentReminderTemplateFactory.create()
        cls.test_despatch_advice_template = StandardDespatchAdviceTemplateFactory.create()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreateSalesDocumentFromContract, cls).tearDownClass()

    def tearDown(self):
        directory = os.getcwd() + "/test_results/Screenshots/"
        os.makedirs(directory, exist_ok=True)
        try:
            name = self._testMethodName
            self.selenium.save_screenshot(directory + "%s.png" % name)
            with open(directory + "%s.html" % name, "w") as fh:
                fh.write(self.selenium.page_source)
            with open(directory + "%s.url" % name, "w") as fh:
                fh.write(self.selenium.current_url)
        except Exception:
            pass
        super(CreateSalesDocumentFromContract, self).tearDown()

    @pytest.mark.front_end_tests
    def test_create_sales_document_from_quote(self):
        selenium = self.selenium
        # login
        selenium.get('%s%s' % (self.live_server_url, '/admin/contract_object_management/invoice/'))
        # the browser will be redirected to the login page
        timeout = 2
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
        # after the login, the browser is redirected to the target url /koalixcrm/crm/contract
        try:
            element_present = expected_conditions.presence_of_element_located((By.ID, 'id_form-0-project'))
            WebDriverWait(selenium, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        test_parameters = {Quotation: {"action_name": "create_quotation",
                                       "template_name": "quotation_template",
                                       "template_to_select": self.test_quotation_template},
                           Invoice: {"action_name": "create_invoice",
                                     "template_name": "invoice_template",
                                     "template_to_select": self.test_invoice_template},
                           PurchaseOrder: {"action_name": "create_purchase_order",
                                           "template_name": "purchase_order_template",
                                           "template_to_select": self.test_purchase_order_template},
                           PaymentReminder: {"action_name": "create_payment_reminder",
                                             "template_name": "payment_reminder_template",
                                             "template_to_select": self.test_payment_reminder_template},
                           DespatchAdvice: {"action_name": "create_despatch_advice",
                                            "template_name": "despatch_advice_template",
                                            "template_to_select": self.test_despatch_advice_template},
                           }
        for document_type in test_parameters:
            test_parameter = test_parameters[document_type]
            create_commercial_document_from_reference(test_case=self,
                                                 timeout=timeout,
                                                 document_type=document_type,
                                                 reference_type="invoice",
                                                 reference_id=self.test_invoice,
                                                 action_name=test_parameter["action_name"],
                                                 template_name=test_parameter["template_name"],
                                                 template_to_select=test_parameter["template_to_select"])
