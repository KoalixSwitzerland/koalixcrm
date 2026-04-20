# koalixcrm API routing contract

This document is the normative reference for the shape of the koalixcrm REST
API. It was introduced by [CR-002](../change_requests/CR_002_API_ROUTING_VERSIONING_AND_APP_GROUPING.md)
and supersedes the older flat-router scheme.

## URL shape

Every REST resource in koalixcrm is exposed under exactly this pattern:

```
/<koalixcrm_app>/api/v1/<int:workspace_id>/<resource>/
/<koalixcrm_app>/api/v1/<int:workspace_id>/<resource>/<int:pk>/
/<koalixcrm_app>/api/v1/_batch/<operation>/                      # workspace-independent
/<koalixcrm_app>/api/schema/v1/
/<koalixcrm_app>/api/swagger/v1/
/<koalixcrm_app>/api/redoc/v1/
```

Each rule:

1. **`<koalixcrm_app>` is always `koalixcrm_<appname>`** — `koalixcrm_accounting`,
   `koalixcrm_contacts`, `koalixcrm_products`, `koalixcrm_core`, `koalixcrm_contracts`,
   `koalixcrm_reporting`. The `koalixcrm_` prefix is the anti-collision segment
   for the day koalixcrm apps are mounted alongside
   [`qq_workflow_support_webapp_backend`](https://github.com/quantalq/qq_workflow_support_webapp_backend)
   (WFS) apps in a single Django project. WFS apps keep their `qq_*` prefix;
   koalixcrm gets `koalixcrm_*`.
2. **`/api/v1/` is mandatory.** There are no root-mounted resources and no
   unversioned resources. Breaking serializer changes land under a new `v2`
   segment and coexist with `v1` during a deprecation window.
3. **`<workspace_id>` is a required path parameter for every workspace-scoped
   resource.** Workspace-independent endpoints (global enumerations, batch
   jobs) live under `_batch/` and omit the workspace segment.
4. **Resource segments are kebab-case** (`accounting-periods`, `phone-numbers`,
   `commercial-document-media`). `basename` values on the router match
   (`basename='accounting-period'`).
5. **Each app owns its own OpenAPI triplet.** One `drf-spectacular` schema
   per app, one Swagger UI per app, one Redoc UI per app. Schemas do not
   cross-contaminate.

## Per-app URL conf layout

```
koalixcrm/accounting/urls.py       # exports `router` + `urlpatterns`
koalixcrm/contacts/urls.py
koalixcrm/products/urls.py
koalixcrm/core/urls.py
koalixcrm/contracts/urls.py
koalixcrm/reporting/api_urls.py    # NOT urls.py — the legacy HTML reporting
                                   # views already own that name. See CR-002 §3.5.
```

Every registration passes an explicit `basename` — inferred basenames are
brittle when the ViewSet overrides `get_queryset`, and explicit naming is
required for the per-app Spectacular schemas to render `operationId`s cleanly.

Composition lives in `projectsettings/urls.py`, which:
- mounts each app's `urls.py` / `api_urls.py` under the per-app `koalixcrm_<app>/api/v1/<int:workspace_id>/` prefix, and
- exposes one `SpectacularAPIView` / `SpectacularSwaggerView` / `SpectacularRedocView` triplet per app.

## Python clients (`*_api_py/*_api_client.py`)

The `*_api_py` packages contain **hand-written** Python API clients — there is
no codegen tooling in the repo. Each client class sets:

```python
class KoalixCRM<App>APIClient(BaseAPIClient):
    api_path_env_var = 'KOALIXCRM_<APP>_API_PATH'
    api_path_default = '/koalixcrm_<app>/api/v1/'
    uses_workspace_id = True
```

and must be kept in sync with the schema by hand. When a resource is renamed,
added, or removed, update both:
- the app's `urls.py` / `api_urls.py` (routing + `basename`), and
- the app's `*_api_client.py` (method names, endpoint strings).

Per-app OpenAPI schemas are still valuable for humans reading the docs and
for any future codegen effort, but until such an effort exists the clients
are a hand-maintained artifact.

## Workspace scoping — URL layer vs data layer

CR-002 adds `<workspace_id>` to the URL path. The **data-level** filtering
(ViewSets actually honouring that parameter when constructing querysets) is
tracked separately by koalixcrm CR-9 (and WFS CR-001 on the other side). In
the interim, ViewSets accept and ignore `workspace_id` — the URL parameter
is captured but has no behavioural effect until CR-9 lands.

Custom DRF `@action` methods must accept `**kwargs` so that the router's
`workspace_id` kwarg does not break the call signature.

## External references

- WFS reference pattern: `qq_workflow_support_webapp_backend/urls.py`, `qq_workflow_support_webapp_backend/qq_workflow_support/urls.py`, `qq_workflow_support_webapp_backend/qq_human_resources_support/urls.py`.
- Originating change request: [`change_requests/CR_002_API_ROUTING_VERSIONING_AND_APP_GROUPING.md`](../change_requests/CR_002_API_ROUTING_VERSIONING_AND_APP_GROUPING.md).
