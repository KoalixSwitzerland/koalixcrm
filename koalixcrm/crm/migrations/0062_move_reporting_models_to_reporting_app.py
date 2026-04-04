# Hand-written: Remove reporting models from crm state (moved to reporting app)
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0061_move_document_models_to_contract_object_management'),
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                # Delete dependents first
                migrations.DeleteModel(name='Work'),
                migrations.DeleteModel(name='Agreement'),
                migrations.DeleteModel(name='Estimation'),
                migrations.DeleteModel(name='GenericProjectLink'),
                migrations.DeleteModel(name='GenericTaskLink'),
                migrations.DeleteModel(name='ReportingPeriod'),
                migrations.DeleteModel(name='Task'),
                migrations.DeleteModel(name='ResourcePrice'),
                migrations.DeleteModel(name='ResourceManager'),
                migrations.DeleteModel(name='HumanResource'),
                migrations.DeleteModel(name='Resource'),
                migrations.DeleteModel(name='Project'),
                # Then independent models
                migrations.DeleteModel(name='AgreementStatus'),
                migrations.DeleteModel(name='AgreementType'),
                migrations.DeleteModel(name='EstimationStatus'),
                migrations.DeleteModel(name='ProjectLinkType'),
                migrations.DeleteModel(name='ProjectStatus'),
                migrations.DeleteModel(name='ReportingPeriodStatus'),
                migrations.DeleteModel(name='ResourceType'),
                migrations.DeleteModel(name='TaskLinkType'),
                migrations.DeleteModel(name='TaskStatus'),
            ],
            database_operations=[],
        ),
    ]
