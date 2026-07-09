# -*- coding: utf-8 -*-

import pytest

from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.models.quotation import Quotation
from tests.e2e.support_functions import *
from tests.e2e.UITests import UITests
from koalixcrm.contacts.tests.factories.customer_group_factory import StandardCustomerGroupFactory
from koalixcrm.contacts.tests.factories.user_factory import AdminUserFactory
from koalixcrm.contracts.tests.factories.contract_factory import StandardContractFactory
from koalixcrm.djangoUserExtension.tests.factories.document_template_factory import (
    StandardInvoiceTemplateFactory,
    StandardPurchaseOrderTemplateFactory,
    StandardQuotationTemplateFactory,
)


class CreateSalesDocumentFromContract(UITests):

    def setUp(self):
        super().setUp()
        self.test_user = AdminUserFactory.create()
        self.test_customer_group = StandardCustomerGroupFactory.create()
        self.test_contract = StandardContractFactory.create()
        self.test_quotation_template = StandardQuotationTemplateFactory.create()
        self.test_invoice_template = StandardInvoiceTemplateFactory.create()
        self.test_purchase_order_template = StandardPurchaseOrderTemplateFactory.create()

    def tearDown(self):
        super().tearDown()

    @pytest.mark.front_end_tests
    def test_create_sales_document_from_contract(self):
        selenium = self.selenium
        # login
        selenium.get('%s%s' % (self.live_server_url, '/admin/contract_object_management/contract/'))
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
                                           "template_to_select": self.test_purchase_order_template}
                           }
        for document_type in test_parameters:
            test_parameter = test_parameters[document_type]
            create_commercial_document_from_reference(test_case=self,
                                                 timeout=timeout,
                                                 document_type=document_type,
                                                 reference_type="contract",
                                                 reference_id=self.test_contract,
                                                 action_name=test_parameter["action_name"],
                                                 template_name=test_parameter["template_name"],
                                                 template_to_select=test_parameter["template_to_select"])
