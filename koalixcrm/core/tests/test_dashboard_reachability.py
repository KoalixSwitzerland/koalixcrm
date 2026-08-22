# -*- coding: utf-8 -*-
"""Every registered ModelAdmin must be reachable from the Grappelli dashboard.

KoalixCRM replaces the stock admin index with a hand-written
``GRAPPELLI_INDEX_DASHBOARD``, which lists models by explicit dotted-path
pattern. Registering a ModelAdmin therefore does *not* make it reachable — if
nobody adds a pattern, the changelist exists but nothing links to it and the
model is invisible to an administrator.

That has now happened three times (``PDFExportProcess``, ``RoleInWorkspace``,
and the two koalixcrm#430/#432 models), each found only by someone going
looking. This test turns the class of defect into a failing build: add a
ModelAdmin without a dashboard entry and it fails, naming the model.

Deliberate omissions go in ``INTENTIONALLY_UNLISTED`` with a reason, so
"unreachable" is always a recorded decision rather than an oversight.
"""
import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory

User = get_user_model()

#: Registered but deliberately absent from the dashboard, with the reason.
INTENTIONALLY_UNLISTED = {
    # Reached as an inline on Invoice/Quotation and aggregated read-only on
    # Contract; a top-level entry would invite editing S3 keys by hand.
    'koalixcrm.contracts.models.commercial_document_media.CommercialDocumentS3Media',
    # Pre-existing gaps, unrelated to the access-control surface. Listed here
    # so this test passes today; removing an entry is how you adopt one.
    'koalixcrm.reporting.models.work.Work',
    'koalixcrm.subscriptions.models.subscription.Subscription',
    'koalixcrm.subscriptions.models.subscription_type.SubscriptionType',
}


def _dashboard_visible_model_paths(request):
    """The dotted paths the dashboard actually renders for ``request``.

    Uses Grappelli's own ``filter_models`` rather than re-implementing the
    pattern match, so the test cannot drift from the renderer.
    """
    from grappelli.dashboard.utils import filter_models

    from projectsettings.dashboard import CustomIndexDashboard

    dashboard = CustomIndexDashboard()
    dashboard.init_with_context({'request': request})

    visible = set()

    def walk(node):
        for child in getattr(node, 'children', []) or []:
            if isinstance(child, (str, dict)):
                continue
            patterns = list(getattr(child, 'models', []) or [])
            excludes = list(getattr(child, 'exclude', []) or [])
            if patterns or excludes:
                for model, _perms in filter_models(request, patterns, excludes):
                    visible.add(f'{model.__module__}.{model.__name__}')
            walk(child)

    walk(dashboard)
    return visible


@pytest.fixture
def superuser_request(db):
    request = RequestFactory().get('/admin/')
    request.user = User.objects.create_superuser(
        username='dash-admin', email='dash-admin@example.test', password='pw'
    )
    return request


@pytest.mark.django_db
def test_every_registered_model_admin_is_reachable(superuser_request):
    visible = _dashboard_visible_model_paths(superuser_request)
    registered = {f'{m.__module__}.{m.__name__}' for m in admin.site._registry}

    unreachable = registered - visible - INTENTIONALLY_UNLISTED
    assert not unreachable, (
        'These ModelAdmins are registered but listed nowhere in '
        'projectsettings/dashboard.py, so an administrator cannot navigate to '
        'them: ' + ', '.join(sorted(unreachable)) + '. Add a dashboard entry, '
        'or add the path to INTENTIONALLY_UNLISTED with a reason.'
    )


@pytest.mark.django_db
def test_intentionally_unlisted_entries_are_all_still_registered(superuser_request):
    """Keeps the allowlist from outliving the models it excuses."""
    registered = {f'{m.__module__}.{m.__name__}' for m in admin.site._registry}
    stale = INTENTIONALLY_UNLISTED - registered
    assert not stale, f'INTENTIONALLY_UNLISTED names models that are no longer registered: {sorted(stale)}'


@pytest.mark.django_db
def test_access_control_surface_is_administrable(superuser_request):
    """The koalixcrm#430/#432 workflow must be completable in the admin.

    Registering an issuer, granting the service account, and binding a
    claim-derived group to a workspace role are the three steps the fix
    depends on. All three need a reachable admin.
    """
    visible = _dashboard_visible_model_paths(superuser_request)
    for path in (
        'koalixcrm.core.models.oidc_tenant.OidcTenant',
        'koalixcrm.core.models.service_account_grant.ServiceAccountGrant',
        'koalixcrm.core.models.access.RoleInWorkspace',
        'koalixcrm.core.models.workspace.Workspace',
        'django.contrib.auth.models.Group',
        'django.contrib.auth.models.User',
    ):
        assert path in visible, f'{path} is not reachable from the dashboard'


@pytest.mark.django_db
def test_superuser_only_models_are_hidden_from_staff(db):
    """The #430/#432 admins must not render as dead links for staff users.

    Grappelli drops a model whose ``get_model_perms`` are all False, so the
    superuser-only hooks on these two admins hide the entries rather than
    showing a link that 403s.
    """
    request = RequestFactory().get('/admin/')
    request.user = User.objects.create_user(
        username='staffer', email='staffer@example.test', password='pw', is_staff=True
    )
    visible = _dashboard_visible_model_paths(request)
    assert 'koalixcrm.core.models.oidc_tenant.OidcTenant' not in visible
    assert 'koalixcrm.core.models.service_account_grant.ServiceAccountGrant' not in visible
