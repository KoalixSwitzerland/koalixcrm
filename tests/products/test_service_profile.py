# -*- coding: utf-8 -*-
"""ADR-0007, REQ-0016, ADR-0019: `ServiceProfile` — 1:1 with `Product`,
gated to `kind = SERVICE` via `ProductKindPolicy`."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from koalixcrm.products.models.choices import ProductKind, ServiceBillingModel
from koalixcrm.products.models.service_profile import ServiceProfile
from tests.factories.products.product_type_factory import StandardProductTypeFactory
from tests.factories.products.service_profile_factory import (
    StandardServiceProfileFactory,
)


class ServiceProfileGatingTest(TestCase):
    @pytest.mark.back_end_tests
    def test_service_profile_allowed_for_service(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.SERVICE)
        profile = StandardServiceProfileFactory.create(product=product)
        profile.full_clean()  # no raise

    @pytest.mark.back_end_tests
    def test_service_profile_rejected_for_trading_good(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.TRADING_GOOD)
        profile = StandardServiceProfileFactory.build(product=product, workspace=product.workspace)
        with self.assertRaises(ValidationError):
            profile.clean()

    @pytest.mark.back_end_tests
    def test_billing_model_enum_values(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.SERVICE)
        for value in (
            ServiceBillingModel.FIXED,
            ServiceBillingModel.HOURLY,
            ServiceBillingModel.SUBSCRIPTION,
            ServiceBillingModel.TIERED,
        ):
            profile = StandardServiceProfileFactory.build(
                product=product, billing_model=value, workspace=product.workspace
            )
            profile.full_clean()  # no raise

    @pytest.mark.back_end_tests
    def test_product_has_at_most_one_service_profile(self):
        product = StandardProductTypeFactory.create(kind=ProductKind.SERVICE)
        StandardServiceProfileFactory.create(product=product)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ServiceProfile.objects.create(
                    workspace=product.workspace,
                    product=product,
                    billing_model=ServiceBillingModel.FIXED,
                    deliverable="second profile",
                )
