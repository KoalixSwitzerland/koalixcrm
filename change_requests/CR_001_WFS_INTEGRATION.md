# CR-001 — Changes required to integrate koalixcrm into `qq_workflow_support_webapp_backend`

**Requested by:** quantalq.com — Workflow Support Webapp team (WFS).
**Target branch:** `feature/wfs-integration-change-request` (off `develop`).
**Companion documents (external):**

- `qq_workflow_support_webapp_system` repo → `INTEGRATION_CONCEPT_QUAQ2_27_QUAQ2_28_KOALIXCRM_MODELS.md`
- `qq_workflow_support_webapp_system` repo → `HARMONIZATION_CONCEPT_QUAQ2_27_QUAQ2_28.md`

**Scope of this CR:** the set of koalixcrm-side changes that allow the WFS backend to install `koalixcrm.core`, `koalixcrm.contacts`, `koalixcrm.contracts`, `koalixcrm.djangoUserExtension`, and `koalixcrm.products` as-is (same app labels, same migrations, same model names), alongside WFS's own Django apps, in a multi-tenant (workspace-scoped) deployment, without requiring downstream forks of the koalixcrm source tree. This CR delivers a **breaking v2.0.0 release**: workspace-scoping is introduced as mandatory across the product, not as an opt-in.

**Partial harmonization included.** `core.Workspace` and `core.RoleInWorkspace` are introduced as shared models inside `koalixcrm.core`, which becomes the shared package between koalixcrm and WFS. App-specific workspace settings stay in each owning app under a `*WorkspaceSettings` model keyed to the shared `Workspace`. Object-level access grants (`RoleOnObject`) are split out into a follow-up CR-10 to keep the v2.0.0 release surface tight. The broader harmonization proposal (extracting further shared primitives beyond `core`) remains tracked separately.

**Explicitly out of scope for v2.0.0:** switching primary keys to UUID. The `(workspace, business_number)` uniqueness pattern covers the "each workspace starts numbering from 1" use case without a PK migration; any UUID transition is deferred to a later release with its own justification.

---

## 1. Why these changes are being requested

The WFS backend (Django, multi-tenant per `Workspace`) wants to adopt koalixcrm's Party data model and commercial-document family instead of building its own. To keep upstream koalixcrm and the WFS fork **bidirectionally copy-paste compatible** (a hard requirement on the WFS side), no WFS-specific edits may live inside the copied Django apps. Integration seams therefore exist on the koalixcrm side, either as settings-gated extension points or as shared primitives inside `core`.

Because v1.14.0 → v2.0.0 is already a breaking release with non-trivial migrations (party rename, UBL alignment), this CR folds the tenant-awareness step into the same release rather than shipping it as an opt-in. CR-1 through CR-7 remain additive / invariant-preserving; CR-8 introduces the shared `Workspace` / `RoleInWorkspace` models in `core`; CR-9 makes workspace-scoping mandatory across all tenant-scoped models, with a one-off data migration that places existing rows onto a "Default Workspace".

---

## 2. Prerequisites (must land first)

### P-1. Finish the Party-data-model rename (PLAN_contact_party_data_model.md, phase 4)

- **Today:** `koalixcrm/contacts/models/` contains interim names — `PartyContact`, `PartyEmail`. The active plan renames these to `Contact` and `EmailAddress`.
- **Request:** complete phase 4 of `PLAN_contact_party_data_model.md` **before** the first WFS copy. Copying a half-renamed tree guarantees divergence the next time phase 4 lands.
- **Cost:** this is already planned upstream — no new work, just sequencing.

### P-2. Complete the UBL rename (`PLAN_commercial_document_ubl_alignment.md`) beyond `contracts`

**Initial assumption (wrong):** a quick verification step with no code change.

**Actual state (2026-04):** the `contracts` app is fully renamed — `SalesDocument → CommercialDocument`, `Quote → Quotation`, `DeliveryNote → DespatchAdvice`, `PurchaseConfirmation → SalesOrder`, including migrations `0004/0005/0006`. But the UBL rename stopped at the `contracts` boundary. Meaningful stragglers exist in two other areas and must land before WFS pins its baseline, because `djangoUserExtension` is one of the five apps copied to WFS and shipping it with legacy names would bake the inconsistency into the fork permanently.

P-2 is therefore split into three sub-items:

#### P-2a. Delete the obsolete Python PDF-export microservice

**Context:** the former Python Celery task at `koalixcrm_microservices/pdf_export_task/tasks.py` was replaced by the Java PDF worker at `pdf-export-service/` (XSL-FO / Apache FOP). The Python task still exists on `develop` with broken imports (it still imports `contracts.models.quote`, `contracts.models.delivery_note`, `contracts.models.purchase_confirmation` — module paths that no longer exist after the `contracts` rename). It is non-functional and is no longer referenced by any production code path. The koalixcrm Django side is a publisher-only for `PDFExportCommand` messages now; the Java worker polls its own SQS queue.

**Change:**

- Delete the entire package `koalixcrm_microservices/pdf_export_task/` (147 lines of dead code).
- In `koalixcrm_microservices/sqs_poller.py`, remove the `PDFExportCommand.TYPE` entry from `TASK_ROUTES` (Django side no longer consumes this command type).
- Keep `koalixcrm_microservices/celery_app.py` and `sqs_poller.py` as the runtime shell — they remain for future non-PDF commands.
- Review `tests/core_api_py/test_pdf_service_endpoints.py` and delete or trim to whatever still describes a live code path.

**Migration:** none.

**Risk:** low. Removing dead code with broken imports that no prod path exercises.

#### P-2b. Complete the UBL rename in `djangoUserExtension`

**Context:** when `contracts` was UBL-aligned, the matching *template* models in `djangoUserExtension` were missed. Current state:

| Legacy (still present) | UBL-aligned (target) |
|---|---|
| class `QuoteTemplate` | `QuotationTemplate` |
| class `DeliveryNoteTemplate` | `DespatchAdviceTemplate` |
| class `PurchaseConfirmationTemplate` | `SalesOrderTemplate` |
| FK `TemplateSet.quote_template` | `quotation_template` |
| FK `TemplateSet.delivery_note_template` | `despatch_advice_template` |
| FK `TemplateSet.purchase_confirmation_template` | `sales_order_template` |
| `OptionQuoteTemplateJSONSerializer` | `OptionQuotationTemplateJSONSerializer` |
| `OptionDeliveryNoteTemplateJSONSerializer` | `OptionDespatchAdviceTemplateJSONSerializer` |
| `OptionPurchaseConfirmationTemplateJSONSerializer` | `OptionSalesOrderTemplateJSONSerializer` |

A revealing tell in `djangoUserExtension/models/template_set.py:62-66`: the mapping dict already uses the UBL keys (`"Quotation"`, `"DespatchAdvice"`, `"SalesOrder"`) on the left-hand side, but the right-hand side Python attributes are still `quote_template` / `delivery_note_template` / `purchase_confirmation_template`. The rename was half-finished.

**Java-side impact — none.** The Java PDF worker (`pdf-export-service/`) consumes templates exclusively via:

- REST (polymorphic base endpoint): `GET /document_templates/<id>/`, plus asset sub-routes `/xsl/`, `/fop-config/`, `/logo/`. Java DTO is `DocumentTemplateDto` (the base class), not subclass-specific.
- S3 (asset storage): XSL, FOP config, logo files are pulled from S3 by URL returned from the REST response.

Repo grep of `/app/koalixcrm/pdf-export-service/` and `/app/koalixcrm/app_api_java/` for `QuoteTemplate`, `DeliveryNoteTemplate`, `PurchaseConfirmationTemplate`, `quote_template`, `delivery_note_template`, `purchase_confirmation_template` → **zero hits**. The Java worker never names the subclass types or the `TemplateSet` FK fields. The rename is therefore a Django-internal refactor with no cross-repo coordination required.

**Change:**

- In `djangoUserExtension/models/document_template.py`:
  - Rename classes `QuoteTemplate → QuotationTemplate`, `DeliveryNoteTemplate → DespatchAdviceTemplate`, `PurchaseConfirmationTemplate → SalesOrderTemplate`.
  - Update `verbose_name` / `verbose_name_plural` strings to match.
- In `djangoUserExtension/models/template_set.py`:
  - Rename FK fields `quote_template → quotation_template`, `delivery_note_template → despatch_advice_template`, `purchase_confirmation_template → sales_order_template`.
  - Update the mapping dict RHS and all `fieldsets` references.
- In `djangoUserExtension/admin/document_template_admin.py` — update imports and `admin.site.register(...)` calls.
- In `djangoUserExtension/serializers/document_template_rest.py` and `serializers/template_set_rest.py` — rename serializer classes and all field/attribute references. (DRF field key in JSON changes correspondingly — no external REST consumer relies on these keys per the grep above.)
- Write migration `djangoUserExtension/migrations/0003_ubl_template_rename.py`:
  - `RenameModel('QuoteTemplate', 'QuotationTemplate')` + siblings.
  - `RenameField('TemplateSet', 'quote_template', 'quotation_template')` + siblings.
  - No `db_table` declarations exist on these models, so default table names auto-update (`djangouserextension_quotetemplate` → `djangouserextension_quotationtemplate`). No `SeparateDatabaseAndState` dance needed (unlike `contracts/0006` which had explicit `db_table`).
- Cascade through tests:
  - `tests/factories/djangoUserExtension/factory_document_template.py` — rename factory classes (`StandardQuoteTemplateFactory → StandardQuotationTemplateFactory`, etc.) and `Meta.model` references.
  - `tests/factories/contracts/commercial_document_factory.py` — update factory import.
  - `tests/e2e/test_create_sales_document_from_{contract,invoice,quote}.py` — update factory imports, test-class method names, and payload dict keys (`"template_name": "quote_template"` → `"quotation_template"`). Also consider renaming the test files to `test_create_commercial_document_from_*.py` for consistency with the `contracts` rename (decision: defer file rename, classes-only rename to keep diff small).
  - `tests/core_api_py/test_pdf_service_endpoints.py` — update factory import (if file survives P-2a).

**Migration:** one migration in `djangoUserExtension` (`0003_ubl_template_rename.py`). State + schema, RenameModel + RenameField. No data migration required.

**Risk:** low. Mechanical rename; Java does not reference the renamed names; REST keys change but have no external consumer.

#### P-2c. Minor cleanups

- `koalixcrm_mq_commands/pdf_export_command.py:15` — docstring example lists `'Quote', 'DeliveryNote'` — update to `'Quotation', 'DespatchAdvice', 'SalesOrder'`.
- `koalixcrm/core/management/commands/sync_split_migrations.py:42` — comment references historical `SalesDocument`. Leave as-is (historical context, no runtime impact).
- `auftraegekoalixnet/auftraegekoalixnet/dashboard.py:31-33` — references `koalixcrm.crm.documents.quote.Quote` / `purchase_confirmation.PurchaseConfirmation` / `delivery_note.DeliveryNote`. **Decision resolved:** the entire `auftraegekoalixnet/` directory is listed in `.gitignore` (line 50, `/auftraegekoalixnet/`). It is a local-workspace artifact — a standalone Django project scaffold that is **not** part of the shipped codebase. No action required on the repo. If the same dashboard file ever re-enters version control it should be updated to `koalixcrm.contracts.models.quotation.Quotation` / `sales_order.SalesOrder` / `despatch_advice.DespatchAdvice`; until then, the stale imports are only loaded in local developer environments that happen to have a copy of the file.

**Migration:** none.

**Risk:** none.

---

**Sequencing note:** P-2a, P-2b, P-2c are independent and can land in any order. P-2b is the only one that carries a migration. All three must complete before CR-6 cuts the `v2.0.0-wfs-baseline` tag.

#### P-2 completion record

P-2a, P-2b and P-2c landed together on branch `feature/wfs-integration-change-request` in commit `b7d91d7` (2026-04-19). Verification run the same day:

- **Fresh-DB migration** (empty SQLite, `manage.py migrate`): full chain applies cleanly; `djangoUserExtension.0003_ubl_template_rename` included.
- **`/app/koalixcrm_data/db/auftraegekoalixnet_20230101.sqlite3`** (2019-era monolithic reference DB): full v1.14.0 → v2.0.0 chain applied, including the new rename migration — no errors.
- **`/app/koalixcrm_data/db/db.sqlite3`** (current dev DB snapshot): same — clean migration.
- **`unit-django` profile** (`docker compose --env-file .env.claude --profile unit-django run --rm unit-django-runner`): 163 passed, 0 failed, 11 deselected (e2e/front-end/integration by design) in 4:01.

P-2 is therefore **Done**, not Prereq, in the summary table below.

---

## 3. Change items

Each item is a self-contained upstream PR proposal. Numbering (`CR-1` … `CR-9`) mirrors the `M1` … `M9` numbering used in the WFS integration concept, for cross-referencing. `CR-10` is an out-of-band follow-up scheduled after v2.0.0.

### CR-1 — Make `core.Tax.account_activa` / `account_passiva` optional

- **Current state:** `koalixcrm/core/models/tax.py` declares both FKs as `null=False` against `accounting.Account`.
- **Problem for WFS:** WFS does not install `koalixcrm.accounting`. With the current schema `koalixcrm.core` cannot be migrated in a WFS deployment because `Tax` migrations require `accounting.Account` to exist.
- **Proposed change:**
  - Add `null=True, blank=True` to both FKs.
  - Add a model-level `clean()` validator that enforces `not null` **only** when `'koalixcrm.accounting' in settings.INSTALLED_APPS` (or equivalently when a new setting `KOALIXCRM_ACCOUNTING_REQUIRED = True` is set).
  - Default preserves today's semantics for installs that run with `accounting`.
- **Migration:** one additive migration (`ALTER TABLE` to drop NOT NULL). No data migration.
- **Risk:** low. Existing installs continue to require the FKs via the validator.

### CR-2 — Make `CommercialDocumentPosition.product_type` FK swappable

- **Current state:** `koalixcrm/contracts/models/commercial_document_position.py`:
  `product_type = models.ForeignKey("products.ProductType", …)`
- **Problem for WFS:** WFS wants to keep the option of replacing `products.ProductType` with a plugin-provided model in later phases without forking `contracts`.
- **Proposed change:**
  - Introduce setting `KOALIXCRM_PRODUCT_TYPE_MODEL = 'products.ProductType'` (default).
  - Reference via `settings.KOALIXCRM_PRODUCT_TYPE_MODEL` in the FK declaration (Django-swappable-model pattern, same technique as `AUTH_USER_MODEL`).
- **Migration:** none. Default value is the current hard reference.
- **Risk:** low. This is the Django-standard escape hatch; well-trodden territory.

### CR-3 — Keep `koalixcrm_mq_commands` dataclass-only (zero Django import)

- **Current state:** `/app/koalixcrm/koalixcrm_mq_commands/` — on inspection looks Django-free, but there is no test that enforces it.
- **Problem for WFS:** WFS intends to copy this package verbatim and reuse the `CommandEnvelope` / `PDFExportCommand` dataclasses so that both Django processes (koalixcrm + WFS) can publish the same SQS payload to the Java FOP worker. If a Django import leaks in, the copy either pulls the whole koalixcrm app or fails to load without `DJANGO_SETTINGS_MODULE`.
- **Proposed change:**
  - Add a pytest (e.g. `tests/unit/test_mq_commands_is_django_free.py`) that imports `koalixcrm_mq_commands` *without* loading Django settings and asserts no `django.*` symbol shows up in `sys.modules` afterward.
  - If a leak is found, move the offending import into the calling signal code.
- **Migration:** none.
- **Risk:** low. It is an invariant test, not a behaviour change.

### CR-4 — Make the PDF-export SQS dispatcher swappable

- **Current state:** `koalixcrm/core/signals/pdf_export_signals.py` dispatches to SQS via a hard-coded broker reference.
- **Problem for WFS:** WFS already owns a broker / poller fleet (`qq_wfs_microservices.brokers`, `qq_wfs_sqs_commands`). Running two independent SQS client layers inside one Django process — one for workflow-tag PDFs, one for commercial-document PDFs — is avoidable.
- **Proposed change:**
  - Introduce setting `KOALIXCRM_PDF_EXPORT_DISPATCHER` (dotted path to a callable `(command: PDFExportCommand) -> None`).
  - Default: the existing koalixcrm SQS sender, wrapped so nothing changes for current installs.
  - The signal resolves the callable at dispatch time (lazy import), not at module load.
- **Migration:** none.
- **Risk:** low. Pure refactor behind a setting.

### CR-5 — Enforce that `core`, `contacts`, `contracts`, `djangoUserExtension`, `products` have **zero** imports from `reporting`, `accounting`, `subscriptions`

- **Current state:** per current code review, this already appears to hold — but there is no test that guards it going forward.
- **Problem for WFS:** WFS does not install `reporting`, `accounting`, or `subscriptions`. A single accidental `from koalixcrm.reporting.models import Project` in future contracts code would break the WFS build silently in a follow-up release.
- **Proposed change:**
  - Add a pytest (e.g. `tests/unit/test_fork_isolation.py`) that uses `importlib` to walk every module under `koalixcrm/{core,contacts,contracts,djangoUserExtension,products}/` and asserts none of them reference the forbidden app labels, either at module import time or in their model FK `to=` references.
  - Document the invariant in a new file at the repo root: `FORK_CONTRACT.md` (see CR-7).
- **Migration:** none.
- **Risk:** low. Invariant test.

### CR-6 — Version-stamp the point at which WFS pins

- **Current state:** koalixcrm is mid-execution on `PLAN_contact_party_data_model.md` phase 4. WFS's first copy will happen at a specific commit.
- **Proposed change:**
  - After P-1 is done, cut an annotated tag (e.g. `v2.0.0-wfs-baseline`) on koalixcrm `develop`. WFS pins its first copy to this tag.
  - Document the tag and the cross-repo pointer in `FORK_CONTRACT.md` (see CR-7).
- **Migration:** none.
- **Risk:** none.

### CR-7 — Publish a model-level fork contract (`FORK_CONTRACT.md`)

- **Problem for WFS:** today there is no explicit statement of which koalixcrm models / fields / signals are "public surface that forks rely on" versus which are internal. Every upstream rename risks breaking the WFS copy silently.
- **Proposed change:** add `FORK_CONTRACT.md` at the koalixcrm repo root, listing:
  - The five apps in the "public fork surface" (`core`, `contacts`, `contracts`, `djangoUserExtension`, `products`).
  - The models inside those apps that are considered fork-public (essentially all concrete models; this is not intended to be a narrow contract).
  - The fields on those models that are fork-public (all concrete fields except those prefixed `_`).
  - The signals emitted by those apps that are fork-public.
  - The commitment: renames or drops of anything in the fork-public surface are announced by opening an issue labelled `fork-breaking` at least one release cycle before the change lands on `develop`.
- **Migration:** none.
- **Risk:** none. It is a documented commitment, nothing more.

### CR-8 — Introduce shared `core.Workspace` and `core.RoleInWorkspace` (REQUIRED)

Covers the workspace-level access-control substrate that both products share:

- `core.Workspace` — the tenant model (coarse scope).
- `core.RoleInWorkspace` — which workspaces a user can see (workspace-level grants).

Object-level grants (`RoleOnObject`, fine-grained per-object sharing) were considered for inclusion here but have been **deferred to CR-10** to keep the v2.0.0 release surface tight. The shared `Role` enum introduced here is forward-compatible with that future addition: CR-10 reuses it verbatim.

> **This item MUST be implemented on the `qq_workflow_support_webapp_backend` side as well.** `Workspace` and `RoleInWorkspace` are part of the shared `core` surface consumed verbatim by both products. WFS must import (or copy, depending on the adopted consumption strategy) these models and respect the same enforcement rules in its own admin and API layers. Divergence here breaks the entire integration premise.

#### 8.1. `core.Workspace`

Field set is the **union** of what koalixcrm and WFS each had on day one — designed so neither side has to carry product-specific Workspace fields outside `core`:

```python
class Workspace(models.Model):
    name                          = models.CharField(max_length=200, unique=True)
    description                   = models.TextField(blank=True, default='')
    external_workspace_reference  = models.CharField(
        max_length=255, blank=True, default='',
        help_text='Short prefix for human-readable identifiers (e.g. REP, MSD). '
                  'Used in IDs like REP-TASK-1.',
    )
    is_active                     = models.BooleanField(default=True, db_index=True)
    organization                  = models.ForeignKey(
        'contacts.Organization', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='workspaces',
        help_text='Optional: the legal entity this workspace represents.',
    )
    color                         = models.CharField(max_length=7, blank=True,
        help_text='Hex color used by the admin header as a visual cue to prevent workspace mix-ups.')
    date_added                    = models.DateField(auto_now_add=True)
    last_modified                 = models.DateField(auto_now=True)
```

Origin of each field:

- `name`, `organization`, `color`, `date_added`, `last_modified` — koalixcrm-introduced (CR-8 first revision).
- `description`, `external_workspace_reference`, `is_active` — adopted from the WFS `Workspace` so the shared model can replace the WFS one without losing fields.
- WFS-specific adjacent tables (`WorkspaceConfig`, `WorkspaceLogo`, `WorkspaceMedia`) stay on the WFS side as `*WorkspaceSettings`-style models keyed to the shared `Workspace`.

`external_workspace_reference` is `blank=True` here even though WFS has it as `blank=False`: the schema column is required by the shared contract, but per-product validation can still reject blanks where the product needs them (WFS will keep its `clean()` enforcing non-blank).

Anything product-specific (invoice-number prefixes, default currency, template defaults, WFS workflow settings, etc.) lives in **per-app `*WorkspaceSettings` models**, not on `Workspace` itself. Example split:

- `contracts.ContractsWorkspaceSettings(workspace=OneToOne, default_currency, invoice_number_prefix, next_invoice_number, …)`
- `products.ProductsWorkspaceSettings(workspace=OneToOne, default_product_type, …)`
- `djangoUserExtension.TemplateWorkspaceSettings(workspace=OneToOne, default_template_set, …)`
- (WFS side) `qq_workflow_support.WFSWorkspaceSettings(workspace=OneToOne, …)`

Each app owns and migrates its own settings table. Adding a new product-specific setting never requires a change to `core`.

#### 8.2. Shared role vocabulary

`RoleInWorkspace` references a shared `Role` enum that is the **union** of what koalixcrm and WFS each used on day one. Both products commit to consuming the union enum so a future role addition is a single edit on the koalixcrm side picked up by both:

```python
# core/models/access.py
class Role(models.TextChoices):
    ADMIN           = 'admin',           'Admin (full control)'
    EDITOR          = 'editor',          'Editor (edit + read)'
    VIEWER          = 'viewer',          'Viewer (read only)'
    COMMENTER       = 'commenter',       'Commenter (read + comment)'
    EMPLOYEE        = 'employee',        'Employee (WFS: workflow participant)'
    LINE_MANAGER    = 'line_manager',    'Line Manager (WFS: people management)'
    PROJECT_MANAGER = 'project_manager', 'Project Manager (WFS: project lead)'
```

DB stores lowercase snake_case codes (`'line_manager'`, `'project_manager'`) — chosen for cross-product schema consistency. WFS will migrate from its existing `'LineManager'` / `'ProjectManager'` codes to these as part of its mirror CR.

The `Role.COMMENTER`, `Role.EDITOR` and `Role.VIEWER` codes originate on the koalixcrm side and are unused by WFS day one — WFS adopts them as no-op codes that become available for fine-grained permission grants once needed. Symmetrically, `EMPLOYEE` / `LINE_MANAGER` / `PROJECT_MANAGER` are WFS-domain codes that koalixcrm stores but does not actively grant in admin workflows.

The enum is forward-compatible with CR-10 (`RoleOnObject`).

#### 8.3. `core.RoleInWorkspace` (workspace-level grants — Group-based)

The grant subject is **`auth.Group`**, not the user directly. This matches WFS's existing model (`/app/qq_workflow_support_webapp_backend/qq_workflow_support/models/role_in_workspace.py`) and is the more enterprise-friendly shape — Keycloak group claims can be mapped to Django groups, which then carry the workspace role:

```python
class RoleInWorkspace(models.Model):
    group     = models.ForeignKey('auth.Group', on_delete=models.CASCADE,
                                   related_name='workspace_roles', db_index=True,
                                   help_text='Django auth group whose members hold this role.')
    workspace = models.ForeignKey('core.Workspace', on_delete=models.CASCADE,
                                   related_name='group_role_assignments')
    role      = models.CharField(max_length=64, choices=Role.choices)
    class Meta:
        unique_together = [('group', 'workspace', 'role')]
```

Effective access for a user: `user → user.groups.all() → RoleInWorkspace rows`. This is the **sole source of truth** for "which workspaces can this user see?". It is deliberately decoupled from `contacts.OrganizationMembership` (which describes business relationships between parties) — they serve different purposes and must not be conflated. A `Workspace` may optionally point to an `Organization` (see `Workspace.organization` above), but access control does not flow through that link.

Why Group-based:

- WFS already uses Group-based grants — adopting the same shape on the koalixcrm side avoids a breaking schema reshape on the WFS side later.
- Keycloak (the SSO source) emits group claims naturally; mapping claims → `auth.Group` is a one-line backend hook. Mapping claims → individual user assignments would require per-user provisioning logic.
- Bulk role administration (onboard 10 employees → add to "Workspace W Employees" group → done) is intrinsic, no admin tooling required.
- An explicit per-user grant is still expressible: create a singleton group named after the user and assign the role to it. This is rare enough not to warrant a separate code path.

#### 8.4. *(Deferred to CR-10)*

The fine-grained per-object grant model (`RoleOnObject`) was previously specified in this position. It has been moved to **CR-10 — Object-level access grants** to keep the v2.0.0 surface focused on workspace-level isolation. CR-10 will reuse the shared `Role` enum (§8.2) verbatim.

#### 8.5. `effective_roles()` and `user_workspaces()` (workspace-level only in CR-8)

```python
# core/access.py
def effective_roles(user, obj) -> set[str]:
    """Role codes the user holds on this object via group→workspace grants.
    CR-10 will OR in object-level grants without changing the signature."""
    if user is None or not getattr(user, 'is_authenticated', False):
        return set()
    if user.is_superuser:
        return set(Role.values)
    workspace = getattr(obj, 'workspace', None)
    if workspace is None:
        return set()
    return set(
        RoleInWorkspace.objects.filter(
            group__in=user.groups.all(),
            workspace=workspace,
        ).values_list('role', flat=True)
    )

def user_workspaces(user):
    """Active workspaces the user can reach via any group-based role grant.
    Used by the dashboard switcher and the switch view's auth check."""
    if user is None or not getattr(user, 'is_authenticated', False):
        return Workspace.objects.none()
    if user.is_superuser:
        return Workspace.objects.filter(is_active=True)
    return Workspace.objects.filter(
        is_active=True,
        group_role_assignments__group__in=user.groups.all(),
    ).distinct()
```

And on the manager (CR-9 wiring):

```python
# WorkspaceAwareManager.visible_to(user)
return self.filter(workspace__in=user_workspaces(user))
```

A single workspace-level branch in v2.0.0. CR-10 will OR'd-in the object-level branch in a backwards-compatible extension. Superusers bypass (treated as holding every role on every active workspace).

#### 8.6. Grappelli dashboard workspace switcher (shared UI module, REQUIRED in v2.0.0)

The primary post-authentication surface for selecting the active workspace is a Grappelli dashboard module that ships as part of the shared `core` deliverable. Both koalixcrm and WFS install this module onto their respective admin dashboards; because it is part of the shared `core` contract, the user sees the same switcher regardless of which product they are in.

**Why this belongs in CR-8, not CR-9.** The dashboard switcher is part of the *shared access-control surface*: it is the user-visible counterpart to `RoleInWorkspace`, driven directly by that table. Shipping it from `core` is the only way to guarantee that koalixcrm and WFS present the same switching UX with the same data source. The broader admin integration (per-`ModelAdmin` queryset filtering, FK scoping, save-time revalidation, header switcher) stays in CR-9 §9.8 — those are product-specific admin concerns.

**Reference implementation location.** `koalixcrm/core/admin/dashboard_modules.py`. Exported so Grappelli dashboard configs in both products can register it by dotted path.

**Module behaviour.**

- Renders the workspaces returned by `user_workspaces(request.user)` (all roles, not just admin; `is_active=False` workspaces excluded).
- Each row shows: workspace name, `Workspace.color` as a visual swatch, the user's role(s) in that workspace (union across all of the user's groups), and a "currently active" marker on the row matching `request.session['active_workspace_id']`.
- Clicking a workspace writes `request.session['active_workspace_id']`, writes a `WorkspaceSwitchEvent(user, from_ws, to_ws, timestamp)` audit row, and redirects to the admin index. Same backend endpoint as the header switcher (CR-9 §9.8) — a single view handles both surfaces.
- Zero-workspace state: renders a clear "no workspace access — contact an administrator" message. No other dashboard modules render.
- Single-workspace state: module still renders (so the active-workspace context is always visible) but the switch action is a no-op.

**WFS-side requirement.** `qq_workflow_support_webapp_backend` must register the same module on its Grappelli dashboard. This is an explicit part of the mirror-implementation commitment called out at the top of CR-8.

#### 8.7. Scope in v2.0.0 vs. follow-up release

**Included in v2.0.0 (this CR):**

- Two models (`Workspace`, `RoleInWorkspace` — **Group-based**) plus the `WorkspaceSwitchEvent` audit row.
- Shared `Role` enum, union of koalixcrm + WFS day-one vocabularies (forward-compatible with CR-10).
- `effective_roles()` and `user_workspaces()` helpers (workspace-level only — CR-10 extends).
- Workspace-level queryset filter wired into `WorkspaceAwareManager` (CR-9 §9.3).
- Grappelli dashboard workspace switcher module (§8.6), shared between koalixcrm and WFS.

**Deferred to CR-10 (object-level grants):**

- `RoleOnObject` model, manager, admin, and `clean()` validator restricting target content types.
- Object-level branch in `effective_roles()` and `WorkspaceAwareManager.visible_to()`.
- Per-object "Share with…" admin widget on every scoped model's change page.
- Bulk grant / revoke tooling.
- UI for inspecting "who has access to this object?".

Rationale: keeping CR-8 to workspace-level only shrinks the v2.0.0 access-control surface to what the WFS integration actually requires on day one. Object-level grants are additive — they can land in CR-10 without a second breaking migration on the workspace tables.

#### 8.8. Migration

Schema-only (three new tables — `Workspace`, `RoleInWorkspace`, `WorkspaceSwitchEvent`). The data migration that creates the Default Workspace lives under CR-9 so the dependent-row backfill is co-located with the column addition.

#### 8.9. Risk

Medium. Load-bearing shared models and UI. Listed explicitly in `FORK_CONTRACT.md` (CR-7) as fork-public, with a stricter change-procedure commitment than other models. WFS-side mirror implementation (both `Workspace` / `RoleInWorkspace` and the Grappelli dashboard module) must be tracked in the companion WFS change request.

### CR-9 — Mandatory workspace-scoping + one-off data migration (REQUIRED)

This is the largest item in the CR and the one that makes v2.0.0 a breaking release. Workspace-scoping is introduced **unconditionally** — there is no `KOALIXCRM_TENANT_MODEL = None` fallback. The opt-in design from the earlier revision has been dropped because v1.14.0 → v2.0.0 is already a breaking migration; folding tenancy in avoids a second schema-wide upheaval later.

#### 9.1. Current state

- Koalixcrm is single-tenant. Every row of `Party`, `Contract`, `CommercialDocument`, `DocumentTemplate`, etc. is globally visible to every staff user.
- There is no `workspace` column on any model.

#### 9.2. Design decisions (changed since earlier revision)

| Decision | Rationale |
|---|---|
| Mandatory, not opt-in. | v2.0.0 is already a breaking release. An opt-in mixin with class-body `if settings.X:` conditionals adds complexity solely to preserve upstream-unchanged behaviour — a constraint that no longer applies. |
| `Workspace` and `RoleInWorkspace` live in shared `core` (per CR-8). | `core` is the 100% shared package between koalixcrm and WFS. The workspace model is not swappable; both products use the same one. |
| `Workspace` field set is the union of koalixcrm + WFS day-one fields. | Lets the shared model fully replace WFS's existing `Workspace` without losing data. See CR-8 §8.1 for the breakdown. |
| `RoleInWorkspace` grants are **Group-based** (not user-based). | Matches WFS's existing shape; aligns with Keycloak group-claim provisioning; bulk admin is intrinsic. See CR-8 §8.3. |
| Admin scoping uses `RoleInWorkspace`, not `OrganizationMembership`. | Access control is a user→group→workspace concept; business relationships between parties (`OrganizationMembership`) are unrelated and must not be conflated. |
| Primary keys stay integer. | UUID migration is out of scope; `(workspace, business_number)` covers the "numbering restarts per workspace" need. |

#### 9.3. `WorkspaceScopedModel` abstract base (new)

```python
# koalixcrm/core/models/workspace_scoped.py
from django.db import models

class WorkspaceScopedModel(models.Model):
    workspace = models.ForeignKey(
        'core.Workspace',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = WorkspaceAwareManager()

    class Meta:
        abstract = True
```

No settings conditional, no null fallback. Every model in the list in §9.5 inherits from this.

`WorkspaceAwareManager` implements a context-local active-workspace filter (analogous to `django-scopes`). Management commands, migrations, and shells fall back to unscoped behaviour when no active workspace is set, and raise `WorkspaceContextMissing` inside request-handling code to prevent accidental cross-tenant reads.

#### 9.4. Per-workspace numbering

For every model that today carries a unique human-facing number (invoice number, contract number, customer number, product code, …), v2.0.0 introduces a `business_number` integer field with `unique_together = ('workspace', 'business_number')`. Each workspace therefore starts numbering from 1 independently, without a UUID PK change. The next-number allocator is stored on the corresponding `*WorkspaceSettings` model (e.g. `ContractsWorkspaceSettings.next_invoice_number`).

The exhaustive mapping of "which fields become `business_number`" is tracked in the accompanying implementation plan; items of note: `Invoice.invoice_number`, `Contract.contract_number`, `Quotation.quotation_number`, `Product.product_code`.

#### 9.5. Which concrete models inherit `WorkspaceScopedModel`

**Workspace-scoped:**

- `contacts.Party` (and MTI children `Organization`, `Contact` / `PartyContact`) — the workspace FK lives on the MTI parent only; children inherit by join.
- `contacts.PartyGroup`, `contacts.Address`, `contacts.PhoneNumber`, `contacts.EmailAddress` / `contacts.PartyEmail`, `contacts.CustomerBillingCycle`.
- `contacts.PartyRole`, `contacts.PartyIdentification`, `contacts.OrganizationMembership`, `contacts.OrganizationRelationship`.
- `contacts.AddressAssignment`, `contacts.PhoneAssignment`, `contacts.EmailAssignment`, `contacts.PartyGroupMembership`.
- `contracts.Contract`.
- `contracts.CommercialDocument` (and all MTI children: `Invoice`, `CreditNote`, `Quotation`, `DespatchAdvice`, `SalesOrder`, `PurchaseOrder`, `PaymentReminder`).
- `contracts.CommercialDocumentPosition`, `contracts.TextParagraphInCommercialDocument`, `contracts.CommercialDocumentMedia`.
- `contracts.PostalAddressForContract`, `contracts.PhoneAddressForContract`, `contracts.EmailAddressForContract`.
- `djangoUserExtension.UserExtension`, `djangoUserExtension.TemplateSet`, `djangoUserExtension.DocumentTemplate` (all subclasses), `djangoUserExtension.TextParagraphInDocumentTemplate`.
- `products.ProductType`, `products.Product`, `products.Price`, `products.ProductPrice`, `products.CustomerGroupTransform`.
- `core.PDFExportProcess`.
- Per-app `*WorkspaceSettings` models (CR-8) — scoped by definition; one row per workspace.

**Workspace-global** (do **not** inherit — catalogues shared across workspaces):

- `core.Workspace`, `core.RoleInWorkspace` themselves.
- `core.Currency`, `core.CurrencyTransform`.
- `core.Unit`, `core.UnitTransform`.
- `core.Tax`.

Rationale for the global set: exchange rates, VAT classes, and unit definitions are jurisdiction-wide; per-workspace overrides, if ever needed, are better modelled as a separate override table later.

#### 9.6. Unique-constraint adjustments

Every uniqueness declaration on a workspace-scoped model becomes unconditional per-workspace:

```python
class Meta:
    unique_together = [('workspace', 'email')]
```

No setting branch. v1.14.0 global-unique semantics are replaced by per-workspace semantics in v2.0.0; this is called out in the release notes and covered by the data migration in §9.7.

#### 9.7. Data migration from v1.14.0

Three-phase schema migration per affected app (to keep locking windows short on large installs):

1. **Add nullable `workspace_id` FK** to every affected table.
2. **Data migration (one-shot, runs once):**
   - Create `Workspace(name="Default Workspace", is_active=True)` if no workspaces exist.
   - Stamp every existing row on affected tables with this workspace's id (chunked updates).
   - Create an `auth.Group` named `"Default Workspace Admins"`, add every `is_staff=True` user to it, and create a single `RoleInWorkspace(group=that_group, workspace=default_workspace, role='admin')` so visibility is preserved post-upgrade. (Group-based — see CR-8 §8.3.)
   - Populate per-app `*WorkspaceSettings` rows with defaults (current global values become the Default Workspace's settings).
3. **`ALTER TABLE … SET NOT NULL`** on `workspace_id` columns, plus creation of the new `unique_together` indexes.

The migration is idempotent and re-runnable on partially-migrated databases (guarded by presence of a `Default Workspace` row).

#### 9.8. Admin integration (driven by `RoleInWorkspace`)

**Visibility.** `WorkspaceScopedModelAdmin.get_queryset` uses the workspace-level filter from CR-8 §8.5: rows visible via workspace-level grant OR via superuser bypass. (CR-10 will OR in an object-level branch in a backwards-compatible extension.)

**FK dropdown scoping.** `formfield_for_foreignkey` restricts every FK choice to objects in the *active workspace*. An Invoice's product/party dropdowns cannot list rows from another workspace.

**Save-time validation (defence-in-depth).** `save_model` enforces two invariants on every write:

1. `obj.workspace_id == request.active_workspace.id` — the row being saved belongs to the active workspace. Catches the two-tab race (user switches workspace in one tab while another tab still has an edit form open).
2. Every FK on `obj` points at a row in the active workspace. Catches attempts to cross-link via constructed POST payloads.

Violations reject the save with a clear error rather than silently writing cross-workspace data.

**Active-workspace context.**

- **Authentication is handled by Keycloak (SSO) and MUST NOT be modified by this CR.** No workspace-selection step is inserted into the Keycloak login form or the OIDC callback flow. Workspace selection happens entirely inside the koalixcrm / WFS admin *after* the user is already authenticated.
- `WorkspaceContextMiddleware` reads `request.session['active_workspace_id']` and sets `request.active_workspace`. If the session has no active workspace yet (first request after Keycloak login, or session expired and re-established), middleware picks one deterministically:
  - If the user holds exactly one `RoleInWorkspace` → activate it silently. User sees no additional step.
  - If the user holds several → activate the lowest-id workspace among them as a stable default. User is free to switch immediately via either surface below.
  - If the user holds none → admin renders an empty "no workspace access — contact an administrator" dashboard state. No models are listed, no switcher is shown.

- **Two switching surfaces, both post-authentication:**
  - **Grappelli dashboard module** — primary surface. Ships from shared `core` under CR-8 §8.6 (not duplicated here; both products install the same module). Required, not optional.
  - **Header switcher** in the admin bar — product-specific, always visible across every admin page for mid-session switching. Built in CR-9 as part of the product's admin integration and delegates to the same switch view as the dashboard module.
- Switching redirects to the admin index (the previously-visited URL is intentionally dropped because record IDs may not exist in the new workspace) and writes a `WorkspaceSwitchEvent(user, from_workspace, to_workspace, timestamp)` audit row. One switch view in `core` backs both the dashboard module and the header switcher.
- `Workspace.color` (CR-8 §8.1) tints the admin header band. This is the primary user-visible safeguard against mix-ups: a glance at the header colour tells the user which workspace they are operating in. Far more effective than any backend check at preventing the "I edited the wrong record" class of error.
- **Out of scope for v2.0.0:** mapping Keycloak group / role claims to `RoleInWorkspace` rows automatically. `RoleInWorkspace` is managed manually (or via API) for now. Claim-driven provisioning is a candidate for a later release.

**Role → Django permission mapping.** The shared `Role` enum (CR-8 §8.2) maps to Django's per-model `add`/`change`/`delete`/`view` perms at request time. Mapping is centralised in `core.access.permissions_for_role()`. CR-10 will reuse the same mapping for object-level grants.

**Deliberate non-coupling.** `contacts.OrganizationMembership` (business relationship between parties) plays no role in admin visibility. A user can have a `RoleInWorkspace` in a workspace whose optional `Workspace.organization` points to an Org they are not a member of — that is allowed and expected (e.g. an external bookkeeper).

#### 9.9. Risks and mitigations for CR-9

| Risk | Mitigation |
|---|---|
| Data migration times out on large production databases during step 2. | Chunked updates in the data migration; document the expected duration in the release notes; provide a dry-run management command. |
| Users who were implicit "global admins" in v1.14.0 lose visibility after upgrade because no `RoleInWorkspace` row exists for their groups. | Migration auto-creates a "Default Workspace Admins" group, adds every `is_staff=True` user to it, and grants the group `admin` role on the Default Workspace. Called out in release notes. |
| MTI children accidentally get their own `workspace_id` column (duplication). | Mixin applied to the MTI parent only. Invariant test asserts single-column placement per MTI tree. |
| `core.Workspace` / `core.RoleInWorkspace` drift between koalixcrm and WFS over time. | Extend CR-5's fork-isolation test to additionally assert schema equality against a snapshot in `FORK_CONTRACT.md` (CR-7). |
| Cross-workspace leakage via unscoped managers or raw SQL. | `WorkspaceAwareManager.raise_on_missing_context=True` inside request handlers. Dedicated integration tests per app attempt cross-workspace reads and expect empty results. |

### CR-10 — Object-level access grants (`RoleOnObject`) — DEFERRED, post-v2.0.0

Originally bundled into CR-8; split out to keep the v2.0.0 release surface tight. CR-10 is **additive** — it does not require a migration of existing workspace-scoped tables — and can therefore land any time after v2.0.0 ships without a coordinated breaking-release window.

#### 10.1. Scope

- New model `core.RoleOnObject` (user, GenericForeignKey to any workspace-scoped row, `role` from the shared `Role` enum, `granted_by`, `granted_at`, `expires_at`).
- Custom manager `RoleOnObjectManager` with `.active()` filtering out expired grants.
- `clean()` validator rejecting workspace-global content types (currencies, units, taxes) as targets.
- Extension of `core.access.effective_roles(user, obj)` to OR-in object-level grants.
- Extension of `WorkspaceAwareManager.visible_to(user)` to OR-in `pk__in=RoleOnObject.objects.active().filter(...)`.
- Raw Django-admin UI on `RoleOnObject` for pilot use.
- Per-object "Share with…" admin widget on every scoped model's change page.
- Bulk grant / revoke tooling.
- UI for inspecting "who has access to this object?".

#### 10.2. Semantics (locked in CR-8 §8.2 by the shared Role enum)

- An object-level grant is **additive** to whatever workspace-level grants the user has; it never downgrades workspace-level access.
- A `RoleOnObject` grant does **not** implicitly grant access to the containing workspace's other rows.
- Expired grants (`expires_at < now`) are filtered out at query time.

#### 10.3. Migration

Schema-only — one new table (`crm_roleonobject`) plus its indexes. No backfill.

#### 10.4. Risk

Low — additive table, no changes to existing rows, OR'd branch is empty-table-cheap until grants exist.

#### 10.5. WFS-side impact

Mirror implementation required when CR-10 lands, identical to CR-8: WFS imports/copies the `RoleOnObject` model, manager, admin, and the extension to `effective_roles` / `visible_to`. Tracked separately at the time CR-10 is scheduled.

---

## 4. Summary table

| CR | Title | Status | Default-behaviour impact | Blocking WFS? |
|---|---|---|---|---|
| P-1 | Finish `PLAN_contact_party_data_model.md` phase 4 | Prereq | n/a (already planned) | Yes |
| P-2a | Delete obsolete Python PDF export microservice | **Done** (commit `b7d91d7`, 2026-04-19) | None (dead code removed) | Yes |
| P-2b | UBL rename in `djangoUserExtension` templates + migration `0003_ubl_template_rename` | **Done** (commit `b7d91d7`, 2026-04-19) | Table renames + FK field renames (no data migration); Java unaffected | Yes |
| P-2c | Minor cleanups (docstring + stale-dashboard decision) | **Done** (commit `b7d91d7`, 2026-04-19) | None | No |
| CR-1 | `core.Tax` accounting FKs nullable + validator | Proposed | None (validator preserves required-ness when accounting app installed) | Yes |
| CR-2 | `CommercialDocumentPosition.product_type` swappable | Proposed | None | Yes |
| CR-3 | Enforce `koalixcrm_mq_commands` Django-free | Proposed | None | Yes |
| CR-4 | `KOALIXCRM_PDF_EXPORT_DISPATCHER` swappable | Proposed | None (default keeps current sender) | Yes |
| CR-5 | Fork-isolation invariant test | Proposed | None | Yes |
| CR-6 | Cut `v2.0.0-wfs-baseline` tag | Proposed | None | Yes |
| CR-7 | `FORK_CONTRACT.md` at repo root | Proposed | None | No (but strongly requested) |
| CR-8 | Shared `core.Workspace` + `core.RoleInWorkspace` + Grappelli workspace-switcher dashboard module | Proposed | **Breaking (v2.0.0)** — new tables, shared role enum, workspace-level enforcement, shared switcher UI. Mirror implementation required in WFS. | **Yes, required** |
| CR-9 | Mandatory workspace-scoping + data migration | Proposed | **Breaking (v2.0.0)** — `workspace_id` column on all scoped tables; per-workspace uniqueness | **Yes, required** |
| CR-10 | Object-level access grants (`RoleOnObject` + per-object share UI) | Deferred | Additive — new `RoleOnObject` table, OR'd branch in `effective_roles` / `WorkspaceAwareManager.visible_to`. No migration of existing tables. | No (post-v2.0.0) |

---

## 5. Proposed landing order

1. **P-1** (remaining prerequisite). P-2a/b/c already landed in commit `b7d91d7` (2026-04-19).
2. **CR-8** — shared `Workspace` + `RoleInWorkspace` models in `core`. Must precede CR-9 because CR-9's FK targets them.
3. **CR-9** — mandatory workspace-scoping + one-off data migration. Largest item; lands before CR-1/CR-2 so their migrations can assume the workspace column exists.
4. **CR-1, CR-2, CR-4** — independent, can land in parallel.
5. **CR-3, CR-5** — invariant tests; land after the underlying changes.
6. **CR-7** — `FORK_CONTRACT.md`, depends on the above being agreed.
7. **CR-6** — cut the `v2.0.0-wfs-baseline` tag last.

Total estimated effort: **14–20 working days** on the koalixcrm side, concentrated in CR-8 + CR-9 (the data migration and admin scoping account for most of it). CR-1 through CR-7 are each roughly half a day.

---

## 6. Relationship to the broader harmonization discussion

This CR **partially adopts** the harmonization proposal (`HARMONIZATION_CONCEPT_QUAQ2_27_QUAQ2_28.md` on the WFS-system side): `Workspace` and `RoleInWorkspace` are introduced inside `koalixcrm.core` as shared primitives, consumed verbatim by both products. `koalixcrm.core` therefore becomes the first piece of 100% shared surface between koalixcrm and WFS.

What remains deferred (i.e. *not* in this CR) from the harmonization proposal:

- Moving `UserProfile` / extended-user constructs into shared `core`. `djangoUserExtension.UserExtension` stays where it is; unifying it with WFS's user profile model is a later harmonization step.
- Extracting further shared primitives (e.g. addressing, contact details) into a standalone `core` package with its own release cadence. For now, shared code lives in `koalixcrm.core` under the koalixcrm release.
- Any WFS-side refactor to consume `Workspace` / `RoleInWorkspace` from koalixcrm rather than its own copy. That is a WFS-side decision and is tracked on that side.

---

## 7. Acceptance criteria

- ✅ CI on koalixcrm `develop` stays green after CR-8 + CR-9 land.
- ✅ The v1.14.0 → v2.0.0 data migration runs cleanly on a snapshot of a current production database, creates exactly one `Workspace(name="Default Workspace")`, stamps every existing scoped row with its id, and creates one `RoleInWorkspace(user, default_workspace, role='admin')` per `is_staff=True` user.
- ✅ After the migration, logging in as any previously-staff user in the Django admin shows the same rows as before (no visible change) — confirming the admin scoping via `RoleInWorkspace` is non-regressive on single-workspace installs.
- ✅ A second workspace can be created post-migration and its rows are not visible to users who lack a `RoleInWorkspace` row for it (cross-workspace isolation test).
- ✅ CR-5's fork-isolation test passes on `develop` and includes assertions for `core.Workspace` / `core.RoleInWorkspace` schema stability.
- ✅ CR-3's `koalixcrm_mq_commands` Django-free test passes on `develop`.
- ✅ A WFS-side integration test can install `koalixcrm.core`, `koalixcrm.contacts`, `koalixcrm.contracts`, `koalixcrm.djangoUserExtension`, `koalixcrm.products` against a WFS database and perform the smoke test described in §7.4 of the WFS integration concept, with `Workspace` and `RoleInWorkspace` sourced from `koalixcrm.core`.

---

## 8. Points of contact

- **Upstream (koalixcrm):** _TBD — maintainer assignment pending._
- **Downstream (WFS):** `aaron.riedener@quantalq.com`.

Open questions and clarifications should be filed as GitHub issues against koalixcrm with label `cr-001-wfs-integration`.

---

*End of change request.*
