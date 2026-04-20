"""koalixcrm URL Configuration.

Per CR-002 (change_requests/CR_002_API_ROUTING_VERSIONING_AND_APP_GROUPING.md),
REST resources are mounted under a per-app, versioned, workspace-scoped shape:

    /<koalixcrm_app>/api/v1/<workspace_id>/<resource>/

Each app owns its own ``urls.py`` (or ``api_urls.py`` where a legacy HTML
``urls.py`` already exists — see ``koalixcrm/reporting``) and gets its own
OpenAPI schema / Swagger / Redoc triplet.
"""

from django.urls import path, include
from django.conf.urls.static import *  # noqa: F401,F403 — keeps legacy `static`/`settings` re-exports
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.shortcuts import redirect
from filebrowser.sites import site
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from koalixcrm.auth.oidc_views import (
    LoginSelectionView, OAuthLoginView, OAuthCallbackView, MultiProviderLogoutView,
)
from koalixcrm.core.views.workspace_switch import WorkspaceSwitchView


# ---------------------------------------------------------------------------
# Per-app URL conf lists (fed to per-app SpectacularAPIView) and per-app
# Swagger settings. Mirrors the WFS pattern in
# ``qq_workflow_support_webapp_backend/urls.py``.
# ---------------------------------------------------------------------------

accounting_api_urls = [
    path('koalixcrm_accounting/api/v1/<int:workspace_id>/', include('koalixcrm.accounting.urls')),
]
accounting_swagger_settings = {
    'TITLE': 'koalixcrm Accounting API',
    'DESCRIPTION': 'API documentation for the koalixcrm Accounting service.',
    'VERSION': '1.0.0',
}

contacts_api_urls = [
    path('koalixcrm_contacts/api/v1/<int:workspace_id>/', include('koalixcrm.contacts.urls')),
]
contacts_swagger_settings = {
    'TITLE': 'koalixcrm Contacts API',
    'DESCRIPTION': 'API documentation for the koalixcrm Contacts (Party) service.',
    'VERSION': '1.0.0',
}

products_api_urls = [
    path('koalixcrm_products/api/v1/<int:workspace_id>/', include('koalixcrm.products.urls')),
]
products_swagger_settings = {
    'TITLE': 'koalixcrm Products API',
    'DESCRIPTION': 'API documentation for the koalixcrm Products service.',
    'VERSION': '1.0.0',
}

core_api_urls = [
    path('koalixcrm_core/api/v1/<int:workspace_id>/', include('koalixcrm.core.urls')),
]
core_swagger_settings = {
    'TITLE': 'koalixcrm Core API',
    'DESCRIPTION': 'API documentation for the koalixcrm Core (currency/tax/unit/pdf) service.',
    'VERSION': '1.0.0',
}

contracts_api_urls = [
    path('koalixcrm_contracts/api/v1/<int:workspace_id>/', include('koalixcrm.contracts.urls')),
]
contracts_swagger_settings = {
    'TITLE': 'koalixcrm Contracts API',
    'DESCRIPTION': 'API documentation for the koalixcrm Contracts (invoice/quotation/...) service.',
    'VERSION': '1.0.0',
}

reporting_api_urls = [
    path('koalixcrm_reporting/api/v1/<int:workspace_id>/', include('koalixcrm.reporting.api_urls')),
]
reporting_swagger_settings = {
    'TITLE': 'koalixcrm Reporting API',
    'DESCRIPTION': 'API documentation for the koalixcrm Reporting (project/task/work) service.',
    'VERSION': '1.0.0',
}


admin.autodiscover()
# Override Django admin login to redirect to OIDC
admin.site.login = LoginSelectionView.as_view()


urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),

    # --- Admin / auth / non-API (unchanged from pre-CR-002) -------------------
    # Workspace switch view — must appear BEFORE admin/ so the named URL wins.
    path('admin/core/workspace/switch/', WorkspaceSwitchView.as_view(), name='core-workspace-switch'),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('koalixcrm/crm/reporting/', include('koalixcrm.reporting.urls')),  # legacy HTML reporting
    # OIDC auth (admin login via Keycloak)
    path('auth/login/', LoginSelectionView.as_view(), name='login-selection'),
    path('auth/login/<str:provider>/', OAuthLoginView.as_view(), name='oauth-login'),
    path('auth/callback/<str:provider>/', OAuthCallbackView.as_view(), name='oauth-callback'),
    path('auth/logout/', MultiProviderLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # --- Per-app REST API, workspace-scoped -----------------------------------
    path('koalixcrm_accounting/api/v1/<int:workspace_id>/', include('koalixcrm.accounting.urls')),
    path('koalixcrm_contacts/api/v1/<int:workspace_id>/',   include('koalixcrm.contacts.urls')),
    path('koalixcrm_products/api/v1/<int:workspace_id>/',   include('koalixcrm.products.urls')),
    path('koalixcrm_core/api/v1/<int:workspace_id>/',       include('koalixcrm.core.urls')),
    path('koalixcrm_contracts/api/v1/<int:workspace_id>/',  include('koalixcrm.contracts.urls')),
    path('koalixcrm_reporting/api/v1/<int:workspace_id>/',  include('koalixcrm.reporting.api_urls')),

    # --- Per-app OpenAPI / Swagger / Redoc ------------------------------------
    path('koalixcrm_accounting/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=accounting_api_urls, custom_settings=accounting_swagger_settings,
    ), name='koalixcrm-accounting-api-schema'),
    path('koalixcrm_accounting/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-accounting-api-schema',
    ), name='koalixcrm-accounting-swagger-ui'),
    path('koalixcrm_accounting/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-accounting-api-schema',
    ), name='koalixcrm-accounting-redoc'),

    path('koalixcrm_contacts/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=contacts_api_urls, custom_settings=contacts_swagger_settings,
    ), name='koalixcrm-contacts-api-schema'),
    path('koalixcrm_contacts/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-contacts-api-schema',
    ), name='koalixcrm-contacts-swagger-ui'),
    path('koalixcrm_contacts/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-contacts-api-schema',
    ), name='koalixcrm-contacts-redoc'),

    path('koalixcrm_products/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=products_api_urls, custom_settings=products_swagger_settings,
    ), name='koalixcrm-products-api-schema'),
    path('koalixcrm_products/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-products-api-schema',
    ), name='koalixcrm-products-swagger-ui'),
    path('koalixcrm_products/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-products-api-schema',
    ), name='koalixcrm-products-redoc'),

    path('koalixcrm_core/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=core_api_urls, custom_settings=core_swagger_settings,
    ), name='koalixcrm-core-api-schema'),
    path('koalixcrm_core/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-core-api-schema',
    ), name='koalixcrm-core-swagger-ui'),
    path('koalixcrm_core/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-core-api-schema',
    ), name='koalixcrm-core-redoc'),

    path('koalixcrm_contracts/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=contracts_api_urls, custom_settings=contracts_swagger_settings,
    ), name='koalixcrm-contracts-api-schema'),
    path('koalixcrm_contracts/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-contracts-api-schema',
    ), name='koalixcrm-contracts-swagger-ui'),
    path('koalixcrm_contracts/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-contracts-api-schema',
    ), name='koalixcrm-contracts-redoc'),

    path('koalixcrm_reporting/api/schema/v1/', SpectacularAPIView.as_view(
        urlconf=reporting_api_urls, custom_settings=reporting_swagger_settings,
    ), name='koalixcrm-reporting-api-schema'),
    path('koalixcrm_reporting/api/swagger/v1/', SpectacularSwaggerView.as_view(
        url_name='koalixcrm-reporting-api-schema',
    ), name='koalixcrm-reporting-swagger-ui'),
    path('koalixcrm_reporting/api/redoc/v1/', SpectacularRedocView.as_view(
        url_name='koalixcrm-reporting-api-schema',
    ), name='koalixcrm-reporting-redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # noqa: F405
