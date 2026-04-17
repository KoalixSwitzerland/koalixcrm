# Integration Test Concept — `pdf-export-service`

**Status:** initial — this is the first integration-test pass after both
(a) the monolith → microservice split and
(b) the Python/FOP-subprocess → Java/FOP-library migration.

**Expectation:** tests will fail. That is intentional. We keep the scope of this
first pass to one narrow goal: *prove the moving pieces are wired together so
that subsequent fixes have a place to land*.

## Scope

Two independent layers. Each layer is a standalone integration test so a
failure in one doesn't block signal from the other.

```
  ┌──────────────────────────────────────────────────────────────┐
  │  Step 1 — TemplateFetcherIT                                  │
  │  ------------------------------------------------------------│
  │  LocalStack S3  ◀── PUT fixture assets                       │
  │        ▲                                                     │
  │        │  presigned GET                                      │
  │  WireMock (Django)  ◀── TemplateFetcher.fetch()              │
  │        ▲                  (302 Location → presigned URL)     │
  │        │                                                     │
  │  CrmApiClient (real)                                         │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  Step 2 — FopRendererIT                                      │
  │  ------------------------------------------------------------│
  │  XmlAggregator (real) ──▶ <koalixcrm-export> bytes           │
  │                           │                                  │
  │                           ▼                                  │
  │  FopFactory (real)  ◀─ invoice.xsl / quote.xsl / ...  (real) │
  │                           │                                  │
  │                           ▼                                  │
  │                     PDF bytes (≥ %PDF- header)               │
  └──────────────────────────────────────────────────────────────┘
```

What we **deliberately do NOT test** in this first pass:

- `PdfExportListener` ↔ SQS (needs ElasticMQ container; added later).
- `PdfExportOrchestrator` end-to-end (needs full WireMock suite for all 6
  Django endpoints + retry verification; added later).
- OIDC token refresh (needs WireMock `openid-configuration` + `token` stubs).
- Golden-PDF regression. Per owner decision, the Python worker cannot be run
  anymore, so there is no reference output. We intentionally skip byte- and
  visual-diff assertions.

## Step 1 — TemplateFetcherIT

**Goal:** prove that given a `DocumentTemplateDto` containing three hrefs,
`TemplateFetcher.fetch` produces three local files with the expected bytes.

**Fixtures** (`src/test/resources/fixtures/templates/`):

- `invoice.xsl` — copy of `auftraegekoalixnet/.../invoice.xsl`
- `fop.xconf`  — copy of `auftraegekoalixnet/.../fontconfig.xml`
- `logo.jpg`   — copy of `auftraegekoalixnet/.../logo.jpg`

**Infrastructure:**

- Testcontainers `LocalStackContainer` with S3 service.
- `WireMockServer` in-process, random port.

**Flow per test:**

1. `PutObject` each fixture into the LocalStack bucket under
   `templatefiles/<name>` using the real `S3Client` that the service will use.
2. Stub `GET /document_templates/1/xsl/`   → `302 Location: <presigned URL>`.
3. Stub `GET /document_templates/1/fop-config/` → same pattern.
4. Stub `GET /document_templates/1/logo/`  → same pattern.
5. Build a real `CrmApiClient` pointing at WireMock. Inject a
   **stub `OidcTokenProvider`** that returns a fixed string — we do not care
   about OIDC here, only the asset fetch path.
6. Call `templateFetcher.fetch(new DocumentTemplateDto(1L, "test",
   "/document_templates/1/xsl/", ...))`.
7. Assert every returned `Path`:
   - file exists,
   - `Files.size(path) == expectedSize`,
   - for the XSL: first line starts with `<?xml`.

**Negative cases:**

- `fopConfigHref == null` → `assets.fopConfigFile()` is `null`, no request made.
- Django stub for logo returns `404` → `assets.logoFile()` is `null`, `fetch`
  does *not* throw.

**Likely failures we want to surface:**

- `resolvePresignedAssetUrl` doesn't surface the Location header the way
  `ClientResponse` reads it (reactor-netty defaults may auto-follow redirects
  — if so, the exchange never reaches our stub with status 302).
- Presigned-URL path-style vs virtual-host-style mismatch between LocalStack
  and the `S3Utilities.getUrl(...)` call inside `S3PdfUploader` (only relevant
  once we wire upload into the same test; for Step 1 we only read).
- `WebClient.get().bodyToMono(byte[].class)` chokes on chunked responses
  from LocalStack (unlikely but has surprised people before).

## Step 2 — FopRendererIT

**Goal:** prove Apache FOP runs in-process, consumes every real XSL template,
and emits a non-empty PDF byte stream. We do **not** assert visual layout,
page count, or text content.

**Fixtures:**

- `src/test/resources/fixtures/templates/*.xsl` — all 14 real templates.
- `src/test/resources/fixtures/fop/fop.xconf` + `DejaVuSans{,-Bold}.ttf`
  + `dejavusans{,-bold}.xml` — so font embedding works.

**Parameterisation:**
JUnit5 `@ParameterizedTest` over a list of template filenames. For each,

1. Build a `CommercialDocumentDto` + `UserExtensionDto` using the same fixture
   DTOs as `XmlAggregatorTest`. Keep them minimal but non-null for every
   required field.
2. `byte[] xml = aggregator.build(doc, userExt);`
3. `FopFactory fop = FopFactory.newInstance(tempDir.toUri(), fopConfInputStream);`
4. `byte[] pdf = renderer.render(xml, assets);`
5. Assert:
   - `pdf.length > 0`
   - `new String(pdf, 0, 5, StandardCharsets.US_ASCII).equals("%PDF-")`
   - **Soft check (logged, not asserted):** `pdf.length` per template, so we
     can diff this against a future baseline once XSL reconciliation lands.

**XSL reconciliation — where we are:**

The legacy XSL templates in `auftraegekoalixnet/` originally started with
`<xsl:template match="django-objects">`. They assumed the old
Django-serializer output shape. The new `XmlAggregator` emits
`<koalixcrm-export>`.

Reconciliation is split into two tiers:

- **Tier A — root rename.** Done. All 12 commercial-document templates
  now declare `<xsl:template match="/koalixcrm-export">` so the root
  template fires and FOP accepts the produced `<fo:root>`. This is what
  makes `FopRendererIT` green. PDFs are valid but field-level XPaths
  (`object[@model='crm.xxx']/field[@name='yyy']`) still return empty
  strings, so most cells are blank.
- **Tier B — per-template XPath rewrite.** Not done. Each template needs
  its data-lookup XPaths rewritten against the new tree
  (`commercial_document/customer/contact/name`,
  `user_extension/user/first_name`, `.../items/position`, etc.).
  This will surface gaps in the current DTOs — fields the XSL templates
  expect that aren't currently emitted. Known gaps spotted while patching
  Tier A (list is not exhaustive):

  | XSL needs | Today's DTO / builder |
  | --- | --- |
  | `crm.invoice.iteration_number` | not on `CommercialDocumentDto` |
  | `crm.invoice.payable_until` | not on `CommercialDocumentDto` |
  | `djangoUserExtension.documenttemplate.pagefooterleft`/`pagefootermiddle`/`bankingaccountref` | `DocumentTemplateDto` only has `xslHref`/`fopConfigHref`/`logoHref` |
  | `djangoUserExtension.templateset.addresser` | no DTO at all |
  | `crm.textparagraphinsalesdocument` (BS / AS / AT blocks) | not serialised |
  | `filebrowser_directory` + relative logo path | logo is now a local file path under `TemplateAssets.logoFile()` — XSL must read the path differently |

  Expect Tier B to touch: `DocumentTemplateDto`, `CommercialDocumentDto`,
  the corresponding Django REST serialisers, the XML builders, and each
  XSL file once. `FopRendererIT` will stay green throughout and
  additional content-level assertions (text in PDF, page count) can be
  layered on as each template is verified.

**Accounting templates excluded:** `balancesheet.xsl` and
`profitlossstatement.xsl` live on completely different XML roots
(`koalixaccountingbalacesheet`, `koalixaccountingprofitlossstatement`).
They belong to the still-unmigrated accounting export flow and are not
parameterised into `FopRendererIT`.

A separate failure mode to watch for:

- Missing/misconfigured fonts → FOP logs warnings at WARN level, substitutes
  Helvetica. PDF still emits. Not a test failure.
- XSL parse error in one template (syntax error) → `TransformerException`
  → the parameterized row fails. Isolate and fix that template.
- FOP 2.9 strict-validation rejects old `fo:*` attributes that were accepted
  by the old Python FOP → render exception. Log the offending line, mark the
  template for XSL reconciliation.

## Step 3 (planned, not in this pass) — OrchestratorIT

Will compose both layers plus WireMock stubs for the remaining 5 Django
endpoints, exercising `PdfExportOrchestrator.handle(cmd)` as one test. Adds
verification that:

- status PATCH happens twice (`processing` → `completed`).
- `/commercial_document_media/` POST body contains the S3 URL returned by the
  uploader.
- Retry semantics work — 500 on first PATCH is recovered.

Out of scope for the current PR.

## Step 4 (planned) — SqsE2EIT

Container-based end-to-end: ElasticMQ + LocalStack + WireMock, send envelope
to the queue, assert the orchestration completes. Only valuable once Step 3
is green.

## How to run

### Preferred — through `koalixcrm_system` docker-compose

No host JDK required. Two compose profiles, one per test tier:

```bash
cd /app/koalixcrm_system

# Fast unit tests only (*Test classes — no containers, no infra). ~10 s.
docker compose --env-file .env.<you> --profile unit-pdf-service \
  run --rm unit-pdf-service-runner

# Full suite including *IT (Testcontainers LocalStack + WireMock). ~2–3 min
# on first run while the localstack image pulls + LocalStack boots.
docker compose --env-file .env.<you> --profile integration-pdf-service \
  run --rm integration-pdf-service-runner
```

The IT runner bind-mounts `/var/run/docker.sock` so Testcontainers can spawn
sibling containers on the host daemon, and sets
`TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal` so endpoint URLs are
reachable from inside the runner. This is the standard
"Testcontainers-in-Docker" pattern.

To run a single test class or single method, append a gradle invocation:

```bash
docker compose --env-file .env.<you> --profile unit-pdf-service \
  run --rm unit-pdf-service-runner \
  gradle --no-daemon :pdf-export-service:test \
         --tests net.koalix.pdf.xml.XmlAggregatorTest

docker compose --env-file .env.<you> --profile integration-pdf-service \
  run --rm integration-pdf-service-runner \
  gradle --no-daemon :pdf-export-service:test \
         --tests '*FopRendererIT'
```

### Alternative — direct on the host

```bash
cd /app/koalixcrm
gradle :pdf-export-service:test --info
```

(Gradle wrapper is a known gap — see parking lot in
`CELERY_TO_JAVA_MIGRATION.md`.)

### CI

Not wired yet. Deliberately left out so we don't gate main on tests that
are expected to fail until XSL reconciliation lands. The compose entry
point is the bridge we'll promote into CI once the suite is green.

## Definition of done for this first pass

- [ ] `TemplateFetcherIT` compiles and runs to completion locally.
- [ ] `FopRendererIT` compiles, runs to completion, and emits a `%PDF-` blob
      for each template (content intentionally not validated).
- [ ] Fixture files checked in under `src/test/resources/fixtures/`.
- [ ] This concept document committed alongside the tests.
- [ ] Follow-up issues filed for every template that throws at render time
      (these are candidates for the XSL-reconciliation work already queued
      in `CELERY_TO_JAVA_MIGRATION.md` step #4).
