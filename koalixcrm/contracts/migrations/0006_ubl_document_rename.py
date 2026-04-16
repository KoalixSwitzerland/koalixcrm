# -*- coding: utf-8 -*-
"""UBL 2.3 document-type rename.

Quote -> Quotation                  (crm_quote -> crm_quotation)
PurchaseConfirmation -> SalesOrder  (crm_purchaseconfirmation -> crm_salesorder)
DeliveryNote -> DespatchAdvice      (crm_deliverynote -> crm_despatchadvice)
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contract_object_management", "0005_add_credit_note"),
    ]

    operations = [
        # ---------------------------------------------------------------
        # 1. State-only rename of each MTI child model.  Because every
        #    model declares an explicit ``db_table`` in its Meta, Django
        #    treats the physical table name as pinned and RenameModel is
        #    a DB no-op.  The physical table rename happens in step 2.
        # ---------------------------------------------------------------
        migrations.RenameModel(
            old_name="Quote",
            new_name="Quotation",
        ),
        migrations.RenameModel(
            old_name="PurchaseConfirmation",
            new_name="SalesOrder",
        ),
        migrations.RenameModel(
            old_name="DeliveryNote",
            new_name="DespatchAdvice",
        ),

        # ---------------------------------------------------------------
        # 2. Rename physical tables and keep state.db_table in sync.
        #    ALTER TABLE ... RENAME TO is safe on SQLite >= 3.25 and on
        #    PostgreSQL; it auto-updates FK references in other tables
        #    (none exist for these leaf models, but harmless).
        # ---------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name="quotation",
                    table="crm_quotation",
                ),
                migrations.AlterModelTable(
                    name="salesorder",
                    table="crm_salesorder",
                ),
                migrations.AlterModelTable(
                    name="despatchadvice",
                    table="crm_despatchadvice",
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_quote" RENAME TO "crm_quotation"',
                    reverse_sql='ALTER TABLE "crm_quotation" RENAME TO "crm_quote"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_purchaseconfirmation" RENAME TO "crm_salesorder"',
                    reverse_sql='ALTER TABLE "crm_salesorder" RENAME TO "crm_purchaseconfirmation"',
                ),
                migrations.RunSQL(
                    sql='ALTER TABLE "crm_deliverynote" RENAME TO "crm_despatchadvice"',
                    reverse_sql='ALTER TABLE "crm_despatchadvice" RENAME TO "crm_deliverynote"',
                ),
            ],
        ),
    ]
