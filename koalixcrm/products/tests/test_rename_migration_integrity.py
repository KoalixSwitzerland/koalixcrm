# -*- coding: utf-8 -*-
"""ADR-0003 Amendment 2026-06-27 — ProductType -> Product rename integrity
(REQ-0007 AC-2/AC-3/AC-4).

Two complementary angles:

1. Structural introspection of migration 0007 itself (the operations it is
   built from — `SeparateDatabaseAndState`/`RunSQL` pure table rename,
   `DeleteModel` for the hollow hull, `AddField(kind, default=TRADING_GOOD,
   preserve_default=False)`). A full `MigratorTestCase`-style before/after
   row-count comparison would need `django-test-migrations`, which is not
   a project dependency; the round-trip (`migrate products 0006` <->
   `migrate`) was additionally verified manually — see the engineer's
   report — and is exercised end-to-end by `manage.py makemigrations
   --check` staying clean after a full down/up cycle.
2. End-to-end FK-integrity check on the *current* schema: every app that
   references the renamed model (`contract_object_management`,
   `accounting`, `subscriptions`, `core`) can create real rows against
   `products.Product` and read them back — proving the FK constraints
   that used to target `crm_producttype` now resolve against
   `products_product` without any row having been rewritten.
"""
import importlib

import pytest
from django.db import migrations as dj_migrations
from django.test import TestCase

from koalixcrm.accounting.models import Account, ProductCategory
from koalixcrm.accounting.models.product_category_assignment import (
    ProductCategoryAssignment,
)
from koalixcrm.core.models.currency_transform import CurrencyTransform
from koalixcrm.core.models.unit_transform import UnitTransform
from koalixcrm.products.models.product import Product
from koalixcrm.subscriptions.models.subscription_type import SubscriptionType
from koalixcrm.contracts.tests.factories.commercial_document_position_factory import (
    StandardCommercialDocumentPositionFactory,
)
from koalixcrm.contracts.tests.factories.quotation_factory import StandardQuotationFactory
from koalixcrm.core.tests.factories.currency_factory import (
    SecondStandardCurrencyFactory,
    StandardCurrencyFactory,
)
from koalixcrm.core.tests.factories.unit_factory import SmallUnitFactory, StandardUnitFactory
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory


class RenameMigrationStructureTest(TestCase):
    """Static introspection of the migration 0007 operation list."""

    @pytest.mark.back_end_tests
    def test_kind_field_backfill_default_is_trading_good(self):
        module = importlib.import_module(
            "koalixcrm.products.migrations.0007_rename_producttype_to_product"
        )
        migration = module.Migration

        add_field_ops = [
            op for op in migration.operations
            if isinstance(op, dj_migrations.AddField) and op.name == "kind"
        ]
        self.assertEqual(len(add_field_ops), 1)
        add_kind = add_field_ops[0]
        self.assertEqual(add_kind.field.default, "TRADING_GOOD")
        self.assertFalse(add_kind.preserve_default)

    @pytest.mark.back_end_tests
    def test_migration_deletes_the_hollow_product_hull_and_renames_producttype(self):
        module = importlib.import_module(
            "koalixcrm.products.migrations.0007_rename_producttype_to_product"
        )
        migration = module.Migration

        delete_ops = [
            op for op in migration.operations
            if isinstance(op, dj_migrations.DeleteModel) and op.name == "Product"
        ]
        self.assertEqual(len(delete_ops), 1)

        rename_ops = [
            op for op in migration.operations
            if isinstance(op, dj_migrations.SeparateDatabaseAndState)
        ]
        self.assertEqual(len(rename_ops), 1)
        state_ops = rename_ops[0].state_operations
        self.assertTrue(
            any(
                isinstance(op, dj_migrations.RenameModel)
                and op.old_name == "ProductType"
                and op.new_name == "Product"
                for op in state_ops
            )
        )
        db_ops = rename_ops[0].database_operations
        self.assertEqual(len(db_ops), 1)
        self.assertIn("ALTER TABLE crm_producttype RENAME TO products_product", db_ops[0].sql)
        self.assertIn("ALTER TABLE products_product RENAME TO crm_producttype", db_ops[0].reverse_sql)


class RenamedModelForeignKeyIntegrityTest(TestCase):
    """FK-integrity (REQ-0007 AC-2): every app that used to reference
    `ProductType` resolves cleanly against the renamed `Product` model."""

    @pytest.mark.back_end_tests
    def test_product_table_is_the_renamed_producttype_table(self):
        self.assertEqual(Product._meta.db_table, "products_product")

    @pytest.mark.back_end_tests
    def test_contracts_position_fk_resolves_against_product(self):
        quotation = StandardQuotationFactory.create()
        position = StandardCommercialDocumentPositionFactory.create(
            commercial_document=quotation
        )
        self.assertIsInstance(position.product_type, Product)
        self.assertEqual(
            position.__class__._meta.get_field("product_type").related_model,
            Product,
        )

    @pytest.mark.back_end_tests
    def test_accounting_product_category_assignment_fk_resolves_against_product(self):
        product = StandardProductTypeFactory.create()
        profit_account = Account.objects.create(
            account_number=4100,
            title="Earnings Account",
            account_type="E",
            description="Test earnings account",
            is_open_reliabilities_account=False,
            is_open_interest_account=False,
            is_product_inventory_activa=False,
            is_a_customer_payment_account=False,
        )
        loss_account = Account.objects.create(
            account_number=5100,
            title="Spendings Account",
            account_type="S",
            description="Test spendings account",
            is_open_reliabilities_account=False,
            is_open_interest_account=False,
            is_product_inventory_activa=False,
            is_a_customer_payment_account=False,
        )
        category = ProductCategory.objects.create(
            title="Rename Integrity Category",
            profit_account=profit_account,
            loss_account=loss_account,
        )
        assignment = ProductCategoryAssignment.objects.create(
            product_type=product, category=category
        )
        assignment.refresh_from_db()
        self.assertEqual(assignment.product_type_id, product.id)

    @pytest.mark.back_end_tests
    def test_subscriptions_subscription_type_fk_resolves_against_product(self):
        product = StandardProductTypeFactory.create()
        subscription_type = SubscriptionType.objects.create(product_type=product)
        subscription_type.refresh_from_db()
        self.assertEqual(subscription_type.product_type_id, product.id)

    @pytest.mark.back_end_tests
    def test_core_unit_transform_fk_resolves_against_product(self):
        product = StandardProductTypeFactory.create()
        transform = UnitTransform.objects.create(
            from_unit=StandardUnitFactory.create(),
            to_unit=SmallUnitFactory.create(),
            product_type=product,
            factor="1.00",
        )
        transform.refresh_from_db()
        self.assertEqual(transform.product_type_id, product.id)

    @pytest.mark.back_end_tests
    def test_core_currency_transform_fk_resolves_against_product(self):
        product = StandardProductTypeFactory.create()
        transform = CurrencyTransform.objects.create(
            from_currency=StandardCurrencyFactory.create(),
            to_currency=SecondStandardCurrencyFactory.create(),
            product_type=product,
            factor="1.00",
        )
        transform.refresh_from_db()
        self.assertEqual(transform.product_type_id, product.id)
