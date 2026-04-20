# -*- coding: utf-8 -*-
"""Drop the three MTI base classes PostalAddress, PhoneAddress, EmailAddress.

All inheriting satellites (PostalAddressForContract, PhoneAddressForContract,
EmailAddressForContract, PostalAddressForCommercialDocument,
PhoneAddressForCommercialDocument, EmailAddressForCommercialDocument,
UserExtensionPostalAddress, UserExtensionPhoneAddress,
UserExtensionEmailAddress) were deleted in:
  - contracts.0013_contract_address_assignments
  - contracts.0014_commercial_document_address_assignments
  - djangoUserExtension.0005_user_address_assignments

This migration runs strictly after those three and drops the now-orphaned
base tables crm_postaladdress, crm_phoneaddress, crm_emailaddress.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0011_workspace_scoping'),
        ('contract_object_management', '0014_commercial_document_address_assignments'),
        ('djangoUserExtension', '0005_user_address_assignments'),
    ]

    operations = [
        migrations.DeleteModel(name='PostalAddress'),
        migrations.DeleteModel(name='PhoneAddress'),
        migrations.DeleteModel(name='EmailAddress'),
    ]
