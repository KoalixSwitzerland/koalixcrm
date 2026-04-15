# Welcome to the koalixcrm 
## Why koalixcrm
<table><tr><th>Values:</th><th>Features:</th></tr>
<tr><td><ul>
 <li><b>Free and open</b></li>
 <li>REST interface to many entities </li>
 <li>Open source </li>
 <li>BSD license </li>
<li>Simple and beautiful user interface </li>
<li>High quality output documents </li>
<li>Small business <10 employees with access </li>
                       <li>Cloud hosted, Self-hosted, Not hosted (single-user, offline)</li></ul></td>
<td><ul>
<li> Manage Contacts, Leads, Persons</li>
<li> Manage Products and Prices</li>
<li> Manage Documents such as Invoices, Quotes, Purchase Orders, ...</li>
<li> Manage Projects, Tasks, Work (Traditional project management)</li>
<li> Manage Document Tempaltes</li>
<li>Double Entry Accounting</li>
<li> Create Project Reports</li>
<li> Adjust Access Rights </li></ul></td>
  </tr></table>

## Quality badges on master
| Project build: | Codacy results: |Docker: | Social Networks: |
| --- | --- | --- | --- |
| [![Django CI](https://github.com/KoalixSwitzerland/koalixcrm/actions/workflows/django.yml/badge.svg)](https://github.com/KoalixSwitzerland/koalixcrm/actions/workflows/django.yml) | [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cfae578b5c174f438786c935fa425002)](https://app.codacy.com/gh/KoalixSwitzerland/koalixcrm/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) </br> [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/cfae578b5c174f438786c935fa425002)](https://app.codacy.com/gh/KoalixSwitzerland/koalixcrm/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)| [![Docker Automated build](https://img.shields.io/docker/automated/koalixswitzerland/koalixcrm.svg)]() <br/> [![Docker Stars](https://img.shields.io/docker/stars/koalixswitzerland/koalixcrm.svg)]() [![Docker Pulls](https://img.shields.io/docker/pulls/koalixswitzerland/koalixcrm.svg)]() | [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/koalix-crm/Lobby) |


## Documentation
You can find the documentation of koalixcrm here: [doc](http://readthedocs.org/docs/koalixcrm/en/master/)

## Installation
Some information about the installation of koalixcrm: [installation](https://github.com/scaphilo/koalixcrm/wiki/Installation)

## Development environment setup
To set up the development environment for KoalixCRM, you can use Docker with the following commands:

docker-compose pull
docker-compose up

To run the application, use:

docker compose run --service-ports web python manage.py runserver 0.0.0.0:8000 --settings=projectsettings.settings.development_docker_sqlite_settings.py

## Release Process
Information about the release process: [Release Process](https://github.com/scaphilo/koalixcrm/wiki/Release-Process)

## Upgrade from 1.14.0 to v2.0.0

v2.0.0 is a major release that restructures the monolithic `crm` app into independent Django apps:

| New app | Moved from | Contains |
| --- | --- | --- |
| `accounting` | `accounting` (unchanged) | Account, AccountingPeriod, Booking, ProductCategory |
| `contract_object_management` | `crm` | Contract, SalesDocument, Invoice, Quote, DeliveryNote, Position, ... |
| `products` | `crm` | Currency, ProductType, Product, Tax, Unit, Price, ... |
| `reporting` | `crm` | Project, Task, Work, ReportingPeriod, Agreement, Estimation, Resource, ... |
| `crm` | `crm` (reduced) | Contact, Customer, Supplier, Person, Call, EmailAddress, PhoneAddress, PostalAddress, ... |
| `djangoUserExtension` | `djangoUserExtension` (unchanged) | DocumentTemplate, TemplateSet, UserExtension, ... |
| `subscriptions` | `subscriptions` (unchanged) | Subscription, SubscriptionEvent, SubscriptionType |

All database table names remain unchanged (`crm_*` prefix) to preserve data compatibility.

### Migration steps (PostgreSQL dump to v2.0.0)

The upgrade requires three steps. Make sure you have a backup of your database before starting.

**Prerequisites:**
- A PostgreSQL dump from 1.14.0 (e.g. `auftraegekoalixnet_20230101.sql`)
- The v2.0.0 codebase checked out
- Python virtualenv activated

**Step 1 -- Convert PostgreSQL dump to SQLite:**

```bash
python koalixcrm_utils/pg2sqlite.py your_dump.sql projectsettings/db.sqlite3
```

**Step 2 -- Extract legacy data and prepare for migration:**

```bash
python koalixcrm_utils/pre_migrate_cleanup.py
```

This detects the legacy database, extracts all data to `projectsettings/legacy_data.json`,
and drops all tables so Django can recreate them with proper schemas.

**Step 3 -- Run Django migrations to create the new schema:**

```bash
python manage.py migrate --settings=projectsettings.settings.development_docker_sqlite_settings
```

**Step 4 -- Import legacy data into the new schema:**

```bash
python koalixcrm_utils/pre_migrate_cleanup.py projectsettings/db.sqlite3 projectsettings/legacy_data.json import
```

This imports all data back, automatically handling:
- Columns removed in v2.0.0 (e.g. `originalAmount` in Account) are skipped
- Tables Django manages itself (`django_migrations`, `auth_permission`, `django_content_type`) are skipped
- Foreign key relationships are preserved (all tables keep their original `crm_*` names)

### Fresh install (no existing data)

For a fresh v2.0.0 install without existing data, simply run:

```bash
python manage.py migrate --settings=projectsettings.settings.development_docker_sqlite_settings
python manage.py createsuperuser --settings=projectsettings.settings.development_docker_sqlite_settings
```

### Migration utilities reference

| File | Purpose |
| --- | --- |
| `koalixcrm_utils/pg2sqlite.py` | Converts a PostgreSQL dump file to SQLite3 |
| `koalixcrm_utils/pre_migrate_cleanup.py` | Handles legacy data extraction, table cleanup, and data re-import |
| `koalixcrm/migration_utils.py` | `CreateModelIfNotExists` and `AddFieldIfNotExists` -- migration operations that skip table/column creation when they already exist, allowing the same migrations to work for both fresh installs and upgrades |

## Update from version 1.12 to 1.14
Some information about the update procedure from Version 1.12 to Version 1.14: [update](https://github.com/scaphilo/koalixcrm/wiki/Update) 
