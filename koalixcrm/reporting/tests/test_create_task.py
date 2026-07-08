# -*- coding: utf-8 -*-

import pytest
from django.test import TestCase

from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.views.create_task import CreateTaskView
from koalixcrm.contacts.tests.factories.user_factory import StaffUserFactory
from koalixcrm.contracts.tests.factories.commercial_document_position_factory import (
    StandardCommercialDocumentPositionFactory,
)
from koalixcrm.contracts.tests.factories.quotation_factory import StandardQuotationFactory
from koalixcrm.core.tests.factories.currency_factory import StandardCurrencyFactory
from koalixcrm.products.tests.factories.product_price_factory import StandardPriceFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class DocumentCalculationsTest(TestCase):
    def setUp(self):
        self.test_currency = StandardCurrencyFactory.create()
        self.test_quotation = StandardQuotationFactory.create()
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
            StandardCommercialDocumentPositionFactory.create(
                commercial_document=self.test_quotation,
                position_number=i*10,
                quantity=0.333*i,
                description="This is a test position " + i.__str__(),
                discount=i*5
            )

    @pytest.mark.back_end_tests
    def test_create_task(self):
        project = CreateTaskView.create_project_from_document(self.test_user, self.test_quotation)
        tasks = Task.objects.filter(project=project.id)
        task_counter = 0
        for task_current in tasks:
            self.assertEqual(
                task_current.title.__str__()[:24], "This is a test position ")
            task_counter += 1
        self.assertEqual(
            task_counter.__str__(), "10")

