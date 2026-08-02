# -*- coding: utf-8 -*-
"""Guards the Grappelli index dashboard against silently empty panels.

`modules.ModelList` resolves its `models` patterns against the admin registry
and simply renders nothing when a pattern matches no registered model. There
is no error and no warning — the panel just disappears from the dashboard.

That is not hypothetical: the `Products` panel pointed at
`koalixcrm.products.models.product_type.ProductType` long after ADR-0003's
2026-06-27 amendment renamed the model to `Product` and moved it to
`models/product.py`. The dashboard kept rendering an empty `Products` section,
and nothing in the test suite noticed.

These tests fail if any dashboard panel resolves to zero models, so a model
rename or an un-registered ModelAdmin cannot quietly empty a panel again.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from grappelli.dashboard import modules

from projectsettings.dashboard import CustomIndexDashboard

pytestmark = pytest.mark.django_db


def _iter_model_lists(children):
    """Yield every ModelList in the tree, descending into Group children."""
    for child in children:
        if isinstance(child, modules.ModelList):
            yield child
        elif isinstance(child, modules.Group):
            yield from _iter_model_lists(child.children)


@pytest.fixture
def dashboard_context(db):
    superuser, _ = User.objects.get_or_create(
        username='dashboard-admin',
        defaults={
            'email': 'dashboard-admin@example.com',
            'is_staff': True,
            'is_superuser': True,
        },
    )
    request = RequestFactory().get('/admin/')
    request.user = superuser
    return {'request': request}


@pytest.fixture
def model_lists(dashboard_context):
    dashboard = CustomIndexDashboard()
    dashboard.init_with_context(dashboard_context)
    return list(_iter_model_lists(dashboard.children))


@pytest.mark.back_end_tests
def test_dashboard_declares_model_lists(model_lists):
    # A guard against the guard: if the traversal silently found nothing, the
    # emptiness check below would pass vacuously.
    assert len(model_lists) > 5


@pytest.mark.back_end_tests
def test_no_dashboard_panel_resolves_to_zero_models(model_lists, dashboard_context):
    empty = []
    for model_list in model_lists:
        model_list.init_with_context(dashboard_context)
        if not model_list.children:
            empty.append((str(model_list.title), model_list.models))

    assert not empty, (
        "Dashboard panels resolved to no models — a rename or an unregistered "
        f"ModelAdmin has emptied them: {empty}"
    )


@pytest.mark.back_end_tests
def test_products_panel_includes_the_renamed_product_model(model_lists, dashboard_context):
    """The specific regression: ADR-0003's ProductType -> Product rename."""
    products = next(m for m in model_lists if str(m.title) == 'Products')
    products.init_with_context(dashboard_context)
    # Titles come from each model's `verbose_name_plural` via `capfirst`, and
    # these models declare theirs already title-cased.
    titles = {child['title'] for child in products.children}
    assert {'Products', 'Product Variants', 'Product Families'} <= titles
