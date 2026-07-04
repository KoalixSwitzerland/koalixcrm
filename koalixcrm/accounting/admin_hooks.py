# -*- coding: utf-8 -*-
"""Attach accounting-owned inlines to `core.Tax` and `products.Product`
admins at startup, so users with the accounting app installed see the
activa/passiva accounts and product category directly on the Tax /
Product change pages (the pre-CR-2c UX).

Runs from `AccountingConfig.ready()`. When the accounting app is not
installed this module never loads, so the admins stay clean.
"""

from __future__ import annotations

from django.apps import apps
from django.contrib import admin


def _patch_tax_admin() -> None:
    from koalixcrm.accounting.admin.tax_account_assignment_admin import (
        TaxAccountAssignmentInline,
    )
    from koalixcrm.core.models.tax import Tax

    try:
        existing = admin.site._registry[Tax]
    except KeyError:
        return
    existing_cls = type(existing)
    if TaxAccountAssignmentInline in getattr(existing_cls, "inlines", ()):
        return
    existing_cls.inlines = tuple(getattr(existing_cls, "inlines", ())) + (TaxAccountAssignmentInline,)


def _patch_product_type_admin() -> None:
    if not apps.is_installed("koalixcrm.products"):
        return
    from koalixcrm.accounting.admin.product_category_assignment_admin import (
        ProductCategoryAssignmentInline,
    )
    from koalixcrm.products.models.product import Product

    try:
        existing = admin.site._registry[Product]
    except KeyError:
        return
    existing_cls = type(existing)
    if ProductCategoryAssignmentInline in getattr(existing_cls, "inlines", ()):
        return
    existing_cls.inlines = tuple(getattr(existing_cls, "inlines", ())) + (ProductCategoryAssignmentInline,)


_patch_tax_admin()
_patch_product_type_admin()
