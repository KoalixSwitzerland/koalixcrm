# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'XSLFile'
        db.create_table('djangoUserExtension_xslfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('xslfile', self.gf('filebrowser.fields.FileBrowseField')(max_length=200)),
        ))
        db.send_create_signal('djangoUserExtension', ['XSLFile'])

        # Adding model 'UserExtension'
        db.create_table('djangoUserExtension_userextension', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('defaultTemplateSet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djangoUserExtension.TemplateSet'])),
            ('defaultCurrency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Currency'])),
        ))
        db.send_create_signal('djangoUserExtension', ['UserExtension'])

        # Adding model 'TemplateSet'
        db.create_table('djangoUserExtension_templateset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organisationname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('invoiceXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplateinvoice', to=orm['djangoUserExtension.XSLFile'])),
            ('quoteXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplatequote', to=orm['djangoUserExtension.XSLFile'])),
            ('purchaseconfirmationXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplatepurchaseorder', to=orm['djangoUserExtension.XSLFile'])),
            ('deilveryorderXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplatedeliveryorder', to=orm['djangoUserExtension.XSLFile'])),
            ('profitLossStatementXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplateprofitlossstatement', to=orm['djangoUserExtension.XSLFile'])),
            ('balancesheetXSLFile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltemplatebalancesheet', to=orm['djangoUserExtension.XSLFile'])),
            ('logo', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('bankingaccountref', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('addresser', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('fopConfigurationFile', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('footerTextsalesorders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('headerTextsalesorders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('headerTextpurchaseorders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('footerTextpurchaseorders', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pagefooterleft', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('pagefootermiddle', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('djangoUserExtension', ['TemplateSet'])

        # Adding model 'UserExtensionPostalAddress'
        db.create_table('djangoUserExtension_userextensionpostaladdress', (
            ('postaladdress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PostalAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('userExtension', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djangoUserExtension.UserExtension'])),
        ))
        db.send_create_signal('djangoUserExtension', ['UserExtensionPostalAddress'])

        # Adding model 'UserExtensionPhoneAddress'
        db.create_table('djangoUserExtension_userextensionphoneaddress', (
            ('phoneaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PhoneAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('userExtension', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djangoUserExtension.UserExtension'])),
        ))
        db.send_create_signal('djangoUserExtension', ['UserExtensionPhoneAddress'])

        # Adding model 'UserExtensionEmailAddress'
        db.create_table('djangoUserExtension_userextensionemailaddress', (
            ('emailaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.EmailAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('userExtension', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djangoUserExtension.UserExtension'])),
        ))
        db.send_create_signal('djangoUserExtension', ['UserExtensionEmailAddress'])


    def backwards(self, orm):
        # Deleting model 'XSLFile'
        db.delete_table('djangoUserExtension_xslfile')

        # Deleting model 'UserExtension'
        db.delete_table('djangoUserExtension_userextension')

        # Deleting model 'TemplateSet'
        db.delete_table('djangoUserExtension_templateset')

        # Deleting model 'UserExtensionPostalAddress'
        db.delete_table('djangoUserExtension_userextensionpostaladdress')

        # Deleting model 'UserExtensionPhoneAddress'
        db.delete_table('djangoUserExtension_userextensionphoneaddress')

        # Deleting model 'UserExtensionEmailAddress'
        db.delete_table('djangoUserExtension_userextensionemailaddress')


    models = {
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
        'crm.currency': {
            'Meta': {'object_name': 'Currency'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rounding': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'crm.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crm.phoneaddress': {
            'Meta': {'object_name': 'PhoneAddress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'crm.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'addressline1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressline2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressline3': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressline4': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'prename': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'djangoUserExtension.templateset': {
            'Meta': {'object_name': 'TemplateSet'},
            'addresser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'balancesheetXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplatebalancesheet'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'bankingaccountref': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'deilveryorderXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplatedeliveryorder'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'footerTextpurchaseorders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footerTextsalesorders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fopConfigurationFile': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'headerTextpurchaseorders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'headerTextsalesorders': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoiceXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplateinvoice'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'organisationname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pagefooterleft': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'pagefootermiddle': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'profitLossStatementXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplateprofitlossstatement'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'purchaseconfirmationXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplatepurchaseorder'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'quoteXSLFile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltemplatequote'", 'to': "orm['djangoUserExtension.XSLFile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djangoUserExtension.userextension': {
            'Meta': {'object_name': 'UserExtension'},
            'defaultCurrency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Currency']"}),
            'defaultTemplateSet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangoUserExtension.TemplateSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'djangoUserExtension.userextensionemailaddress': {
            'Meta': {'object_name': 'UserExtensionEmailAddress', '_ormbases': ['crm.EmailAddress']},
            'emailaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.EmailAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'userExtension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangoUserExtension.UserExtension']"})
        },
        'djangoUserExtension.userextensionphoneaddress': {
            'Meta': {'object_name': 'UserExtensionPhoneAddress', '_ormbases': ['crm.PhoneAddress']},
            'phoneaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PhoneAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'userExtension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangoUserExtension.UserExtension']"})
        },
        'djangoUserExtension.userextensionpostaladdress': {
            'Meta': {'object_name': 'UserExtensionPostalAddress', '_ormbases': ['crm.PostalAddress']},
            'postaladdress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PostalAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'userExtension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangoUserExtension.UserExtension']"})
        },
        'djangoUserExtension.xslfile': {
            'Meta': {'object_name': 'XSLFile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'xslfile': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['djangoUserExtension']