# CR-002 (koalixcrm) — Adopt per-app, versioned, workspace-scoped REST API routing

**Requested by:** quantalq.com — koalixcrm ⇄ `qq_workflow_support_webapp_backend` (WFS) integration.
**Companion documents:**
- WFS side (reference pattern): `qq_workflow_support_webapp_backend/urls.py`, `qq_workflow_support_webapp_backend/qq_workflow_support/urls.py`, `qq_workflow_support_webapp_backend/qq_human_resources_support/urls.py`.
- koalixcrm CR-001 (companion, workspace alignment): `qq_workflow_support_webapp_backend/change_requests/CR_001_KOALIXCRM_WORKSPACE_ALIGNMENT.md`.
**Target branch:** `feature/api-routing-versioning-and-grouping` (off `develop`).
**Status:** Proposed.

---

## 0. TL;DR

Today, every koalixcrm REST resource is registered on a **single flat, unversioned `DefaultRouter` at the project root** in `projectsettings/urls.py` — e.g. `/accounts/`, `/parties/`, `/invoices/`, `/tasks/`, … live side-by-side with no app grouping and no version segment.

WFS has moved to a **per-app, versioned, workspace-scoped** pattern:

```
/<app_name>/api/v<n>/<workspace_id>/<resource>/
```

and each app owns its own `urls.py` + its own OpenAPI schema/swagger/redoc pair.

Since koalixcrm's API is **not yet consumed by any external client** (confirmed by the requester — "they are using a different API pattern which is not yet used on their side"), we have a free window to change it. This CR describes the full migration so that koalixcrm and WFS become **portable** under the same routing contract, which is a precondition for mounting koalixcrm apps into the WFS project (and vice versa) without URL collisions, duplicate schemas, or version ambiguity.

This CR is **routing / URL conf / schema generation only**. It does not change ViewSets, serializers, models, permissions, or business logic. Workspace scoping of the data itself is tracked separately (koalixcrm CR-9 / WFS CR-001).

---

## 1. Why this change

### 1.1 The flat router does not scale to a merged WFS + koalixcrm deployment

Both projects define a `projects` resource. Both define `tasks`. WFS has `persons`, `companies`, `phone-numbers`, `email-addresses`; koalixcrm has `parties`, `organizations`, `phone_numbers`, `party_emails`. Some overlap semantically, some do not. At the URL level, `/tasks/` is ambiguous as soon as both projects run in the same Django process or are composed as a platform.

WFS's answer is app-prefixed namespaces — `/qq_workflow_support/api/v1/<ws>/tasks/` and `/qq_human_resources_support/api/v1/<ws>/...` never collide, each app renders its own Swagger, and a reader of the URL always knows which app and which version they are talking to. koalixcrm must adopt the same discipline.

### 1.2 No versioning = no safe evolution

The current koalixcrm URL `/invoices/` has no version segment. Any breaking change to the invoice serializer is a wire break with no coexistence path. WFS's `/qq_workflow_support/api/v1/...` explicitly leaves room for `v2` side-by-side; koalixcrm needs the same.

### 1.3 Per-app schemas unlock per-app docs

WFS uses `drf-spectacular`'s `SpectacularAPIView(urlconf=..., custom_settings=...)` trick to emit **one OpenAPI document per app**, each at a predictable path (`/<app>/api/schema/v1/`, `/<app>/api/swagger/v1/`, `/<app>/api/redoc/v1/`). Each app's Swagger / Redoc UI then renders only that app's endpoints.

koalixcrm has a parallel `*_api_py` client structure (`accounting_api_py`, `contacts_api_py`, `contracts_api_py`, `core_api_py`, `products_api_py`, `reporting_api_py`). These are **hand-written Python clients**, not generated from a schema — no codegen tooling exists in the repo. Per-app schemas are still valuable for humans reading the docs and for any future codegen effort, but this CR does not introduce codegen; the client files are updated by hand as part of CR-R4.

### 1.4 Workspace-scoping the URL (not just the queryset) makes intent explicit

WFS puts `<int:workspace_id>` in the URL path. This makes multi-tenancy visible at the router level, removes any chance of a ViewSet forgetting to filter by workspace, and makes it trivial for a reverse proxy / BFF to route, rate-limit or authorize per workspace. koalixcrm's workspace rollout (CR-9 over there) is landing the data-level scoping; this CR lands the URL-level scoping that mirrors it.

---

## 2. Current koalixcrm state

**File of record:** `projectsettings/urls.py` (lines 9–139).

Shape:

```python
router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'accounting_periods', AccountingPeriodViewSet)
# ... ~55 resources from 6 apps, all flat ...
router.register(r'generic_task_links', GenericTaskLinkViewSet)

urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),
    path('', include(router.urls)),              # ← everything mounted at root
    path('admin/core/workspace/switch/', WorkspaceSwitchView.as_view(), ...),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('koalixcrm/crm/reporting/', include('koalixcrm.reporting.urls')),  # only non-API prefix
    path('auth/login/', ...),
    path('auth/callback/<str:provider>/', ...),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
```

Observations:

- **No `api/` prefix** on any REST resource. `/accounts/` lives on the root, immediately next to `/admin/` and `/auth/`.
- **No version segment** anywhere.
- **No app grouping** in the URL. The only clue to which app a resource belongs to is the comment `# Accounting` / `# CRM (contacts)` in the urls.py itself.
- **No per-app `urls.py`** for the API. `koalixcrm/reporting/urls.py` exists but it is the legacy server-rendered reporting views, not the REST API.
- **A single implicit DRF schema** (whatever the current drf-spectacular settings produce) covers every ViewSet. There is no `SpectacularAPIView` / `SpectacularSwaggerView` in `projectsettings/urls.py` today — so schema / swagger / redoc routes are either unregistered or pulled in globally from settings.

### 2.1 Apps in scope

From the imports in `projectsettings/urls.py` plus the on-disk `*_api_py` packages:

| App (Django label) | API package | Resources registered today | Proposed URL prefix |
|---|---|---|---|
| `accounting` | `koalixcrm.accounting_api_py` | `accounts`, `accounting_periods`, `bookings`, `product_categories` | `/koalixcrm_accounting/` |
| `contacts` | `koalixcrm.contacts_api_py` | `parties`, `organizations`, `party_contacts`, `party_identifications`, `party_roles`, `organization_memberships`, `organization_relationships`, `addresses`, `address_assignments`, `phone_numbers`, `phone_assignments`, `party_emails`, `email_assignments`, `party_groups`, `party_group_memberships`, `customer_billing_cycles` | `/koalixcrm_contacts/` |
| `products` | `koalixcrm.products_api_py` | `products` (= `ProductTypeViewSet`), `product_items`, `product_prices`, `customer_group_transforms` | `/koalixcrm_products/` |
| `core` | `koalixcrm.core_api_py` (+ `djangoUserExtension`, pieces of `contracts`) | `currencies`, `taxes`, `units`, `currency_transforms`, `unit_transforms`, `pdf_export_processes`, `document_templates`, `commercial_document_media` | `/koalixcrm_core/` |
| `contracts` | `koalixcrm.contracts_api_py` | `contracts`, `invoices`, `quotations`, `purchase_orders`, `sales_orders`, `despatch_advices`, `payment_reminders`, `commercial_document_positions`, `credit_notes` | `/koalixcrm_contracts/` |
| `reporting` | `koalixcrm.reporting_api_py` | `projects`, `project_status`, `tasks`, `task_status`, `agreements`, `works`, `estimations`, `estimation_status`, `human_resources`, `resources`, `resource_types`, `resource_managers`, `resource_prices`, `reporting_periods`, `reporting_period_status`, `agreement_status`, `agreement_types`, `project_link_types`, `task_link_types`, `generic_project_links`, `generic_task_links` | `/koalixcrm_reporting/` |

> **Note on `commercial_document_media`**: it is imported from `koalixcrm.contracts.views.commercial_document_media_view_set` today, not from `contracts_api_py`. Decide during implementation whether to move the ViewSet into `contracts_api_py` (preferred, for parity) or keep it under `core` because its storage/PDF concerns are cross-cutting. **Default recommendation: move to `contracts_api_py`.**

---

## 3. Target state

### 3.1 URL shape (normative)

```
/<koalixcrm_app>/api/v1/<int:workspace_id>/<resource>/
/<koalixcrm_app>/api/v1/<int:workspace_id>/<resource>/<int:pk>/
/<koalixcrm_app>/api/v1/_batch/<operation>/                          # workspace-independent
/<koalixcrm_app>/api/schema/v1/
/<koalixcrm_app>/api/swagger/v1/
/<koalixcrm_app>/api/redoc/v1/
```

Rules:

1. **`<koalixcrm_app>`** is always `koalixcrm_<appname>` (e.g. `koalixcrm_accounting`). The `koalixcrm_` prefix is mandatory — it is the anti-collision segment for the day koalixcrm apps are mounted alongside WFS apps in a single project. WFS apps keep their `qq_*` prefix; koalixcrm gets `koalixcrm_*`.
2. **`/api/v1/`** is mandatory. No root-mounted resources. No unversioned resources.
3. **`<workspace_id>`** is a required path parameter for every workspace-scoped resource. Workspace-independent endpoints (global enumerations, batch jobs) use `_batch/` under the same app prefix and **omit** the workspace segment — this mirrors WFS's `qq_human_resources_support/api/v1/_batch/...` convention.
4. **Each app owns its own `urls.py`** at `koalixcrm/<app>/urls.py`, exporting a `router` registered with *only that app's* ViewSets and exposing `urlpatterns = router.urls` (plus any non-router views for that app).
5. **Each app gets its own OpenAPI triplet** (`schema`, `swagger`, `redoc`) driven by a per-app `urlconf` list and per-app `custom_settings`, following the WFS pattern in `qq_workflow_support_webapp_backend/urls.py:82-115`.

### 3.2 Resource naming normalisation (sub-decision inside this CR)

WFS uses **kebab-case** for URL segments (`workflow-tags`, `phone-numbers`, `email-addresses`, `workspace-configs`). koalixcrm currently uses **snake_case** (`accounting_periods`, `product_categories`, `phone_numbers`, `party_emails`).

**Decision required — pick one and apply consistently across koalixcrm:**

- **(A) Adopt kebab-case everywhere** — matches WFS, matches common REST convention, but is a breaking change for every koalixcrm resource. Acceptable because no external consumer exists yet.
- **(B) Keep snake_case in koalixcrm, kebab-case in WFS** — documents the heritage honestly, no churn on koalixcrm clients, but means the two halves of the combined platform will not feel like one API.

**Recommendation: (A) kebab-case.** Portability is the whole point of this CR; leaving them split defeats it. The generated `*_api_py` client classes do not care about the URL casing — only `basename` does, and that is decoupled from the URL.

**Decision: (A) kebab-case is adopted.** The impact on the Django apps is small and well-bounded — see §3.2.1.

#### 3.2.1 Impact of the snake_case → kebab-case switch on the Django apps

The change is **purely a URL-segment rename**. Nothing that Django considers structural is affected:

| Surface | Affected? | Notes |
|---|---|---|
| Django `app_label`, app `name`, app config | **No** | App labels stay `accounting`, `contacts`, `products`, `core`, `contracts`, `reporting`. |
| Models (`class Meta: db_table`, model names, FKs) | **No** | Zero migrations triggered by this change. |
| Serializers, ViewSets, permissions, signals | **No** | Python identifiers are untouched. Only the string passed to `router.register(r'...')` changes. |
| `basename` on router registrations | **Keep kebab-case** | Already kebab-case in the §3.4 template (`basename='accounting-period'`). View-name lookups like `reverse('accounting-period-list')` follow this, not the URL segment. |
| `reverse()` / `reverse_lazy()` call sites | **Minimal** | A full-repo scan finds only **5 `reverse()` calls across 3 files** (`core/views/workspace_switch.py`, `auth/oidc_views.py`, `core/admin/dashboard_modules.py`), **none of which resolve to API router URLs**. No rewrites needed for kebab-case specifically; the ones that do need updating are the ones already in CR-R4 (app/version prefix changes), not URL-segment casing. |
| DRF hyperlinked serializers (`HyperlinkedModelSerializer`, `HyperlinkedIdentityField`, `HyperlinkedRelatedField`) | **None in repo** | A full-repo grep finds **zero usages**. koalixcrm uses `PrimaryKeyRelatedField` / id-based serialization throughout, so response payloads do not embed URL segments. Kebab-case does not ripple into wire responses. |
| Django admin | **No** | Admin URLs are generated from model/app labels, not from the DRF router. Untouched. |
| OpenAPI `operationId` and generated client method names | **Yes — cosmetic** | `drf-spectacular` derives `operationId` from the URL path. `accounting_periods_list` becomes `accounting-periods_list` (or the generator's kebab-to-camel transform produces `accountingPeriodsList` — same as `accounting_periods_list` produces today, depending on the generator). The `*_api_py/*_api_client.py` files regenerate cleanly in CR-R3; they are not hand-maintained. |
| Tests hitting hard-coded URL strings | **Yes, mechanical** | Already covered by CR-R4. The casing flip is one extra find-and-replace on top of the prefix/version changes — same PR, same pass. |
| External consumers | **None** | The premise of this CR. Nothing outside the repo to break. |

**Conclusion.** The kebab-case switch adds no migrations, no model churn, no serializer churn, no admin changes, and no new `reverse()` breakage beyond what CR-R2 already forces. The only real work is the client regeneration (already planned as CR-R3) and the test sweep (already planned as CR-R4). Going with (A) is effectively free on top of this CR's existing cost.

### 3.3 `projectsettings/urls.py` after the change

```python
"""koalixcrm URL Configuration"""
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static as staticfiles_static  # noqa
from django.contrib import admin
from django.shortcuts import redirect
from filebrowser.sites import site
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView,
)
from koalixcrm.auth.oidc_views import (
    LoginSelectionView, OAuthLoginView, OAuthCallbackView, MultiProviderLogoutView,
)
from koalixcrm.core.views.workspace_switch import WorkspaceSwitchView

# -------- Per-app URL conf lists (fed to per-app SpectacularAPIView) --------

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
admin.site.login = LoginSelectionView.as_view()

urlpatterns = [
    path('', lambda _: redirect('admin:index'), name='index'),

    # --- Admin / auth / non-API (unchanged) -----------------------------------
    path('admin/core/workspace/switch/', WorkspaceSwitchView.as_view(), name='core-workspace-switch'),
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('koalixcrm/crm/reporting/', include('koalixcrm.reporting.urls')),   # legacy HTML reporting
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
    path('koalixcrm_accounting/api/swagger/v1/', SpectacularSwaggerView.as_view(url_name='koalixcrm-accounting-api-schema'),
         name='koalixcrm-accounting-swagger-ui'),
    path('koalixcrm_accounting/api/redoc/v1/', SpectacularRedocView.as_view(url_name='koalixcrm-accounting-api-schema'),
         name='koalixcrm-accounting-redoc'),

    # ... repeat the schema/swagger/redoc triplet for contacts, products, core,
    #     contracts, reporting. Copy-paste is acceptable here — WFS does the
    #     same (`qq_workflow_support_webapp_backend/urls.py:82-115`).
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 3.4 Per-app `urls.py` template

Each app gets a new file (or a new `api_urls.py` where a legacy `urls.py` already exists, see §3.5):

```python
# koalixcrm/accounting/urls.py
from rest_framework.routers import DefaultRouter
from koalixcrm.accounting_api_py.accounting_api import (
    AccountViewSet, AccountingPeriodViewSet, BookingViewSet, ProductCategoryViewSet,
)

router = DefaultRouter()
router.register(r'accounts',             AccountViewSet,          basename='account')
router.register(r'accounting-periods',   AccountingPeriodViewSet, basename='accounting-period')
router.register(r'bookings',             BookingViewSet,          basename='booking')
router.register(r'product-categories',   ProductCategoryViewSet,  basename='product-category')

urlpatterns = router.urls
```

Every app follows the same template. This mirrors `qq_workflow_support_webapp_backend/qq_workflow_support/urls.py` and `qq_human_resources_support/urls.py`.

### 3.5 Collision with legacy `koalixcrm/reporting/urls.py`

`koalixcrm/reporting/urls.py` already exists and serves the **legacy server-rendered reporting views** (it is included at `koalixcrm/crm/reporting/` in the current root `urlpatterns`). Do **not** overload that file. Create a sibling `koalixcrm/reporting/api_urls.py` for the REST router and reference it from `projectsettings/urls.py`. The six-app table in §2.1 is already written with this in mind.

### 3.6 `basename` is mandatory

The current flat router omits `basename` on most `router.register(...)` calls. Under the new per-app structure, with workspace-scoped URLs and per-app schemas, **every registration must pass an explicit `basename`**. DRF's inference from `queryset.model` breaks in some of the `*_api_py` ViewSets (those that override `get_queryset`) and is brittle in any case. WFS already enforces this — see `qq_workflow_support/urls.py:17-60`.

### 3.7 ViewSet changes required

The ViewSets themselves need one **non-trivial** adjustment: they must read `workspace_id` from `self.kwargs['workspace_id']` and filter their querysets accordingly. This is the ViewSet-level mirror of CR-9 (koalixcrm-side workspace scoping). **This CR explicitly does not specify the ViewSet changes** — it depends on CR-9 landing first or in parallel. If CR-9 has already chosen a mixin (e.g. `WorkspaceScopedViewSetMixin`), point each ViewSet at it and you are done.

For the interim (CR-9 not yet merged), the ViewSets can **accept and ignore** `workspace_id` without filtering — the URL parameter is still captured, it just has no behavioural effect. This lets CR-002 land independently.

---

## 4. Change items

### CR-R1 — Create per-app `urls.py` / `api_urls.py`

Create six files following the §3.4 template:

- `koalixcrm/accounting/urls.py`
- `koalixcrm/contacts/urls.py`
- `koalixcrm/products/urls.py`
- `koalixcrm/core/urls.py`
- `koalixcrm/contracts/urls.py`
- `koalixcrm/reporting/api_urls.py` (**not** `urls.py` — see §3.5)

Each file:
- Imports ViewSets only from its own app's `*_api_py` package.
- Registers every ViewSet with an explicit `basename`.
- Uses **kebab-case** URL segments (§3.2 decision A).

**Risk:** low. Pure addition; nothing in production yet references these paths.

### CR-R2 — Rewrite `projectsettings/urls.py`

Replace the flat router + root `include(router.urls)` with the shape shown in §3.3:

- Remove the project-level `router = routers.DefaultRouter()` and all 55 `router.register(...)` calls.
- Remove the top-level imports of every ViewSet — they now live only in their app's `urls.py`.
- Add the six `path('koalixcrm_<app>/api/v1/<int:workspace_id>/', include(...))` lines.
- Add the six `SpectacularAPIView` / `SpectacularSwaggerView` / `SpectacularRedocView` triplets.
- Keep the admin, auth, filebrowser, grappelli, legacy reporting, and `api-auth` routes untouched.

**Risk:** medium — every path changes. No external consumer today (the premise of this CR), but internal callers do exist:

- Any `reverse(...)` calls that previously relied on DRF's auto-generated URL names. **Action:** grep `reverse\(` and `reverse_lazy\(` across the koalixcrm repo; update names that resolve to the router (they move under the per-app `basename`).
- Any tests hitting hard-coded `/parties/`, `/invoices/`, … URLs. **Action:** grep `'/accounts/'`, `'/invoices/'`, etc. under `test/` and update; or rewrite those tests to use `reverse()`.
- The `*_api_client.py` files in each `*_api_py` package — these are **hand-written** clients (no codegen script exists in this repo). They contain ~236 hardcoded `/snake_case/` URL strings across 57 unique paths, plus `api_path_default = ''` and an implicit `uses_workspace_id = False`. **Action:** update by hand in the same PR as CR-R2 — see CR-R4.

### CR-R3 — (Removed)

Earlier drafts of this CR proposed updating a client-generation script to target per-app schemas. **No such script exists in this repo** — the `*_api_py/*_api_client.py` files are hand-written. Updating them is folded into CR-R4. Per-app schema URLs (one per app under `/koalixcrm_<app>/api/schema/v1/`) are still produced by CR-R2 and are useful for humans and any future codegen effort, but wiring codegen is out of scope for this CR.

### CR-R4 — Update hand-written clients, tests, and any internal callers

- Run `pytest` and fix URL-based assertions.
- Grep the repo for `'/accounts/'`, `'/parties/'`, `'/invoices/'`, `'/tasks/'`, `'/projects/'`, `'/bookings/'`, `'/works/'`, `'/agreements/'`, `'/estimations/'`, `'/human_resources/'`, `'/resources/'`, `'/products/'`, `'/contracts/'`, `'/quotations/'`, `'/purchase_orders/'`, `'/sales_orders/'`, `'/despatch_advices/'`, `'/payment_reminders/'`, `'/credit_notes/'`, `'/currencies/'`, `'/taxes/'`, `'/units/'`, and the rest of the table in §2.1.
- Replace with `reverse('<basename>-list')` / `reverse('<basename>-detail', args=[pk])`, supplying the workspace-id kwarg where applicable.

**Risk:** medium if the test suite is large. Mostly mechanical.

### CR-R5 — Document the routing contract

Add `docs/api-routing.md` (or append to the existing API docs) stating:

- The normative URL shape from §3.1.
- That `koalixcrm_<app>` is an anti-collision prefix for platform composition with WFS and other quantalq.com apps.
- That every resource is workspace-scoped in the URL unless placed under `_batch/`.
- That every app owns its own OpenAPI schema (rendered as Swagger / Redoc per app); the `*_api_py` clients are hand-maintained and must be kept in sync with the schema by hand.

**Risk:** none. Docs-only.

### CR-R6 — (Optional, recommended) Freeze the old URLs with a 410 Gone

Since there is no external consumer, a hard cut is acceptable. But if any partially-integrated internal tooling points at the old flat paths, add a transitional `urls.py` block that returns `410 Gone` with a body pointing to the new URL for six months. After the freeze window, delete.

**Risk:** trivial. This is hygiene, not a requirement.

---

## 5. Out of scope

- **Data-level workspace filtering in ViewSets.** Handled by koalixcrm CR-9 (sibling effort). This CR adds `<workspace_id>` to the URL; CR-9 makes the ViewSets honour it.
- **Authentication / authorization changes.** OIDC routes are unchanged.
- **Admin, filebrowser, grappelli, legacy HTML reporting.** Unchanged.
- **Microservices (`koalixcrm_microservices/`) and MQ commands (`koalixcrm_mq_commands/`).** Unchanged — they are not mounted under the DRF router.
- **Renaming the `reporting` legacy `urls.py`.** We add a sibling `api_urls.py` rather than touching the legacy file (§3.5).
- **Picking between `snake_case` and `kebab-case`** — settled: **kebab-case** (§3.2, decision A). Impact analysis in §3.2.1.

---

## 6. Acceptance criteria

1. `curl http://<host>/koalixcrm_accounting/api/v1/1/accounts/` returns the same payload that `curl http://<host>/accounts/` returned before the change (modulo workspace filtering from CR-9).
2. All six `api/schema/v1/`, `api/swagger/v1/`, `api/redoc/v1/` triplets return 200 and the Swagger UI renders only that app's endpoints — no cross-contamination.
3. `projectsettings/urls.py` contains **zero** `router.register(...)` calls at module scope.
4. Every `router.register(...)` across the koalixcrm codebase passes an explicit `basename`.
5. `pytest` is green on the post-migration URL scheme.
6. Each `*_api_py/*_api_client.py` references only its own app's endpoints, uses the new `koalixcrm_<app>/api/v1/` prefix via `api_path_default`, sets `uses_workspace_id = True`, and uses kebab-case path segments throughout.
7. A smoke deploy that mounts koalixcrm and WFS in the same Django process — hypothetical today, real soon — has **no URL collisions** under `/admin/`, `/auth/`, or any `/*/api/v1/` prefix.

---

## 7. Rollout order

1. **CR-R1** (new per-app urls.py files) — can be merged immediately, inert until referenced.
2. **CR-R2** (rewrite projectsettings/urls.py) — the atomic cutover. All-or-nothing per app is fine; doing all six in one PR is preferred since they share the template.
3. **CR-R4** (update hand-written clients + fix tests) — must land in the same PR as CR-R2 or the test suite breaks.
4. **CR-R5** (docs) — follow-up PR.
5. **CR-R6** (410 Gone shims) — only if needed.

(CR-R3 was removed — no client-generation script exists in the repo; the `*_api_py` clients are hand-written and are updated under CR-R4.)

**Coordination with WFS:** none blocking. WFS is already on the target pattern. Once koalixcrm ships CR-R2, the two projects can be composed on the same host without collision — the original motivation for this CR.
