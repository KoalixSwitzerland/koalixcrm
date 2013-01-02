# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table('crm_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('rounding', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('crm', ['Currency'])

        # Adding model 'PostalAddress'
        db.create_table('crm_postaladdress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('prename', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('addressline1', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('addressline2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('addressline3', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('addressline4', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['PostalAddress'])

        # Adding model 'PhoneAddress'
        db.create_table('crm_phoneaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('crm', ['PhoneAddress'])

        # Adding model 'EmailAddress'
        db.create_table('crm_emailaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
        ))
        db.send_create_signal('crm', ['EmailAddress'])

        # Adding model 'Contact'
        db.create_table('crm_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('dateofcreation', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastmodification', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastmodifiedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
        ))
        db.send_create_signal('crm', ['Contact'])

        # Adding model 'CustomerBillingCycle'
        db.create_table('crm_customerbillingcycle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('timeToPaymentDate', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('crm', ['CustomerBillingCycle'])

        # Adding model 'CustomerGroup'
        db.create_table('crm_customergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('crm', ['CustomerGroup'])

        # Adding model 'Customer'
        db.create_table('crm_customer', (
            ('contact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.Contact'], unique=True, primary_key=True)),
            ('defaultCustomerBillingCycle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CustomerBillingCycle'])),
        ))
        db.send_create_signal('crm', ['Customer'])

        # Adding M2M table for field ismemberof on 'Customer'
        db.create_table('crm_customer_ismemberof', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['crm.customer'], null=False)),
            ('customergroup', models.ForeignKey(orm['crm.customergroup'], null=False))
        ))
        db.create_unique('crm_customer_ismemberof', ['customer_id', 'customergroup_id'])

        # Adding model 'Supplier'
        db.create_table('crm_supplier', (
            ('contact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.Contact'], unique=True, primary_key=True)),
            ('offersShipmentToCustomers', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('crm', ['Supplier'])

        # Adding model 'Contract'
        db.create_table('crm_contract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='db_relcontractstaff', null=True, to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('defaultcustomer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Customer'], null=True, blank=True)),
            ('defaultSupplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Supplier'], null=True, blank=True)),
            ('defaultcurrency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Currency'])),
            ('dateofcreation', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastmodification', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastmodifiedby', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_contractlstmodified', to=orm['auth.User'])),
        ))
        db.send_create_signal('crm', ['Contract'])

        # Adding model 'PurchaseOrder'
        db.create_table('crm_purchaseorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
            ('externalReference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Supplier'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('lastPricingDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lastCalculatedPrice', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('lastCalculatedTax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='db_relpostaff', null=True, to=orm['auth.User'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Currency'])),
            ('dateofcreation', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastmodification', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastmodifiedby', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_polstmodified', to=orm['auth.User'])),
        ))
        db.send_create_signal('crm', ['PurchaseOrder'])

        # Adding model 'SalesContract'
        db.create_table('crm_salescontract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
            ('externalReference', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('lastPricingDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lastCalculatedPrice', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('lastCalculatedTax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Customer'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='db_relscstaff', null=True, to=orm['auth.User'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Currency'])),
            ('dateofcreation', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastmodification', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastmodifiedby', self.gf('django.db.models.fields.related.ForeignKey')(blank='True', related_name='db_lstscmodified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('crm', ['SalesContract'])

        # Adding model 'Quote'
        db.create_table('crm_quote', (
            ('salescontract_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.SalesContract'], unique=True, primary_key=True)),
            ('validuntil', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('crm', ['Quote'])

        # Adding model 'Invoice'
        db.create_table('crm_invoice', (
            ('salescontract_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.SalesContract'], unique=True, primary_key=True)),
            ('payableuntil', self.gf('django.db.models.fields.DateField')()),
            ('derivatedFromQuote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Quote'], null=True, blank=True)),
            ('paymentBankReference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('crm', ['Invoice'])

        # Adding model 'Unit'
        db.create_table('crm_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('isAFractionOf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Unit'], null=True, blank=True)),
            ('fractionFactorToNextHigherUnit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['Unit'])

        # Adding model 'Tax'
        db.create_table('crm_tax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxrate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('accountActiva', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='db_relaccountactiva', null=True, to=orm['accounting.Account'])),
            ('accountPassiva', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='db_relaccountpassiva', null=True, to=orm['accounting.Account'])),
        ))
        db.send_create_signal('crm', ['Tax'])

        # Adding model 'Product'
        db.create_table('crm_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('productNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('defaultunit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Unit'])),
            ('dateofcreation', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lastmodification', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastmodifiedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank='True')),
            ('tax', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Tax'])),
            ('accoutingProductCategorie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.ProductCategorie'], null=True, blank='True')),
        ))
        db.send_create_signal('crm', ['Product'])

        # Adding model 'UnitTransform'
        db.create_table('crm_unittransform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromUnit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltransfromfromunit', to=orm['crm.Unit'])),
            ('toUnit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltransfromtounit', to=orm['crm.Unit'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Product'])),
            ('factor', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['UnitTransform'])

        # Adding model 'CustomerGroupTransform'
        db.create_table('crm_customergrouptransform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromCustomerGroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltransfromfromcustomergroup', to=orm['crm.CustomerGroup'])),
            ('toCustomerGroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='db_reltransfromtocustomergroup', to=orm['crm.CustomerGroup'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Product'])),
            ('factor', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['CustomerGroupTransform'])

        # Adding model 'Price'
        db.create_table('crm_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Product'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Unit'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Currency'])),
            ('customerGroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CustomerGroup'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=17, decimal_places=2)),
            ('validfrom', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('validuntil', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['Price'])

        # Adding model 'Position'
        db.create_table('crm_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('positionNumber', self.gf('django.db.models.fields.IntegerField')()),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Product'], null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Unit'], null=True, blank=True)),
            ('sentOn', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Supplier'], null=True, blank=True)),
            ('shipmentID', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('overwriteProductPrice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('positionPricePerUnit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('lastPricingDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lastCalculatedPrice', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
            ('lastCalculatedTax', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=17, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('crm', ['Position'])

        # Adding model 'SalesContractPosition'
        db.create_table('crm_salescontractposition', (
            ('position_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.Position'], unique=True, primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.SalesContract'])),
        ))
        db.send_create_signal('crm', ['SalesContractPosition'])

        # Adding model 'PurchaseOrderPosition'
        db.create_table('crm_purchaseorderposition', (
            ('position_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.Position'], unique=True, primary_key=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.PurchaseOrder'])),
        ))
        db.send_create_signal('crm', ['PurchaseOrderPosition'])

        # Adding model 'PhoneAddressForContact'
        db.create_table('crm_phoneaddressforcontact', (
            ('phoneaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PhoneAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contact'])),
        ))
        db.send_create_signal('crm', ['PhoneAddressForContact'])

        # Adding model 'EmailAddressForContact'
        db.create_table('crm_emailaddressforcontact', (
            ('emailaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.EmailAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contact'])),
        ))
        db.send_create_signal('crm', ['EmailAddressForContact'])

        # Adding model 'PostalAddressForContact'
        db.create_table('crm_postaladdressforcontact', (
            ('postaladdress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PostalAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contact'])),
        ))
        db.send_create_signal('crm', ['PostalAddressForContact'])

        # Adding model 'PostalAddressForContract'
        db.create_table('crm_postaladdressforcontract', (
            ('postaladdress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PostalAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
        ))
        db.send_create_signal('crm', ['PostalAddressForContract'])

        # Adding model 'PostalAddressForPurchaseOrder'
        db.create_table('crm_postaladdressforpurchaseorder', (
            ('postaladdress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PostalAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.PurchaseOrder'])),
        ))
        db.send_create_signal('crm', ['PostalAddressForPurchaseOrder'])

        # Adding model 'PostalAddressForSalesContract'
        db.create_table('crm_postaladdressforsalescontract', (
            ('postaladdress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PostalAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.SalesContract'])),
        ))
        db.send_create_signal('crm', ['PostalAddressForSalesContract'])

        # Adding model 'PhoneAddressForContract'
        db.create_table('crm_phoneaddressforcontract', (
            ('phoneaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PhoneAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
        ))
        db.send_create_signal('crm', ['PhoneAddressForContract'])

        # Adding model 'PhoneAddressForSalesContract'
        db.create_table('crm_phoneaddressforsalescontract', (
            ('phoneaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PhoneAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.SalesContract'])),
        ))
        db.send_create_signal('crm', ['PhoneAddressForSalesContract'])

        # Adding model 'PhoneAddressForPurchaseOrder'
        db.create_table('crm_phoneaddressforpurchaseorder', (
            ('phoneaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.PhoneAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.PurchaseOrder'])),
        ))
        db.send_create_signal('crm', ['PhoneAddressForPurchaseOrder'])

        # Adding model 'EmailAddressForContract'
        db.create_table('crm_emailaddressforcontract', (
            ('emailaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.EmailAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contract'])),
        ))
        db.send_create_signal('crm', ['EmailAddressForContract'])

        # Adding model 'EmailAddressForSalesContract'
        db.create_table('crm_emailaddressforsalescontract', (
            ('emailaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.EmailAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.SalesContract'])),
        ))
        db.send_create_signal('crm', ['EmailAddressForSalesContract'])

        # Adding model 'EmailAddressForPurchaseOrder'
        db.create_table('crm_emailaddressforpurchaseorder', (
            ('emailaddress_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.EmailAddress'], unique=True, primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.PurchaseOrder'])),
        ))
        db.send_create_signal('crm', ['EmailAddressForPurchaseOrder'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table('crm_currency')

        # Deleting model 'PostalAddress'
        db.delete_table('crm_postaladdress')

        # Deleting model 'PhoneAddress'
        db.delete_table('crm_phoneaddress')

        # Deleting model 'EmailAddress'
        db.delete_table('crm_emailaddress')

        # Deleting model 'Contact'
        db.delete_table('crm_contact')

        # Deleting model 'CustomerBillingCycle'
        db.delete_table('crm_customerbillingcycle')

        # Deleting model 'CustomerGroup'
        db.delete_table('crm_customergroup')

        # Deleting model 'Customer'
        db.delete_table('crm_customer')

        # Removing M2M table for field ismemberof on 'Customer'
        db.delete_table('crm_customer_ismemberof')

        # Deleting model 'Supplier'
        db.delete_table('crm_supplier')

        # Deleting model 'Contract'
        db.delete_table('crm_contract')

        # Deleting model 'PurchaseOrder'
        db.delete_table('crm_purchaseorder')

        # Deleting model 'SalesContract'
        db.delete_table('crm_salescontract')

        # Deleting model 'Quote'
        db.delete_table('crm_quote')

        # Deleting model 'Invoice'
        db.delete_table('crm_invoice')

        # Deleting model 'Unit'
        db.delete_table('crm_unit')

        # Deleting model 'Tax'
        db.delete_table('crm_tax')

        # Deleting model 'Product'
        db.delete_table('crm_product')

        # Deleting model 'UnitTransform'
        db.delete_table('crm_unittransform')

        # Deleting model 'CustomerGroupTransform'
        db.delete_table('crm_customergrouptransform')

        # Deleting model 'Price'
        db.delete_table('crm_price')

        # Deleting model 'Position'
        db.delete_table('crm_position')

        # Deleting model 'SalesContractPosition'
        db.delete_table('crm_salescontractposition')

        # Deleting model 'PurchaseOrderPosition'
        db.delete_table('crm_purchaseorderposition')

        # Deleting model 'PhoneAddressForContact'
        db.delete_table('crm_phoneaddressforcontact')

        # Deleting model 'EmailAddressForContact'
        db.delete_table('crm_emailaddressforcontact')

        # Deleting model 'PostalAddressForContact'
        db.delete_table('crm_postaladdressforcontact')

        # Deleting model 'PostalAddressForContract'
        db.delete_table('crm_postaladdressforcontract')

        # Deleting model 'PostalAddressForPurchaseOrder'
        db.delete_table('crm_postaladdressforpurchaseorder')

        # Deleting model 'PostalAddressForSalesContract'
        db.delete_table('crm_postaladdressforsalescontract')

        # Deleting model 'PhoneAddressForContract'
        db.delete_table('crm_phoneaddressforcontract')

        # Deleting model 'PhoneAddressForSalesContract'
        db.delete_table('crm_phoneaddressforsalescontract')

        # Deleting model 'PhoneAddressForPurchaseOrder'
        db.delete_table('crm_phoneaddressforpurchaseorder')

        # Deleting model 'EmailAddressForContract'
        db.delete_table('crm_emailaddressforcontract')

        # Deleting model 'EmailAddressForSalesContract'
        db.delete_table('crm_emailaddressforsalescontract')

        # Deleting model 'EmailAddressForPurchaseOrder'
        db.delete_table('crm_emailaddressforpurchaseorder')


    models = {
        'accounting.account': {
            'Meta': {'ordering': "['accountNumber']", 'object_name': 'Account'},
            'accountNumber': ('django.db.models.fields.IntegerField', [], {}),
            'accountType': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isACustomerPaymentAccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isProductInventoryActiva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isopeninterestaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isopenreliabilitiesaccount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'crm.customergrouptransform': {
            'Meta': {'object_name': 'CustomerGroupTransform'},
            'factor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fromCustomerGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltransfromfromcustomergroup'", 'to': "orm['crm.CustomerGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Product']"}),
            'toCustomerGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltransfromtocustomergroup'", 'to': "orm['crm.CustomerGroup']"})
        },
        'crm.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crm.emailaddressforcontact': {
            'Meta': {'object_name': 'EmailAddressForContact', '_ormbases': ['crm.EmailAddress']},
            'emailaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.EmailAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contact']"}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.emailaddressforcontract': {
            'Meta': {'object_name': 'EmailAddressForContract', '_ormbases': ['crm.EmailAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'emailaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.EmailAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.emailaddressforpurchaseorder': {
            'Meta': {'object_name': 'EmailAddressForPurchaseOrder', '_ormbases': ['crm.EmailAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.PurchaseOrder']"}),
            'emailaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.EmailAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.emailaddressforsalescontract': {
            'Meta': {'object_name': 'EmailAddressForSalesContract', '_ormbases': ['crm.EmailAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.SalesContract']"}),
            'emailaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.EmailAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.invoice': {
            'Meta': {'object_name': 'Invoice', '_ormbases': ['crm.SalesContract']},
            'derivatedFromQuote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Quote']", 'null': 'True', 'blank': 'True'}),
            'payableuntil': ('django.db.models.fields.DateField', [], {}),
            'paymentBankReference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'salescontract_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.SalesContract']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.phoneaddress': {
            'Meta': {'object_name': 'PhoneAddress'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'crm.phoneaddressforcontact': {
            'Meta': {'object_name': 'PhoneAddressForContact', '_ormbases': ['crm.PhoneAddress']},
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contact']"}),
            'phoneaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PhoneAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.phoneaddressforcontract': {
            'Meta': {'object_name': 'PhoneAddressForContract', '_ormbases': ['crm.PhoneAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'phoneaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PhoneAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.phoneaddressforpurchaseorder': {
            'Meta': {'object_name': 'PhoneAddressForPurchaseOrder', '_ormbases': ['crm.PhoneAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.PurchaseOrder']"}),
            'phoneaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PhoneAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.phoneaddressforsalescontract': {
            'Meta': {'object_name': 'PhoneAddressForSalesContract', '_ormbases': ['crm.PhoneAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.SalesContract']"}),
            'phoneaddress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PhoneAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.position': {
            'Meta': {'object_name': 'Position'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastCalculatedPrice': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastCalculatedTax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastPricingDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'overwriteProductPrice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'positionNumber': ('django.db.models.fields.IntegerField', [], {}),
            'positionPricePerUnit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Product']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'sentOn': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'shipmentID': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Supplier']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Unit']", 'null': 'True', 'blank': 'True'})
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
        'crm.postaladdressforcontact': {
            'Meta': {'object_name': 'PostalAddressForContact', '_ormbases': ['crm.PostalAddress']},
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contact']"}),
            'postaladdress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PostalAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.postaladdressforcontract': {
            'Meta': {'object_name': 'PostalAddressForContract', '_ormbases': ['crm.PostalAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'postaladdress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PostalAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.postaladdressforpurchaseorder': {
            'Meta': {'object_name': 'PostalAddressForPurchaseOrder', '_ormbases': ['crm.PostalAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.PurchaseOrder']"}),
            'postaladdress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PostalAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.postaladdressforsalescontract': {
            'Meta': {'object_name': 'PostalAddressForSalesContract', '_ormbases': ['crm.PostalAddress']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.SalesContract']"}),
            'postaladdress_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.PostalAddress']", 'unique': 'True', 'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.price': {
            'Meta': {'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Currency']"}),
            'customerGroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.CustomerGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '17', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Product']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Unit']"}),
            'validfrom': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'validuntil': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
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
        'crm.purchaseorder': {
            'Meta': {'object_name': 'PurchaseOrder'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Currency']"}),
            'dateofcreation': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'externalReference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastCalculatedPrice': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastCalculatedTax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastPricingDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lastmodification': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastmodifiedby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_polstmodified'", 'to': "orm['auth.User']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'db_relpostaff'", 'null': 'True', 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Supplier']"})
        },
        'crm.purchaseorderposition': {
            'Meta': {'object_name': 'PurchaseOrderPosition', '_ormbases': ['crm.Position']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.PurchaseOrder']"}),
            'position_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.Position']", 'unique': 'True', 'primary_key': 'True'})
        },
        'crm.quote': {
            'Meta': {'object_name': 'Quote', '_ormbases': ['crm.SalesContract']},
            'salescontract_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.SalesContract']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'validuntil': ('django.db.models.fields.DateField', [], {})
        },
        'crm.salescontract': {
            'Meta': {'object_name': 'SalesContract'},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contract']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Currency']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Customer']"}),
            'dateofcreation': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'externalReference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastCalculatedPrice': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastCalculatedTax': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '17', 'decimal_places': '2', 'blank': 'True'}),
            'lastPricingDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'lastmodification': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastmodifiedby': ('django.db.models.fields.related.ForeignKey', [], {'blank': "'True'", 'related_name': "'db_lstscmodified'", 'null': 'True', 'to': "orm['auth.User']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'db_relscstaff'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'crm.salescontractposition': {
            'Meta': {'object_name': 'SalesContractPosition', '_ormbases': ['crm.Position']},
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.SalesContract']"}),
            'position_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['crm.Position']", 'unique': 'True', 'primary_key': 'True'})
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
        'crm.unittransform': {
            'Meta': {'object_name': 'UnitTransform'},
            'factor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fromUnit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltransfromfromunit'", 'to': "orm['crm.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Product']"}),
            'toUnit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'db_reltransfromtounit'", 'to': "orm['crm.Unit']"})
        }
    }

    complete_apps = ['crm']