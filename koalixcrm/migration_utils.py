"""
Utility migration operations for handling the monolithic-to-split-app transition.

These operations make migrations work for BOTH:
- Fresh installs (no existing DB) -> tables get created normally
- Upgrades from old monolithic CRM -> tables already exist, skip creation
"""

from django.db import migrations


class CreateModelIfNotExists(migrations.CreateModel):
    """
    Like CreateModel, but skips the database CREATE TABLE if the table
    already exists. State is always updated regardless.

    This handles the case where the old monolithic app already created
    the table, so we just need Django to know about it in the new app.
    """

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.name)
        table_name = model._meta.db_table
        existing_tables = schema_editor.connection.introspection.table_names()
        if table_name not in existing_tables:
            super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.name)
        table_name = model._meta.db_table
        existing_tables = schema_editor.connection.introspection.table_names()
        if table_name in existing_tables:
            super().database_backwards(app_label, schema_editor, from_state, to_state)


class AddFieldIfNotExists(migrations.AddField):
    """
    Like AddField, but skips the database ALTER TABLE if the column
    already exists on the table.
    """

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        table_name = model._meta.db_table
        columns = [
            col.name
            for col in schema_editor.connection.introspection.get_table_description(
                schema_editor.connection.cursor(), table_name
            )
        ]
        field = model._meta.get_field(self.name)
        column_name = field.column  # handles FK _id suffix etc.
        if column_name not in columns:
            super().database_forwards(app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model_name)
        table_name = model._meta.db_table
        columns = [
            col.name
            for col in schema_editor.connection.introspection.get_table_description(
                schema_editor.connection.cursor(), table_name
            )
        ]
        field = model._meta.get_field(self.name)
        column_name = field.column
        if column_name in columns:
            super().database_backwards(app_label, schema_editor, from_state, to_state)


def cleanup_legacy_migrations(apps, schema_editor):
    """
    Remove old migration records from the monolithic app era.

    This runs once as the very first migration operation. It clears out
    the old migration history so Django doesn't see inconsistencies
    between old app-scoped records and new app-scoped migrations.
    """
    MigrationRecorder = apps.get_model('django', 'Migration') if False else None

    # We can't use the ORM here because the Migration model isn't in
    # INSTALLED_APPS. Use raw SQL instead.
    cursor = schema_editor.connection.cursor()

    # Check if django_migrations table exists (fresh install won't have it
    # populated with old records)
    cursor.execute(
        "SELECT COUNT(*) FROM django_migrations WHERE app = 'crm' AND name = '0002_auto_20170927_2042'"
    )
    is_upgrade = cursor.fetchone()[0] > 0

    if not is_upgrade:
        return  # Fresh install, nothing to clean up

    # Remove ALL old migration records for apps that have been restructured.
    # The new migrations will re-record themselves as they run.
    old_apps = [
        'accounting',
        'crm',
        'djangoUserExtension',
        'subscriptions',
    ]
    for app in old_apps:
        cursor.execute("DELETE FROM django_migrations WHERE app = %s", [app])

    # Also remove any records for apps that didn't exist before
    # (contract_object_management, products, reporting) - just in case
    new_only_apps = [
        'contract_object_management',
        'products',
        'reporting',
    ]
    for app in new_only_apps:
        cursor.execute("DELETE FROM django_migrations WHERE app = %s", [app])
