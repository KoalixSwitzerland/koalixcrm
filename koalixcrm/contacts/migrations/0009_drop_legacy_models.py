"""Drop legacy Party-domain models + DB tables (issue #395 G3).

Final destructive step of the Party migration. By this point:

  - Every row has been migrated into the Party tables (0005_backfill_party).
  - Every invariant has been verified (0006_verify_ready_for_cutover).
  - Party.default_billing_cycle has inherited the legacy Customer value
    (0008_backfill_party_billing_cycle).
  - Documents/products have dropped their legacy FKs (contracts.0010,
    products.0004).

This migration removes the Django model classes and drops the underlying
tables. After this point the legacy data only survives in pre-v2.0.0
backups — that's by design.

PostalAddress / PhoneAddress / EmailAddress are NOT dropped here — they
are retained as MTI base classes for non-legacy satellites in contracts
(PostalAddressForContract etc.) and djangoUserExtension
(UserExtensionPostalAddress etc.). Restructuring those satellites and
finally dropping the bases is tracked as a follow-up (out of scope for
this commit;
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_backfill_party_billing_cycle'),
        # Legacy FK drops must land first so there are no dangling FK refs
        # into the tables we're about to delete.
        ('contract_object_management', '0010_drop_legacy_customer_fks'),
        ('products', '0004_drop_legacy_customer_group_fks'),
    ]

    operations = [
        # Subclasses first (MTI children before their parents).
        migrations.DeleteModel(name='CallForContact'),
        migrations.DeleteModel(name='VisitForContact'),
        migrations.DeleteModel(name='Call'),
        migrations.DeleteModel(name='Customer'),
        migrations.DeleteModel(name='Supplier'),
        migrations.DeleteModel(name='PostalAddressForContact'),
        migrations.DeleteModel(name='EmailAddressForContact'),
        migrations.DeleteModel(name='PhoneAddressForContact'),
        migrations.DeleteModel(name='ContactPersonAssociation'),
        migrations.DeleteModel(name='Person'),
        migrations.DeleteModel(name='CustomerGroup'),
        # Legacy Contact last (Customer/Supplier inherited from it).
        migrations.DeleteModel(name='Contact'),
    ]
