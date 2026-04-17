# -*- coding: utf-8 -*-
"""Rename SalesDocument -> CommercialDocument and all satellite models/fields."""

from django.db import migrations
from django.db.migrations.operations.base import Operation


class RenameParentModel(Operation):
    """
    Atomically rename an MTI parent model together with the auto-generated
    ``<parent>_ptr`` fields on every child model.

    Django's built-in ``RenameModel`` crashes for MTI parents because
    ``state.rename_model()`` re-renders child models *during* the rename,
    before ptr field names are updated.  This operation reimplements the
    state change so that ALL mutations (model key, field references, ptr
    names, bases) are applied before the final model reload.
    """

    reduces_to_sql = False
    reversible = True

    def __init__(self, old_name, new_name, child_models):
        self.old_name = old_name
        self.new_name = new_name
        self.child_models = child_models

    def state_forwards(self, app_label, state):
        old_lower = self.old_name.lower()
        new_lower = self.new_name.lower()
        old_ptr = f"{old_lower}_ptr"
        new_ptr = f"{new_lower}_ptr"
        old_key = (app_label, old_lower)
        new_key = (app_label, new_lower)
        old_ref_str = f"{app_label}.{self.old_name}"
        new_ref_str = f"{app_label}.{self.new_name}"
        old_ref_lower = f"{app_label}.{old_lower}"

        to_reload = set()
        to_reload.add(new_key)

        # --- 1. Rename ptr fields on children + update FK targets ----
        for model_key, model_state in state.models.items():
            changed = False
            new_fields = {}
            for field_name, field in model_state.fields.items():
                new_name_f = field_name
                if field_name == old_ptr and model_key != old_key:
                    new_name_f = new_ptr
                    changed = True
                if hasattr(field, "remote_field") and field.remote_field:
                    remote_model = getattr(field.remote_field, "model", None)
                    if isinstance(remote_model, str) and remote_model.lower() == old_ref_lower:
                        field.remote_field.model = new_ref_str
                        changed = True
                if hasattr(field, "to") and isinstance(field.to, str):
                    if field.to.lower() == old_ref_lower:
                        field.to = new_ref_str
                        changed = True
                new_fields[new_name_f] = field
            if changed:
                model_state.fields = new_fields
                to_reload.add(model_key)

        # --- 2. Rename the model key in state -------------------------
        model_state = state.models.pop(old_key)
        model_state.name = self.new_name
        state.models[new_key] = model_state
        if hasattr(state, "_models_cache"):
            state._models_cache.clear()
        to_reload.discard(old_key)
        to_reload.add(new_key)

        # --- 3. Update bases on all models ----------------------------
        for model_state in state.models.values():
            new_bases = []
            bases_changed = False
            for base in model_state.bases:
                if base == old_key:
                    new_bases.append(new_key)
                    bases_changed = True
                elif isinstance(base, str) and base.lower() == old_ref_lower:
                    new_bases.append(new_ref_str)
                    bases_changed = True
                else:
                    new_bases.append(base)
            if bases_changed:
                model_state.bases = tuple(new_bases)
                to_reload.add((model_state.app_label, model_state.name_lower))

        # --- 4. Reload all affected models ----------------------------
        if hasattr(state, "reload_models"):
            state.reload_models(to_reload, delay=True)
        elif hasattr(state, "reload_model"):
            for key in to_reload:
                state.reload_model(*key, delay=True)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass  # DB changes handled by RunSQL / SeparateDatabaseAndState ops

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return f"Rename MTI parent {self.old_name} -> {self.new_name}"

    @property
    def migration_name_fragment(self):
        return f"rename_{self.old_name.lower()}_to_{self.new_name.lower()}"

    def deconstruct(self):
        return (
            self.__class__.__qualname__,
            [],
            {
                "old_name": self.old_name,
                "new_name": self.new_name,
                "child_models": self.child_models,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("contract_object_management", "0003_add_sales_document_media"),
    ]

    operations = [
        # ---------------------------------------------------------------
        # 0. Repair pre-existing broken MTI child schemas.
        #
        # Historical monolithic-crm migrations created child tables
        # (crm_invoice, crm_quote, ...) with the ``salesdocument_ptr_id``
        # column declared as plain ``INTEGER NOT NULL`` -- no PRIMARY KEY
        # and no UNIQUE constraint.  On fresh installs Django creates
        # them correctly, but upgrades from monolithic DBs carry the
        # broken schema.  Without a UNIQUE/PK constraint on the ptr
        # column, any FK that later references it (e.g. ``CreditNote
        # .corrects_invoice`` in 0005) fails SQLite's
        # ``PRAGMA foreign_key_check`` with ``foreign key mismatch``.
        #
        # Adding a ``CREATE UNIQUE INDEX IF NOT EXISTS`` is idempotent:
        # a no-op on fresh DBs (PK already provides uniqueness) and a
        # schema fix on dirty DBs.  SQLite auto-rewrites the index
        # definition when we ``RENAME COLUMN`` below.
        # ---------------------------------------------------------------
        migrations.RunSQL(
            sql=(
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_invoice_ptr_uniq" '
                'ON "crm_invoice" ("salesdocument_ptr_id");\n'
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_quote_ptr_uniq" '
                'ON "crm_quote" ("salesdocument_ptr_id");\n'
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_deliverynote_ptr_uniq" '
                'ON "crm_deliverynote" ("salesdocument_ptr_id");\n'
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_paymentreminder_ptr_uniq" '
                'ON "crm_paymentreminder" ("salesdocument_ptr_id");\n'
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_purchaseorder_ptr_uniq" '
                'ON "crm_purchaseorder" ("salesdocument_ptr_id");\n'
                'CREATE UNIQUE INDEX IF NOT EXISTS "crm_purchaseconfirmation_ptr_uniq" '
                'ON "crm_purchaseconfirmation" ("salesdocument_ptr_id");'
            ),
            reverse_sql=(
                'DROP INDEX IF EXISTS "crm_invoice_ptr_uniq";\n'
                'DROP INDEX IF EXISTS "crm_quote_ptr_uniq";\n'
                'DROP INDEX IF EXISTS "crm_deliverynote_ptr_uniq";\n'
                'DROP INDEX IF EXISTS "crm_paymentreminder_ptr_uniq";\n'
                'DROP INDEX IF EXISTS "crm_purchaseorder_ptr_uniq";\n'
                'DROP INDEX IF EXISTS "crm_purchaseconfirmation_ptr_uniq";'
            ),
        ),

        # ---------------------------------------------------------------
        # 1. State-only rename of the MTI parent + child ptr fields
        # ---------------------------------------------------------------
        RenameParentModel(
            old_name="SalesDocument",
            new_name="CommercialDocument",
            child_models=[
                "Invoice",
                "Quote",
                "DeliveryNote",
                "PaymentReminder",
                "PurchaseOrder",
                "PurchaseConfirmation",
            ],
        ),

        # ---------------------------------------------------------------
        # 2. Rename satellite / non-MTI models. With explicit db_table
        #    the DB portion is a no-op (old_db_table == new_db_table).
        # ---------------------------------------------------------------
        migrations.RenameModel(
            old_name="SalesDocumentPosition",
            new_name="CommercialDocumentPosition",
        ),
        migrations.RenameModel(
            old_name="SalesDocumentMedia",
            new_name="CommercialDocumentMedia",
        ),
        migrations.RenameModel(
            old_name="TextParagraphInSalesDocument",
            new_name="TextParagraphInCommercialDocument",
        ),
        migrations.RenameModel(
            old_name="PostalAddressForSalesDocument",
            new_name="PostalAddressForCommercialDocument",
        ),
        migrations.RenameModel(
            old_name="EmailAddressForSalesDocument",
            new_name="EmailAddressForCommercialDocument",
        ),
        migrations.RenameModel(
            old_name="PhoneAddressForSalesDocument",
            new_name="PhoneAddressForCommercialDocument",
        ),

        # ---------------------------------------------------------------
        # 3. Rename physical DB tables and keep state.db_table in sync.
        #
        #    We use RunSQL for the physical rename (plain ALTER TABLE
        #    RENAME TO, which is safe on SQLite >= 3.25 and also updates
        #    FK references in other tables).  We pair it with a state-only
        #    AlterModelTable so that subsequent RenameField operations
        #    (which rely on model._meta.db_table) look at the new name.
        # ---------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name="commercialdocument",
                    table="crm_commercialdocument",
                ),
                migrations.AlterModelTable(
                    name="commercialdocumentposition",
                    table="crm_commercialdocumentposition",
                ),
                migrations.AlterModelTable(
                    name="commercialdocumentmedia",
                    table="crm_commercialdocumentmedia",
                ),
                migrations.AlterModelTable(
                    name="textparagraphincommercialdocument",
                    table="crm_textparagraphincommercialdocument",
                ),
                migrations.AlterModelTable(
                    name="postaladdressforcommercialdocument",
                    table="crm_postaladdressforcommercialdocument",
                ),
                migrations.AlterModelTable(
                    name="emailaddressforcommercialdocument",
                    table="crm_emailaddressforcommercialdocument",
                ),
                migrations.AlterModelTable(
                    name="phoneaddressforcommercialdocument",
                    table="crm_phoneaddressforcommercialdocument",
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_salesdocument" RENAME TO "crm_commercialdocument"',
                    reverse_sql='ALTER TABLE "crm_commercialdocument" RENAME TO "crm_salesdocument"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_salesdocumentposition" RENAME TO "crm_commercialdocumentposition"',
                    reverse_sql='ALTER TABLE "crm_commercialdocumentposition" RENAME TO "crm_salesdocumentposition"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_salesdocumentmedia" RENAME TO "crm_commercialdocumentmedia"',
                    reverse_sql='ALTER TABLE "crm_commercialdocumentmedia" RENAME TO "crm_salesdocumentmedia"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_textparagraphinsalesdocument" RENAME TO "crm_textparagraphincommercialdocument"',
                    reverse_sql='ALTER TABLE "crm_textparagraphincommercialdocument" RENAME TO "crm_textparagraphinsalesdocument"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_postaladdressforsalesdocument" RENAME TO "crm_postaladdressforcommercialdocument"',
                    reverse_sql='ALTER TABLE "crm_postaladdressforcommercialdocument" RENAME TO "crm_postaladdressforsalesdocument"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_emailaddressforsalesdocument" RENAME TO "crm_emailaddressforcommercialdocument"',
                    reverse_sql='ALTER TABLE "crm_emailaddressforcommercialdocument" RENAME TO "crm_emailaddressforsalesdocument"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_phoneaddressforsalesdocument" RENAME TO "crm_phoneaddressforcommercialdocument"',
                    reverse_sql='ALTER TABLE "crm_phoneaddressforcommercialdocument" RENAME TO "crm_phoneaddressforsalesdocument"',
                ),
            ],
        ),

        # ---------------------------------------------------------------
        # 4. Rename ptr columns on child tables.  State already updated
        #    by RenameParentModel (step 1); only DB column rename needed.
        # ---------------------------------------------------------------
        migrations.RunSQL(
            sql='ALTER TABLE "crm_invoice" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_invoice" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE "crm_quote" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_quote" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE "crm_deliverynote" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_deliverynote" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE "crm_paymentreminder" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_paymentreminder" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE "crm_purchaseorder" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_purchaseorder" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),
        migrations.RunSQL(
            sql='ALTER TABLE "crm_purchaseconfirmation" RENAME COLUMN "salesdocument_ptr_id" TO "commercialdocument_ptr_id"',
            reverse_sql='ALTER TABLE "crm_purchaseconfirmation" RENAME COLUMN "commercialdocument_ptr_id" TO "salesdocument_ptr_id"',
        ),

        # ---------------------------------------------------------------
        # 5. Rename FK fields + columns.  State changes via RenameField,
        #    DB changes via RunSQL (plain column rename, avoids SQLite
        #    _remake_table which would need to re-copy the whole table).
        # ---------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name="commercialdocument",
                    old_name="derived_from_sales_document",
                    new_name="derived_from_commercial_document",
                ),
                migrations.RenameField(
                    model_name="textparagraphincommercialdocument",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
                migrations.RenameField(
                    model_name="postaladdressforcommercialdocument",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
                migrations.RenameField(
                    model_name="emailaddressforcommercialdocument",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
                migrations.RenameField(
                    model_name="phoneaddressforcommercialdocument",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
                migrations.RenameField(
                    model_name="commercialdocumentposition",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
                migrations.RenameField(
                    model_name="commercialdocumentmedia",
                    old_name="sales_document",
                    new_name="commercial_document",
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_commercialdocument" RENAME COLUMN "derived_from_sales_document_id" TO "derived_from_commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_commercialdocument" RENAME COLUMN "derived_from_commercial_document_id" TO "derived_from_sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_textparagraphincommercialdocument" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_textparagraphincommercialdocument" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_postaladdressforcommercialdocument" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_postaladdressforcommercialdocument" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_emailaddressforcommercialdocument" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_emailaddressforcommercialdocument" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_phoneaddressforcommercialdocument" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_phoneaddressforcommercialdocument" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_commercialdocumentposition" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_commercialdocumentposition" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_commercialdocumentmedia" RENAME COLUMN "sales_document_id" TO "commercial_document_id"',
                    reverse_sql='ALTER TABLE "crm_commercialdocumentmedia" RENAME COLUMN "commercial_document_id" TO "sales_document_id"',
                ),
            ],
        ),
    ]
