# Java implementation — stage 1–4 snapshot

Implementation progress against `CELERY_TO_JAVA_MIGRATION.md`. This file
mirrors what actually landed on the `refactor/pdf-service-java-migration`
branch (vs. what was *planned*); update as stages continue.

## Stage 1 — Django JSON-only API additions ✅

New ViewSets wired into `projectsettings/urls.py`:

| Route | ViewSet | Notes |
| --- | --- | --- |
| `GET /pdf_export_processes/{id}/`, `PATCH` | `koalixcrm/core/views/pdf_export_process_view_set.py` | Retrieve + partial update only. Source fields read-only; only `status`, `result_url`, `error_message` are writable. |
| `GET /document_templates/{id}/` | `koalixcrm/djangoUserExtension/views/document_template_view_set.py` | Returns `xsl_href`, `fop_config_href`, `logo_href` sub-resources. |
| `GET /document_templates/{id}/xsl/` → 302 | same ViewSet detail action | Redirects to a short-lived presigned S3 URL via `koalixcrm_utils/presigned_urls.py`. |
| `GET /document_templates/{id}/fop-config/` → 302 | same ViewSet | Ditto; 404 when optional asset absent. |
| `GET /document_templates/{id}/logo/` → 302 | same ViewSet | Ditto. |
| `POST /commercial_document_media/` | `koalixcrm/contracts/views/commercial_document_media_view_set.py` | GET+POST only; created by the worker after upload. |
| `GET /user_extensions/{id}/` | `koalixcrm/djangoUserExtension/views/user_extension_view_set.py` | Nested JSON with user, currency and UserExtension addresses. |
| `GET /invoices/{id}/nested/` (and 5 siblings) | Existing `*ViewSet` + `NestedDetailMixin` | Detail action that returns the deeply-nested shape defined in `11-dto-shapes.md`. |

Nested serializer file (all commercial-document subclasses share a base):
`koalixcrm/contracts/serializers/nested_commercial_document.py`.

Tax-summary aggregation is computed on the fly inside
`_compute_tax_summary(...)` in that file — positions grouped by tax rate.

## Stage 2 — `app_api_java` Gradle module ✅

```
app_api_java/
├── build.gradle.kts                             # Java 21, Spring WebFlux + Jackson
├── README.md
└── src/
    ├── main/java/net/koalix/api/
    │   ├── CrmApiClient.java                    # WebClient façade, one method per endpoint
    │   ├── OidcTokenProvider.java               # discovery + client_credentials + cache
    │   └── dto/*.java                           # records mirroring Django JSON shapes
    └── test/java/net/koalix/api/
        └── CrmApiClientTest.java                # WireMock coverage: GET/PATCH/POST + 401 retry
```

DTOs are `record`s with Jackson `SNAKE_CASE` naming strategy so that
`sourceModel` ↔ `source_model` mapping is automatic.

## Stage 3 — `pdf-export-service` Spring Boot module ✅ (golden-PDF test skipped)

```
pdf-export-service/
├── build.gradle.kts                             # Spring Boot 3.3 + Spring Cloud AWS v3 + FOP 2.9
└── src/main/java/net/koalix/pdf/
    ├── PdfExportApplication.java                # @SpringBootApplication + @EnableRetry
    ├── config/{AppProperties, Beans}.java       # typed config, OIDC + WebClient + FOP beans
    ├── sqs/
    │   ├── PdfExportCommand.java                # wire contract mirror (5 fields, snake_case)
    │   ├── PdfExportEnvelope.java
    │   └── PdfExportListener.java               # @SqsListener, drops unknown envelope types
    ├── orchestrator/PdfExportOrchestrator.java  # Retryable: 3 attempts, expo backoff 1→30 s
    ├── template/{TemplateAssets, TemplateFetcher}.java
    ├── render/FopRenderer.java                  # in-process FOP (no subprocess)
    ├── storage/S3PdfUploader.java               # key = pdf-exports/<model>_<id>_<pid>.pdf
    └── xml/
        ├── XmlBuilder.java (SPI)
        ├── XmlAggregator.java                    # <koalixcrm-export> root
        ├── XmlWriteSupport.java
        └── builders/{Contact,Position,CommercialDocument,UserExtension}XmlBuilder.java
```

**Known gap:** the XML shape emitted by the StAX builders is a reasonable
approximation but has *not* been diffed against the output the Python worker
was producing (user explicitly skipped the golden-PDF capture). Before the
first production run the XSL stylesheets in the templates bucket must be
reviewed against `XmlAggregator.build(...)` output and adjusted if needed.

## Stage 4 — Docker & CI ✅ (partial)

* `docker/dev/Dockerfile.pdf-service` + `docker/prod/Dockerfile.pdf-service` —
  Gradle build → Temurin 21 JRE runtime.
* `.github/workflows/docker-pdf-service.yml` — same structure as `docker-celery.yml`
  (BuildKit, cosign sign, dev-tag handling).
* `docker-compose.yml` lives in the sibling repo `koalixcrm_system`, not here —
  the swap (`celery` → `pdf-service`) is a follow-up commit in that repo.

## Stage 5 — Legacy deletion ⏳ (pending)

Checklist in [`10-migration-reference.md`](./10-migration-reference.md#deletion-checklist-for-stage-5).
Holding until the Java service is verified end-to-end against a real Django.

## Stage 6 — Architecture docs ⏳ (in progress, this file is part of it)

The baseline diagrams (`01-context.md`, `02-architecture.md`,
`03-use-case-flow.md`, `04-state-machine.md`, `05-interfaces.md`) still
describe the Python/Celery implementation. They will be refreshed in the
final migration PR once the Java service runs in CI.
