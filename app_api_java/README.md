# app_api_java

Hand-written Java client library for the koalixCRM REST API. Shared across
the PDF-export service and any future Java consumer of the same endpoints.

Mirrors the role of `koalixcrm/*_api_py` on the Python side: strongly-typed
DTO records plus a thin `CrmApiClient` built on Spring WebClient, with the
OIDC M2M `client_credentials` flow wired into `OidcTokenProvider`.

## Modules produced

| Java type | Purpose |
| --- | --- |
| `net.koalix.api.CrmApiClient` | Typed entry point — one method per endpoint consumed by the PDF worker. |
| `net.koalix.api.OidcTokenProvider` | Fetches & caches access tokens via OIDC discovery + `client_credentials`. |
| `net.koalix.api.dto.*` | Immutable `record` DTOs mirroring the Django JSON shapes. |

## Build

Gradle Kotlin DSL. Publishes to the root Gradle build's composite so that
`pdf-export-service` can depend on it with a simple `implementation(project(":app_api_java"))`.

```
./gradlew :app_api_java:build
./gradlew :app_api_java:test
```

## Environment variables

The client reads its configuration from:

| Env var | Purpose |
| --- | --- |
| `KOALIXCRM_API_URL` | Base URL of the Django API (e.g. `http://backend:8000`). |
| `CELERY_WORKER_M2M_OIDC_ISSUER` | OIDC issuer — discovery endpoint is `${issuer}/.well-known/openid-configuration`. |
| `CELERY_WORKER_M2M_CLIENT_ID` | OIDC client id. |
| `CELERY_WORKER_M2M_CLIENT_SECRET` | OIDC client secret. |
| `CELERY_WORKER_M2M_SCOPE` | Optional scope attached to the token request. |
| `X_CUSTOM_ORIGIN_VERIFICATION_ON` | `"true"`/`"false"` — enables the `X-Custom-Origin-Verify` header. |
| `X_CUSTOM_ORIGIN_VERIFICATION_KEY` | Value for that header when enabled. |

The `CELERY_WORKER_` prefix is preserved (historical reasons / ops parity).
