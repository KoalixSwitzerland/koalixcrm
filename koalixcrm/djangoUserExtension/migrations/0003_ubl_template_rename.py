# -*- coding: utf-8 -*-
"""UBL 2.3 rename applied to the djangoUserExtension document-template
family, mirroring the contracts-side rename already performed in
contracts/migrations/0006_ubl_document_rename.py.

QuoteTemplate                -> QuotationTemplate
DeliveryNoteTemplate         -> DespatchAdviceTemplate
PurchaseConfirmationTemplate -> SalesOrderTemplate

TemplateSet.quote_template                  -> quotation_template
TemplateSet.delivery_note_template          -> despatch_advice_template
TemplateSet.purchase_confirmation_template  -> sales_order_template

Unlike contracts (which pinned explicit db_table names), these models
rely on Django's default table naming, so RenameModel automatically
updates the db_table. No SeparateDatabaseAndState dance needed.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("djangoUserExtension", "0002_documenttemplate_s3_file_fields"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="QuoteTemplate",
            new_name="QuotationTemplate",
        ),
        migrations.RenameModel(
            old_name="DeliveryNoteTemplate",
            new_name="DespatchAdviceTemplate",
        ),
        migrations.RenameModel(
            old_name="PurchaseConfirmationTemplate",
            new_name="SalesOrderTemplate",
        ),
        migrations.RenameField(
            model_name="templateset",
            old_name="quote_template",
            new_name="quotation_template",
        ),
        migrations.RenameField(
            model_name="templateset",
            old_name="delivery_note_template",
            new_name="despatch_advice_template",
        ),
        migrations.RenameField(
            model_name="templateset",
            old_name="purchase_confirmation_template",
            new_name="sales_order_template",
        ),
    ]
