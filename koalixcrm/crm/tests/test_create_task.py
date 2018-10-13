# -*- coding: utf-8 -*-

import pytest
from django.test import TestCase
from koalixcrm.crm.factories.factory_sales_document_position import StandardSalesDocumentPositionFactory
from koalixcrm.crm.factories.factory_currency import StandardCurrencyFactory
from koalixcrm.crm.factories.factory_quote import StandardQuoteFactory
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.crm.factories.factory_product_type import StandardProductTypeFactory
from koalixcrm.crm.factories.factory_product_price import StandardPriceFactory
from koalixcrm.crm.models import Task
from koalixcrm.crm.views.create_task import CreateTaskView


class DocumentCalculationsTest(TestCase):
    def setUp(self):
        self.test_currency = StandardCurrencyFactory.create()
        self.test_quote = StandardQuoteFactory.create()
        self.test_user = StaffUserFactory.create()
        for i in range(10):
            test_product = StandardProductTypeFactory.create(
                description="This is a test product " + i.__str__(),
                title="This is a test product " + i.__str__(),
                product_type_identifier=12334235+i,
            )
            StandardPriceFactory.create(
                product_type=test_product,
            )
            StandardSalesDocumentPositionFactory.create(
                sales_document=self.test_quote,
                position_number=i*10,
                quantity=0.333*i,
                description="This is a test position " + i.__str__(),
                discount=i*5
            )

    @pytest.mark.back_end_tests
    def test_create_task(self):
        project = CreateTaskView.create_project_from_document(self.test_user, self.test_quote)
        tasks = Task.objects.filter(project=project.id)
        task_counter = 0
        for task_current in tasks:
            self.assertEqual(
                task_current.title.__str__()[:24], "This is a test position ")
            task_counter += 1
        self.assertEqual(
            task_counter.__str__(), "10")

