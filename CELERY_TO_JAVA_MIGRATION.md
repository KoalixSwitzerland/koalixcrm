# PDF Service Migration — Python/Celery → Java/Spring Boot

**Status:** planning accepted, not yet implemented
**Tracking issue:** [KoalixSwitzerland/koalixcrm#386](https://github.com/KoalixSwitzerland/koalixcrm/issues/386)
**Owner:** @aaronriedener

## Why

The current PDF-export microservice is a Python/Celery worker that runs
`django.setup()` and speaks to the database via the Django ORM. That violates
the rule that the microservice must only talk to koalixCRM through the REST
API. We are taking the opportunity to also:

1. Move the service to **Java**, which is the native runtime of Apache FOP —
   eliminating the FOP subprocess call and the `/usr/bin/fop` binary.
2. Keep the Django REST API **JSON-only**. All XSL-FO XML aggregation moves
   into the microservice.
3. Reuse the existing **OIDC M2M** auth the other service clients already use.

## Scope

### In scope

- A new Java microservice (`pdf-export-service`) consuming SQS and rendering
  commercial documents to PDF via Apache FOP as a library.
- A new Java client library (`app_api_java`) mirroring the role of
  `koalixcrm/*_api_py`, hand-written with Spring WebClient.
- New JSON-only Django REST endpoints the worker needs.
- Presigned-S3-URL endpoints for template assets (XSL, FOP config, logo).
- Removal of:
  - `koalixcrm_microservices/` (Python Celery worker)
  - `koalixcrm_mq_commands/` (Python envelope package)
  - Every `serialize_to_xml()` method on Django models
  - `koalixcrm/core/documents/pdf_export.py` and every `create_pdf(...)`
    model method
  - `koalixcrm/core/views/renderer.py` (`XSLFORenderer`)
  - `docker/requirements/celery.txt`
  - `docker/dev/Dockerfile.celery`, `docker/prod/Dockerfile.celery`
- Updated architecture documentation under `doc/pdf_creation_service/`.

### Out of scope

- Any synchronous PDF generation path (decision **A**: sync path is deleted —
  only the async SQS → Java flow remains).
- Changes to non-PDF microservices or other SQS consumers.
- UBL alignment (tracked separately in `PLAN_commercial_document_ubl_alignment.md`).

## Target architecture

### Java runtime

Spring Boot 3 + Spring Cloud AWS v3, using `@SqsListener` for SQS
consumption. Chosen over Quarkus / Micronaut / plain AWS SDK for:

- mature SQS + S3 integration,
- built-in visibility-timeout handling, retry, DLQ support,
- FOP usable as an in-process library (no subprocess),
- first-class `WebClient` for REST calls to Django.

Compatible with **ElasticMQ** locally via
`spring.cloud.aws.sqs.endpoint=${SQS_ENDPOINT_URL}` and dummy credentials —
identical dev UX to today.

### Component layout

```
pdf-export-service/src/main/java/net/koalix/pdf/
├── PdfExportApplication.java
├── config/                          # @ConfigurationProperties, WebClient, FopFactory beans
├── sqs/
│   ├── PdfExportCommand.java        # record, mirrors the JSON envelope
│   └── PdfExportListener.java       # @SqsListener → orchestrator
├── orchestrator/
│   └── PdfExportOrchestrator.java
├── api/                             # (re-exports from app_api_java)
├── xml/
│   ├── XmlBuilder.java              # interface Element build(T dto)
│   ├── XmlAggregator.java
│   └── builders/
│       ├── InvoiceXmlBuilder.java
│       ├── QuoteXmlBuilder.java
│       ├── DeliveryNoteXmlBuilder.java
│       ├── PurchaseOrderXmlBuilder.java
│       ├── PurchaseConfirmationXmlBuilder.java
│       ├── PaymentReminderXmlBuilder.java
│       ├── CreditNoteXmlBuilder.java
│       ├── DocumentTemplateXmlBuilder.java
│       └── UserExtensionXmlBuilder.java
├── template/
│   └── TemplateFetcher.java
├── render/
│   └── FopRenderer.java
├── storage/
│   └── S3PdfUploader.java
└── status/
    └── StatusReporter.java
```

XML is emitted via **StAX (`XMLStreamWriter`)**, one builder per DTO type.
Adding a new commercial document type = one new `XmlBuilder<T>` + its
registration.

### Modules / repo layout

```
app_api_java/                      # new Gradle module
├── build.gradle.kts
└── src/main/java/net/koalix/api/
    ├── CrmApiClient.java
    ├── OidcTokenProvider.java
    └── dto/                       # records mirroring Django serializers

pdf-export-service/                # new Gradle module, depends on app_api_java
├── build.gradle.kts
├── Dockerfile                     # multi-stage: gradle build → JRE runtime
└── src/...

docker/
├── dev/
│   ├── Dockerfile.django          (unchanged)
│   └── Dockerfile.pdf-service     (new; thin, just runs the jar)
├── prod/
│   ├── Dockerfile.django          (unchanged)
│   └── Dockerfile.pdf-service     (new)
└── requirements/
    ├── django.txt                 (unchanged)
    └── test.txt                   (unchanged)
    # celery.txt deleted
```

### New Django REST endpoints (JSON only)

| Method & Path | Purpose |
| --- | --- |
| `GET /api/pdf-export-processes/{id}/` | Read process state (source_model/id, template_set, triggered_by) |
| `PATCH /api/pdf-export-processes/{id}/` | Update `status`, `result_url`, `error_message` |
| `GET /api/document-templates/{id}/` | Metadata of the template |
| `GET /api/document-templates/{id}/xsl/` | 302 → presigned S3 URL for the XSL file |
| `GET /api/document-templates/{id}/fop-config/` | 302 → presigned S3 URL for the FOP config |
| `GET /api/document-templates/{id}/logo/` | 302 → presigned S3 URL for the logo |
| `GET /api/invoices/{id}/`, `/quotations/{id}/`, … | Fully-nested JSON tree (contact, addresses, items, taxes, currency, user-extension, company) — the worker builds XML from this |
| `GET /api/user-extensions/{id}/` | The user-extension aggregate used in the XSL-FO |
| `POST /api/commercial-document-media/` | Create the media row after upload |

No XML is served by Django. If any XML renderers or serializers exist today
(e.g. `XSLFORenderer`), they are removed as part of this migration.

### Auth

Reuse the existing OIDC client-credentials flow (`koalixcrm/shared/api_client.py`
on the Python side). Java mirror: `OidcTokenProvider` fetches a token from the
OIDC token endpoint, caches until `exp - 30s`, attaches
`Authorization: Bearer …` on every `WebClient` call.

### Dataflow

```
Admin "create_pdf_async"
    → Django creates PDFExportProcess (pending) + SendMessage to SQS
        → Java @SqsListener receives PDFExportCommand
            → GET /api/pdf-export-processes/{id}/       (context)
            → GET /api/<model>/{id}/                    (deeply nested JSON)
            → GET /api/document-templates/{id}/         (metadata)
            → GET /api/document-templates/{id}/xsl/     (302 → S3)
            → GET /api/document-templates/{id}/fop-config/ (302 → S3)
            → GET /api/document-templates/{id}/logo/    (302 → S3)
            → build XML (StAX, per-DTO builders, aggregate)
            → FOP library: XSL-FO + XSL → PDF (bytes)
            → PUT s3://S3_PDF_BUCKET/pdf-exports/<model>_<id>_<pid>.pdf
            → POST /api/commercial-document-media/
            → PATCH /api/pdf-export-processes/{id}/ status=completed
```

Failure handling: Spring Retry with exponential backoff, max 3 attempts; on
terminal failure the listener moves the message to the configured DLQ and we
PATCH `status=failed` with `error_message`.

## Staged rollout

Each stage is a separate PR on top of the previous:

1. **Django JSON-only API additions**
   Add the ViewSets, nested JSON serializers, and presigned-URL detail actions
   listed above. No behaviour change to existing code.
   *Exit criteria:* OpenAPI schema shows new endpoints; Django test suite
   green; existing Python worker still functions.

2. **`app_api_java` skeleton**
   Gradle module, DTO records, `CrmApiClient`, `OidcTokenProvider`, WireMock
   unit tests for each endpoint.
   *Exit criteria:* `./gradlew :app_api_java:test` green.

3. **`pdf-export-service`**
   Orchestrator, `XmlBuilder<T>` per DTO, `XmlAggregator`, `TemplateFetcher`,
   `FopRenderer`, `S3PdfUploader`, `StatusReporter`. Integration test uses
   LocalStack (SQS + S3) and a dockerised Django.
   *Exit criteria:* integration test renders an Invoice end-to-end and diffs
   equal against a golden PDF produced by the current Python worker (byte-wise
   after deterministic-date patching, or structurally via PDFBox text-extract).

4. **Docker & compose wiring**
   Add `docker/{dev,prod}/Dockerfile.pdf-service`. Update `docker-compose.yml`
   to replace the `celery` service with `pdf-service`. Adjust `.github/workflows`:
   rename `docker-celery.yml` to `docker-pdf-service.yml`, build the jar and
   image in CI.
   *Exit criteria:* `docker compose up` runs the full stack locally against
   ElasticMQ + MinIO and an Invoice PDF round-trips successfully.

5. **Delete legacy code**
   Remove `koalixcrm_microservices/`, `koalixcrm_mq_commands/`,
   `koalixcrm/core/documents/pdf_export.py`, every `create_pdf(...)` /
   `serialize_to_xml()` on the Django models, `core/views/renderer.py`,
   `docker/requirements/celery.txt`, `docker/**/Dockerfile.celery`.
   *Exit criteria:* `grep -R "serialize_to_xml\|create_pdf\|XSLFORenderer" koalixcrm/`
   returns no matches; Django test suite green.

6. **Documentation**
   Update `doc/pdf_creation_service/` (context, architecture, sequence, state
   machine, interfaces) to reflect the Java service and REST-only boundary.
   Update `README.md` and relevant setup guides.

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| XML output differs subtly from today → PDFs change | Stage 3 golden-PDF diff; keep old Python worker running on `develop` until stage 5 lands |
| OIDC token flow misconfigured for the Java client | Reuse `.env` keys already used by Python `api_client`; integration test covers token refresh |
| FOP fonts / image resolution differ between subprocess and library mode | Use the same `fop.xconf` the subprocess used; configure `FopFactory` with the same base URI |
| ElasticMQ queue-URL mismatch in dev | Keep `elasticmq.conf` as-is; configure `spring.cloud.aws.sqs.endpoint` via env |
| Prod `Dockerfile.celery` was missing FOP/JRE anyway | New Java image has JRE bundled; issue disappears |
| Unrelated `develop` changes complicate the rebase | Stages land as small PRs onto `develop`; rebase early and often |

## Configuration & environment

All existing env vars stay in place, plus Spring Cloud AWS equivalents:

| Concern | Env var |
| --- | --- |
| SQS queue name | `KOALIXCRM_MICROSERVICE_SQS` (unchanged, read as `spring.cloud.aws.sqs.listener.queue-names`) |
| SQS endpoint (ElasticMQ) | `SQS_ENDPOINT_URL` → `SPRING_CLOUD_AWS_SQS_ENDPOINT` |
| S3 endpoint (MinIO) | `S3_ENDPOINT_URL` → `SPRING_CLOUD_AWS_S3_ENDPOINT` |
| PDF bucket | `S3_PDF_BUCKET` (unchanged) |
| AWS region | `AWS_REGION` → `SPRING_CLOUD_AWS_REGION_STATIC` |
| koalixCRM base URL | new: `KOALIXCRM_API_BASE_URL` |
| OIDC token URL / client id / client secret | reuse the names already used by Python client |

No `FOP_EXECUTABLE`, no `DJANGO_SETTINGS_MODULE`, no DB credentials on the
worker after this migration.

## Decisions recorded

- **Runtime:** Spring Boot 3 + Spring Cloud AWS v3 `@SqsListener`.
- **XML:** StAX, per-DTO `XmlBuilder<T>`, aggregated in the worker.
- **API boundary:** Django is JSON-only; all XML concerns live in the worker.
- **Sync PDF path:** deleted (option A).
- **Auth:** OIDC M2M client credentials, reusing the established flow.
- **Template assets:** served as 302 to presigned S3 URLs.
- **Dev loop:** same `docker-compose` with ElasticMQ + MinIO; `celery`
  container swapped for `pdf-service` container.
- **API client library:** hand-written `app_api_java` (switch to OpenAPI
  generator if/when a second Java consumer appears).

## Where we are right now

Branch: `refactor/pdf-service-java-migration` on *both* `koalixcrm` and
`koalixcrm_system` (each has its own commits, no push yet).

Landed commits on `koalixcrm`:

| Commit | Subject |
| --- | --- |
| `5b7c2fa` | docs: plan Python/Celery → Java/Spring Boot PDF-service migration (#386) |
| `d636069` | docs(pdf-service): add migration reference, DTO sketches, envelope contract (#386) |
| `c8bf7bc` | feat(pdf-service): implement stages 1-4 of Python/Celery → Java migration (#386) |
| *pending* | fix(pdf-service): declare URISyntaxException in S3PdfUploader |

Landed commits on `koalixcrm_system`:

| Commit | Subject |
| --- | --- |
| `5b70569` | feat: swap Celery worker for Java pdf-service in compose (koalixcrm#386) |

Stage status (see also
[`doc/pdf_creation_service/20-java-implementation.md`](./doc/pdf_creation_service/20-java-implementation.md)):

| Stage | Status |
| --- | --- |
| 1 — Django JSON-only API additions | ✅ committed |
| 2 — `app_api_java` Gradle module | ✅ committed |
| 3 — `pdf-export-service` Spring Boot | ✅ committed (golden-PDF diff explicitly skipped by user) |
| 4 — Docker & compose wiring | ✅ committed (koalixcrm + koalixcrm_system) |
| 5 — Delete legacy Python worker code | ⏳ pending — destructive, deliberately held |
| 6 — Refresh architecture docs | ⏳ pending — diagrams still describe the Python worker |

## Planned next steps

Execute in order. Each step is a small commit on the same branch unless noted.

### 1. Verify the `pdf-service` image builds end-to-end
```
cd /app/koalixcrm_system
docker compose --env-file .env.aaron --profile dev build pdf-service
```
Expected: Gradle build succeeds after the `URISyntaxException` fix.
Likely follow-up issues to fix as they surface:
- `LiveReload`/Jackson-datatype classpath drift (record reflection).
- Spring Cloud AWS auto-config needing `spring.cloud.aws.credentials.type: static` when
  endpoint is MinIO — revisit `application.yaml` if the S3 client can't resolve credentials.
- `FopFactory.newInstance(new File(".").toURI())` is probably too permissive — point it
  at a packaged `fop.xconf` inside the jar once templates are finalised.

### 2. Local round-trip: create one PDF through the admin
Assumes dev stack up with `--profile dev up`.
1. Create a superuser: `docker compose exec backend python manage.py createsuperuser`.
2. Log into `http://localhost:8000/admin/`, set up one `UserExtension`,
   one `DocumentTemplate` (upload a minimal XSL + fop.xconf), one
   `Customer` + `Contract` + `Invoice` + positions.
3. Run the admin action **Create PDF async** on the invoice.
4. Tail `docker compose logs -f pdf-service` — expect:
   - `@SqsListener` receives the `PDFExportCommand` envelope,
   - `CrmApiClient` fetches `/pdf_export_processes/{id}/`,
     `/invoices/{id}/nested/`, `/document_templates/{id}/`,
     `/user_extensions/{id}/`,
   - FOP renders to `s3://koalixcrm-pdf-exports/pdf-exports/Invoice_<id>_<pid>.pdf`,
   - `POST /commercial_document_media/` and `PATCH /pdf_export_processes/{id}/ status=completed`.
5. Verify in MinIO console (`http://localhost:9011`) that the PDF landed
   and opens in a viewer.

### 3. Fix the local-dev auth gap ⚠️ blocking a green round-trip
The Java `OidcTokenProvider` unconditionally calls the OIDC discovery
endpoint. Local dev has no Keycloak (per ADR). The Python
`api_client.py` falls back to sending only the
`X-Custom-Origin-Verify` header when OIDC is not configured.

To unblock:
- Add an `AuthMode` enum to `app_api_java` (`OIDC`, `ORIGIN_KEY`).
- When `CELERY_WORKER_M2M_OIDC_ISSUER` is blank, construct
  `CrmApiClient` without an `OidcTokenProvider`; skip the
  `Authorization: Bearer …` header; always send `X-Custom-Origin-Verify`.
- Mirror this in Django: `koalixcrm/auth/m2m_authentication.py` must
  accept origin-key auth when OIDC is disabled (check the existing
  middleware — it probably already does this for the Python client).

### 4. XSL template reconciliation
`XmlAggregator` emits a clean but new shape. The stylesheets currently
in the MinIO templates bucket expect the old `lxml` output. Options:

1. Re-author the XSL templates against the new structure (preferred).
   One template per commercial-document type; shared includes for
   `postal_address`, `position`, `tax_summary`.
2. Reshape the Java XML to match the old lxml structure. Requires
   capturing a reference sample from a still-running Python worker
   (dev only; the production worker is being removed).

Recommend option 1 + a one-off golden-PDF capture now that the
Java service can reach end-of-pipeline.

### 5. Stage 5 — delete the legacy Python worker
Strict checklist in
[`doc/pdf_creation_service/10-migration-reference.md`](./doc/pdf_creation_service/10-migration-reference.md#deletion-checklist-for-stage-5).
Only execute after step 2 proves a green round-trip. Concretely:

```
rm -rf koalixcrm_microservices/ koalixcrm_mq_commands/
rm koalixcrm/core/documents/pdf_export.py koalixcrm/core/views/renderer.py \
   koalixcrm/core/views/pdfexport.py
# edit: drop serialize_to_xml + create_pdf + sync create_pdf admin action
rm docker/requirements/celery.txt docker/dev/Dockerfile.celery docker/prod/Dockerfile.celery
rm .github/workflows/docker-celery.yml
```
Plus in `koalixcrm_system`: remove the `celery` service block and the
`legacy-celery` profile bookkeeping added by commit `5b70569`.

### 6. Stage 6 — refresh architecture docs
Rewrite `doc/pdf_creation_service/{01-context,02-architecture,03-use-case-flow,05-interfaces}.md`
against the Java service. `04-state-machine.md` stays valid.

### 7. Open PRs
Two PRs, one per repo, cross-linking each other and linking issue
`KoalixSwitzerland/koalixcrm#386`:

- `KoalixSwitzerland/koalixcrm#<new>` — branch
  `refactor/pdf-service-java-migration`, three commits so far plus the
  S3 fix.
- `KoalixSwitzerland/koalixcrm_system#<new>` — branch
  `refactor/pdf-service-java-migration`, one commit so far.

Both still need pushing — no `git push` has happened yet.

## Parking lot (nice-to-have, not required to ship)

- Package the Gradle wrapper (`./gradlew`) so CI doesn't need the
  `gradle:jdk21-alpine` base image.
- Split `app_api_java` into per-domain clients (contracts, core,
  user-extensions) once a second Java consumer needs a subset.
- Replace hand-rolled DTOs with OpenAPI-generated records when the
  Django endpoints publish a schema.
- Add a `/actuator/health` probe and wire it into the compose healthcheck.
