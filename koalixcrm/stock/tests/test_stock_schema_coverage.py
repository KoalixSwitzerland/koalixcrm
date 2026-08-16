# -*- coding: utf-8 -*-
"""Guards the published stock OpenAPI schema against silent endpoint loss.

`ScanResolveView` and `SerialUnitAvailabilityView` are plain `APIView`s, so
drf-spectacular cannot infer a serializer for them. Without an explicit
`@extend_schema` it logs an "unable to guess serializer" error and *drops the
view from the schema* — the endpoints keep working while quietly vanishing
from the published contract. These tests fail if that regresses.
"""
import pytest
from django.test import TestCase
from drf_spectacular.generators import SchemaGenerator

from projectsettings.urls import stock_api_urls

SCAN_RESOLVE_PATH = '/koalixcrm_stock/api/v1/{workspace_id}/scan/resolve/'
AVAILABILITY_PATH = (
    '/koalixcrm_stock/api/v1/{workspace_id}/variants/{variant_id}/serial-units/availability/'
)


class StockSchemaCoverageTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.schema = SchemaGenerator(patterns=stock_api_urls).get_schema(request=None, public=True)

    @pytest.mark.back_end_tests
    def test_scan_resolve_is_published(self):
        operation = self.schema['paths'][SCAN_RESOLVE_PATH]['post']
        self.assertIn('200', operation['responses'])
        self.assertIn('409', operation['responses'])
        self.assertTrue(operation.get('requestBody'))

    @pytest.mark.back_end_tests
    def test_serial_unit_availability_is_published(self):
        operation = self.schema['paths'][AVAILABILITY_PATH]['get']
        self.assertIn('200', operation['responses'])
        query_params = {
            parameter['name']
            for parameter in operation.get('parameters', [])
            if parameter.get('in') == 'query'
        }
        self.assertEqual({'start', 'end'}, query_params)

    @pytest.mark.back_end_tests
    def test_availability_response_documents_free_windows(self):
        operation = self.schema['paths'][AVAILABILITY_PATH]['get']
        schema_ref = operation['responses']['200']['content']['application/json']['schema']
        component = schema_ref['items']['$ref'].rsplit('/', 1)[-1]
        properties = self.schema['components']['schemas'][component]['properties']
        self.assertEqual(
            {'serial_unit', 'serial_number', 'free', 'free_windows'},
            set(properties),
        )
