# Local setup with Docker Desktop

How to get the KoalixCRM stack running on your workstation and pick a UI
language. This page only covers **start the app** — see
[configuration guide](./configuration.md) *(coming soon)* for admin/user
setup, OIDC, storage, etc.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  installed and running (Windows, macOS, or Linux)
- Git
- ~5 GB free disk space (images + volumes)

All stack orchestration lives in the sibling repo **`koalixcrm_system`**
— you need both repos checked out side-by-side, plus a small data
directory for the SQLite DB and secrets.

---

## 1. Clone the repos

```bash
mkdir koalix && cd koalix

git clone https://github.com/KoalixSwitzerland/koalixcrm.git
git clone https://github.com/KoalixSwitzerland/koalixcrm_system.git
mkdir -p koalixcrm_data/db
```

Resulting layout:

```
koalix/
├── koalixcrm/          # application source
├── koalixcrm_system/   # docker-compose and infra config
└── koalixcrm_data/
    ├── db/             # SQLite lives here
    └── secrets.env     # created in step 2
```

---

## 2. Create environment files

All docker commands run from `koalixcrm_system/`.

```bash
cd koalixcrm_system
cp .env.example .env.<yourname>                     # e.g. .env.alice
cp docker/secrets.env.example ../koalixcrm_data/secrets.env
```

Open `.env.<yourname>` and set the three absolute paths:

| Host platform | Example |
| --- | --- |
| Linux / macOS | `KOALIXCRM_DIR=/home/alice/koalix/koalixcrm` |
| Native Windows (Docker Desktop) | `KOALIXCRM_DIR=C:/Users/alice/koalix/koalixcrm` |
| WSL2 shell + Docker Desktop on Windows | set both `KOALIXCRM_DIR=/mnt/c/Users/alice/koalix/koalixcrm` (shell) **and** `KOALIXCRM_HOST_DIR=//c/Users/alice/koalix/koalixcrm` (Windows daemon). See inline comments in `.env.example`. |

`secrets.env` contains OIDC credentials for admin login via cloud
Keycloak. For a first local run you can leave the values as
`CHANGE_ME` and create a local superuser instead (step 5).

---

## 3. Start the stack

```bash
docker compose --env-file .env.<yourname> --profile dev up --build
```

The first run pulls images, builds the Django + Celery containers, runs
migrations, and starts:

| Service   | URL / Port                                            |
| --------- | ----------------------------------------------------- |
| Django    | `http://localhost:${DJANGO_PORT:-8000}`               |
| MinIO UI  | `http://localhost:${MINIO_CONSOLE_PORT:-9011}`        |
| ElasticMQ | `http://localhost:${ELASTICMQ_UI_PORT:-9325}`         |

Ready when you see `Starting development server at http://0.0.0.0:8000/`.

---

## 4. Open the application

Navigate to `http://localhost:8000/admin/` (or whatever `DJANGO_PORT`
you set).

---

## 5. Create a local admin user

In a second terminal, from `koalixcrm_system/`:

```bash
docker compose --env-file .env.<yourname> --profile dev exec backend \
    python manage.py createsuperuser
```

Log in at `/admin/`.

---

## 6. Set the UI language

KoalixCRM ships translations for:

| Language            | Code     |
| ------------------- | -------- |
| English (default)   | `en-us`  |
| German              | `de`     |
| French              | `fr`     |
| Spanish             | `es`     |
| Portuguese (Brazil) | `pt-br`  |

Add the language code to your `.env.<yourname>` file in
`koalixcrm_system/`:

```bash
KOALIXCRM_LANGUAGE_CODE=de
```

Then restart the stack to pick up the new value:

```bash
docker compose --env-file .env.<yourname> --profile dev up -d
```

The env var feeds Django's `LANGUAGE_CODE`; defaults to `en-us` when
unset.

> Translations are compiled from `.po` → `.mo` at image build time.
> After pulling new translation changes, rebuild the backend image:
> `docker compose --env-file .env.<yourname> --profile dev build backend`.

---

## Stopping & cleaning up

```bash
# stop (keep volumes)
docker compose --env-file .env.<yourname> --profile dev down

# stop and wipe MinIO / other docker-managed volumes
docker compose --env-file .env.<yourname> --profile dev down -v
```

The SQLite database lives on the host at `koalixcrm_data/db/db.sqlite3`
— delete that file to start with an empty DB next time.
