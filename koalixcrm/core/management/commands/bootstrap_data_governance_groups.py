# -*- coding: utf-8 -*-
"""ADR-0024 §2: provision the two Django groups that separate defining the
product vocabulary from entering product data.

`catalog-schema-authors` gets add/change/delete on the schema models listed
in `koalixcrm.shared.governance.SCHEMA_MODELS`. `catalog-data-editors` gets
add/change/delete on every other governed model, and `view` only on the
schema models — enough to see which attributes exist and why a field is
required, not enough to redefine them.

Idempotent: permissions are set to the computed target rather than added to,
so re-running after a model is added or reclassified converges instead of
accumulating. Group *membership* is never touched — who belongs in which
group is an operator decision, not this command's.
"""
from __future__ import annotations

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from koalixcrm.shared.governance import (
    DATA_EDITOR_GROUP,
    SCHEMA_AUTHOR_GROUP,
    instance_models,
    schema_models,
    unknown_schema_entries,
)

_WRITE = ('add', 'change', 'delete')
_READ = ('view',)


def _permissions_for(models, actions) -> list[Permission]:
    permissions: list[Permission] = []
    for model in models:
        content_type = ContentType.objects.get_for_model(model)
        for action in actions:
            codename = f'{action}_{model._meta.model_name}'
            try:
                permissions.append(
                    Permission.objects.get(content_type=content_type, codename=codename)
                )
            except Permission.DoesNotExist:
                # Django creates these in a post-migrate hook; a miss means
                # migrations have not been run, which is worth failing on
                # rather than silently under-granting.
                raise CommandError(
                    f"Permission {codename!r} for {model._meta.label} does not exist — "
                    "run migrations before bootstrapping governance groups."
                )
    return permissions


class Command(BaseCommand):
    help = (
        "Create/refresh the catalog-schema-authors and catalog-data-editors groups "
        "and their model permissions (ADR-0024 §2). Does not change group membership."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Report what would be granted without writing anything.",
        )

    def handle(self, *args, **options):
        stale = unknown_schema_entries()
        if stale:
            raise CommandError(
                f"SCHEMA_MODELS references models that do not exist: {sorted(stale)}. "
                "A rename left a stale entry behind, which would silently drop that "
                "model back into the permissive class."
            )

        schema = schema_models()
        instances = instance_models()

        author_permissions = _permissions_for(schema, _WRITE + _READ)
        editor_permissions = (
            _permissions_for(instances, _WRITE + _READ) + _permissions_for(schema, _READ)
        )

        self.stdout.write(
            f"{SCHEMA_AUTHOR_GROUP}: {len(schema)} schema models, "
            f"{len(author_permissions)} permissions"
        )
        self.stdout.write(
            f"{DATA_EDITOR_GROUP}: {len(instances)} instance models "
            f"(+ view on {len(schema)} schema models), "
            f"{len(editor_permissions)} permissions"
        )

        if options['dry_run']:
            self.stdout.write(self.style.WARNING("--dry-run: nothing written."))
            return

        with transaction.atomic():
            authors, _ = Group.objects.get_or_create(name=SCHEMA_AUTHOR_GROUP)
            editors, _ = Group.objects.get_or_create(name=DATA_EDITOR_GROUP)
            # `set` rather than `add`: re-running after a reclassification must
            # revoke what no longer applies, not leave it behind.
            authors.permissions.set(author_permissions)
            editors.permissions.set(editor_permissions)

        self.stdout.write(self.style.SUCCESS("Governance groups provisioned."))
