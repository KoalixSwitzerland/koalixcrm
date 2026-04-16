# Linux server install (VPS / VPC)

How to bring up KoalixCRM on a headless Linux host using native Docker,
and pick a UI language. This page only covers **start the app** — see
[configuration guide](./configuration.md) *(coming soon)* for admin /
user setup, OIDC, storage, backups, TLS, etc.

> The compose file currently provided runs the **dev profile** (Django
> `runserver`, `DEBUG=True`). It is suitable for demos, evaluation and
> single-user self-hosting. A hardened production profile (Gunicorn,
> Postgres, TLS, etc.) is not yet part of this repo — track it in the
> configuration guide when it lands.

---

## Prerequisites

- A Linux host (Debian/Ubuntu tested) reachable by SSH
- **Docker Engine** + **Docker Compose plugin** installed
  (`docker --version`, `docker compose version`)
- Git
- ~5 GB free disk space
- Inbound TCP `8000` (or whatever `DJANGO_PORT` you pick) open in the
  VPC/firewall if you want to reach it from outside

All stack orchestration lives in the sibling repo **`koalixcrm_system`**
— you need both repos checked out side-by-side, plus a small data
directory for the SQLite DB and secrets.

---

## 1. Clone the repos

```bash
mkdir -p ~/koalix && cd ~/koalix

git clone https://github.com/KoalixSwitzerland/koalixcrm.git
git clone https://github.com/KoalixSwitzerland/koalixcrm_system.git
mkdir -p koalixcrm_data/db
```

Resulting layout:

```
~/koalix/
├── koalixcrm/          # application source
├── koalixcrm_system/   # docker-compose and infra config
└── koalixcrm_data/
    ├── db/             # SQLite lives here
    └── secrets.env     # created in step 2
```

---

## 2. Create environment files

```bash
cd ~/koalix/koalixcrm_system
cp .env.example .env.server
cp docker/secrets.env.example ../koalixcrm_data/secrets.env
```

Edit `.env.server` — absolute Linux paths, no daemon-side overrides
needed (shell and Docker daemon see the same filesystem):

```bash
KOALIXCRM_DIR=/home/ubuntu/koalix/koalixcrm
KOALIXCRM_DB_DIR=/home/ubuntu/koalix/koalixcrm_data
KOALIXCRM_SYSTEM_DIR=/home/ubuntu/koalix/koalixcrm_system

# Optional: pick a UI language for the whole instance
# KOALIXCRM_LANGUAGE_CODE=de

# Optional: bind Django to a non-default port
# DJANGO_PORT=8000
```

Fill in `../koalixcrm_data/secrets.env` with real OIDC values if you use
cloud Keycloak for admin login. For a first smoke test you can leave
the values as `CHANGE_ME` and create a local superuser (step 5).

---

## 3. Start the stack

```bash
docker compose --env-file .env.server --profile dev up -d --build
```

`-d` detaches so the stack keeps running after you log out.

Check logs:

```bash
docker compose --env-file .env.server --profile dev logs -f backend
```

Ready when you see `Starting development server at http://0.0.0.0:8000/`.

---

## 4. Reach the application

From the server:

```bash
curl http://localhost:${DJANGO_PORT:-8000}/admin/
```

From outside, hit `http://<server-ip>:<port>/admin/`. If you are
reverse-proxying (nginx/caddy/traefik) in front of it, add the public
hostname to `ALLOWED_HOSTS` — currently hardcoded in
`docker-compose.yml` under the `backend` service's `environment` block.

---

## 5. Create a local admin user

```bash
cd ~/koalix/koalixcrm_system
docker compose --env-file .env.server --profile dev exec backend \
    python manage.py createsuperuser
```

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

Add to `.env.server`:

```bash
KOALIXCRM_LANGUAGE_CODE=de
```

Restart the stack so the containers pick up the new env:

```bash
docker compose --env-file .env.server --profile dev up -d
```

The env var feeds Django's `LANGUAGE_CODE`; defaults to `en-us` when
unset.

> Translations are compiled from `.po` → `.mo` at image build time.
> After pulling new translations rebuild the backend image:
> `docker compose --env-file .env.server --profile dev build backend`.

---

## Operating the instance

```bash
# tail all logs
docker compose --env-file .env.server --profile dev logs -f

# restart after code update (repo is bind-mounted; usually no rebuild needed)
docker compose --env-file .env.server --profile dev restart backend celery

# stop (keep DB and volumes)
docker compose --env-file .env.server --profile dev down

# stop and wipe docker-managed volumes (MinIO blobs etc.)
docker compose --env-file .env.server --profile dev down -v
```

The SQLite database lives on the host at
`~/koalix/koalixcrm_data/db/db.sqlite3` — back up that file to back up
the instance. MinIO blobs live in the `minio_data` docker volume.

---

## Running on boot

To start automatically on reboot, add a small systemd unit:

```ini
# /etc/systemd/system/koalixcrm.service
[Unit]
Description=KoalixCRM docker compose stack
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/koalix/koalixcrm_system
ExecStart=/usr/bin/docker compose --env-file .env.server --profile dev up -d
ExecStop=/usr/bin/docker compose --env-file .env.server --profile dev down

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now koalixcrm.service
```
