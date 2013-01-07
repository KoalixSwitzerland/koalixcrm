# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscription'
        db.create_table('subscriptions_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
            ('subscriptiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.SubscriptionType'], null=True)),
        ))
        db.send_create_signal('subscriptions', ['Subscription'])

        # Adding model 'SubscriptionEvent'
        db.create_table('subscriptions_subscriptionevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriptions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.Subscription'])),
            ('eventdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('subscriptions', ['SubscriptionEvent'])

        # Adding model 'SubscriptionType'
        db.create_table('subscriptions_subscriptiontype', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.Product'], unique=True, primary_key=True)),
            ('cancelationPeriod', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('automaticContractExtension', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('automaticContractExtensionReminder', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('minimumDuration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('paymentIntervall', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('contractDocument', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('subscriptions', ['SubscriptionType'])


    def backwards(self, orm):
        # Deleting model 'Subscription'
        db.delete_table('subscriptions_subscription')

        # Deleting model 'SubscriptionEvent'
        db.delete_table('subscriptions_subscriptionevent')

        # Deleting model 'SubscriptionType'
        db.delete_table('subscriptions_subscriptiontype')


    models = {
        'accounting.account': {
            'Meta': {'ordering': "['accountNumber']", 'object_name': 'Account'},
            'accountNumber': ('django.db.models.fields.IntegerField', [], {}),
            'accountType': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isACustomerPaymentAccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isProductInventoryActiva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isopeninterestaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isopenreliabilitiesaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'originalAmount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'accounting.productcategorie': {
            'Meta': {'object_name': 'ProductCategorie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lossAccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_loss_account'", 'to': "orm['accounting.Account']"}),
            'profitAccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_profit_account'", 'to': "orm['accounting.Account']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'crm.contact': {
            'Meta': {'object_name': 'Contact'},
            'dateofcreation': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmodification': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastmodifiedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'crm.contract': {
            'Meta': {'object_name': 'Contract'},
            'dateofcreation': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'defaultSupplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Supplier']", 'null': 'True', 'blank': 'True'}),
            'defaultcurrency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Currency']"}),
            'defaultcustomer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Customer']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmodification': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastmodifiedby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_contractlstmodified'", 'to': "orm['auth.User']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'db_relcontractstaff'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'crm.currency': {
            'Meta': {'object_name': 'Currency'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rounding': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'crm.customer': {
            'Meta': {'object_name': 'Customer', '_ormbases': ['crm.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.Contact']", 'unique': 'True', 'primary_key': 'True'}),
            'defaultCustomerBillingCycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.CustomerBillingCycle']"}),
            'ismemberof': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['crm.CustomerGroup']", 'null': 'True', 'blank': 'True'})
        },
        'crm.customerbillingcycle': {
            'Meta': {'object_name': 'CustomerBillingCycle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'timeToPaymentDate': ('django.db.models.fields.IntegerField', [], {})
        },
        'crm.customergroup': {
            'Meta': {'object_name': 'CustomerGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'crm.product': {
            'Meta': {'object_name': 'Product'},
            'accoutingProductCategorie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.ProductCategorie']", 'null': 'True', 'blank': "'True'"}),
            'dateofcreation': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'defaultunit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Unit']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastmodification': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastmodifiedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': "'True'"}),
            'productNumber': ('django.db.models.fields.IntegerField', [], {}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Tax']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'crm.supplier': {
            'Meta': {'object_name': 'Supplier', '_ormbases': ['crm.Contact']},
            'contact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.Contact']", 'unique': 'True', 'primary_key': 'True'}),
            'offersShipmentToCustomers': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'crm.tax': {
            'Meta': {'object_name': 'Tax'},
            'accountActiva': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'db_relaccountactiva'", 'null': 'True', 'to': "orm['accounting.Account']"}),
            'accountPassiva': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'db_relaccountpassiva'", 'null': 'True', 'to': "orm['accounting.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'taxrate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'crm.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fractionFactorToNextHigherUnit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isAFractionOf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Unit']", 'null': 'True', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'subscriptions.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriptiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscriptions.SubscriptionType']", 'null': 'True'})
        },
        'subscriptions.subscriptionevent': {
            'Meta': {'object_name': 'SubscriptionEvent'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'eventdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriptions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscriptions.Subscription']"})
        },
        'subscriptions.subscriptiontype': {
            'Meta': {'object_name': 'SubscriptionType', '_ormbases': ['crm.Product']},
            'automaticContractExtension': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'automaticContractExtensionReminder': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cancelationPeriod': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'contractDocument': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'minimumDuration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'paymentIntervall': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.Product']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['subscriptions']