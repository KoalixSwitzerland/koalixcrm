# Claude Code - Backend Testing Guide

How to run and test `koalixcrm` using the unified docker-compose from the
sibling `koalixcrm-system` repo.

## How Claude runs Docker (read this first)

Claude Code has **no direct Docker access** — the agent container does not mount
`/var/run/docker.sock`. Running `docker` / `docker compose` from the shell will
fail by design. Instead, Claude drives an isolated **`docker` MCP** sidecar that
holds the socket and exposes a narrow set of verbs for allowlisted stacks only.

- Stack key (allowlist): **`koalixcrm-system`**
- The MCP **auto-applies `.env.claude`** — do not pass `--env-file` yourself.
- This stack is **profile-gated**: always pass a `profile`.
- **Integrity gate:** `compose_up` / `compose_run` are refused unless
  `koalixcrm-system/docker-compose.yml` is byte-identical to `origin/main` or
  `origin/develop`. Commit and merge compose changes before running.

> ⚠️ **Never** run the `integration-pdf-service` profile or its
> `integration-pdf-service-runner` service: that service bind-mounts
> `/var/run/docker.sock`, re-introducing the exposure this setup removes. It is
> deliberately excluded from the MCP allowlist.

> The verbs below (`compose_run`, `compose_up`, …) are `docker` MCP tool calls,
> not shell commands.

## Quick Reference (MCP calls)

```
# Unit tests — Django (fast, no services)
compose_run(stack="koalixcrm-system", service="unit-django-runner", profile="unit-django")

# Unit tests — Celery
compose_run(stack="koalixcrm-system", service="unit-celery-runner", profile="unit-celery")

# Unit tests — PDF service
compose_run(stack="koalixcrm-system", service="unit-pdf-service-runner", profile="unit-pdf-service")

# Integration tests (full local infra + cloud Keycloak)
compose_run(stack="koalixcrm-system", service="integration-runner", profile="integration")

# E2E tests (Playwright browser)
compose_run(stack="koalixcrm-system", service="e2e-runner", profile="e2e")

# Local dev (manual testing in browser)
compose_up(stack="koalixcrm-system", profile="dev")

# Inspect / tear down
compose_ps(stack="koalixcrm-system", profile="dev")
compose_logs(stack="koalixcrm-system", service="backend", tail=200)
compose_down(stack="koalixcrm-system", profile="dev", volumes=True)
```

Each runner service has a default command that runs its full suite. To run a
subset, pass an explicit `command` (the container's argv), e.g.
`command=["pytest", "-m", "component", "-v"]`.

## Ports (with `.env.claude`)

Ports are offset from the WFS stack to avoid clashes (see `.env.claude` in
`koalixcrm-system`):

| Service | URL |
|---|---|
| Django app | http://localhost:8010/ |
| MinIO API / Console | http://localhost:9030 / http://localhost:9031 |
| ElasticMQ API / UI | http://localhost:9334 / http://localhost:9335 |
| Allure report | http://localhost:5011/ |

## Environment Files

Each developer maintains their own `.env.<name>` in `koalixcrm-system` (and a
`koalixcrm_data/secrets.env`); see
[`docs/setup-local-docker-desktop.md`](./docs/setup-local-docker-desktop.md) for
the human setup. Humans run `docker compose --env-file .env.<yourname> …`
directly. **Claude does not** — the `docker` MCP is hard-tied to `.env.claude`
and applies it automatically.

## Architecture Notes

- **Socket isolation**: the agent container does **not** mount the Docker socket;
  all compose actions go through the `docker` MCP sidecar (the only socket
  holder), constrained by an allowlist + integrity gate. The
  `integration-pdf-service` profile is excluded because it mounts the socket.
- **Unified docker-compose**: all services are defined in
  `koalixcrm-system/docker-compose.yml`; you need both repos checked out
  side-by-side plus a `koalixcrm_data/` directory.
- **No pre-built images needed**: services use `build:` in compose — images are
  built automatically on first run.
