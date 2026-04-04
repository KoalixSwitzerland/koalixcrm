# Hand-written: Remove document models from crm state (moved to contract_object_management)
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0060_move_product_models_to_products_app'),
        ('contract_object_management', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Delete dependents first, then base models
                migrations.DeleteModel(name='PaymentReminder'),
                migrations.DeleteModel(name='DeliveryNote'),
                migrations.DeleteModel(name='PurchaseOrder'),
                migrations.DeleteModel(name='PurchaseConfirmation'),
                migrations.DeleteModel(name='Quote'),
                migrations.DeleteModel(name='Invoice'),
                migrations.DeleteModel(name='PostalAddressForSalesDocument'),
                migrations.DeleteModel(name='PhoneAddressForSalesDocument'),
                migrations.DeleteModel(name='EmailAddressForSalesDocument'),
                migrations.DeleteModel(name='TextParagraphInSalesDocument'),
                migrations.DeleteModel(name='SalesDocumentPosition'),
                migrations.DeleteModel(name='Position'),
                migrations.DeleteModel(name='SalesDocument'),
                migrations.DeleteModel(name='PostalAddressForContract'),
                migrations.DeleteModel(name='PhoneAddressForContract'),
                migrations.DeleteModel(name='EmailAddressForContract'),
                migrations.DeleteModel(name='Contract'),
            ],
            database_operations=[],
        ),
    ]
