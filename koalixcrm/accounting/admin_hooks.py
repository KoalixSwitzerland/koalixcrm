# -*- coding: utf-8 -*-
"""Attach accounting-owned inlines to `core.Tax` and `products.ProductType`
admins at startup, so users with the accounting app installed see the
activa/passiva accounts and product category directly on the Tax /
ProductType change pages (the pre-CR-2c UX).

Runs from `AccountingConfig.ready()`. When the accounting app is not
installed this module never loads, so the admins stay clean.
"""
from django.apps import apps
from django.contrib import admin


def _patch_tax_admin():
    from koalixcrm.accounting.admin.tax_account_assignment_admin import (
        TaxAccountAssignmentInline,
    )
    from koalixcrm.core.models.tax import Tax
    try:
        existing = admin.site._registry[Tax]
    except KeyError:
        return
    existing_cls = type(existing)
    if TaxAccountAssignmentInline in getattr(existing_cls, 'inlines', ()):
        return
    existing_cls.inlines = tuple(getattr(existing_cls, 'inlines', ())) + (
        TaxAccountAssignmentInline,
    )


def _patch_product_type_admin():
    if not apps.is_installed('koalixcrm.products'):
        return
    from koalixcrm.accounting.admin.product_category_assignment_admin import (
        ProductCategoryAssignmentInline,
    )
    from koalixcrm.products.models.product_type import ProductType
    try:
        existing = admin.site._registry[ProductType]
    except KeyError:
        return
    existing_cls = type(existing)
    if ProductCategoryAssignmentInline in getattr(existing_cls, 'inlines', ()):
        return
    existing_cls.inlines = tuple(getattr(existing_cls, 'inlines', ())) + (
        ProductCategoryAssignmentInline,
    )


_patch_tax_admin()
_patch_product_type_admin()
