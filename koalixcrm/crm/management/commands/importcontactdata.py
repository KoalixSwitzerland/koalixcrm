from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.contrib.auth.models import User

from koalixcrm.crm.contact.contact import Contact, PostalAddressForContact, PhoneAddressForContact, EmailAddressForContact, ContactPersonAssociation
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.contact.customer import Customer, PhoneSystemForCustomer
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.contact.customerbillingcycle import CustomerBillingCycle
from koalixcrm.crm.contact.customergroup import CustomerGroup
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.product.tax import Tax
from koalixcrm.crm.product.attribute import AttributeSet
from koalixcrm.crm.const.purpose import *

import xlrd
from xlrd.sheet import ctype_text
from dateutil.parser import parse
import datetime

DEFAULT_PHONE_ATTRIBUTE_SET = 'Centralino'
DEFAULT_PHONE_PRODUCT = 'C01'
DEFAULT_PHONE_PRODUCT_TITLE = 'Centralino Base'
DEFAULT_PHONE_SUPPLIER = 'Telecom'
DEFAULT_EMPTY_SUPPLIER = 'Altro'
DEFAULT_TAX = 'IVA22'
DEFAULT_UNIT = 'PZ'
DEFAULT_UNIT_DESCRIPTION = 'Piece'

class Object(object):
    pass

def is_empty_string(s):
    return str(s).isspace() or not s

class Command(BaseCommand):
    help = 'Import Contact Data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-x',
            '--excel-file',
            dest='excel_file',
            type=str,
            help='Input Contacts Table as XLSX File.')  
        parser.add_argument(
            '-t',
            '--contact-type',
            dest='contact_type',
            type=str,
            help='Customer/Supplier')
        parser.add_argument(
            '-u',
            '--current-user',
            dest='current_user',
            type=str,
            help='Current user.')      
        return parser

    def handle(self, **options):
        excel_file = options.get('excel_file')       
        contact_type =  options.get('contact_type')
        user_id = options.get('current_user')    

        if not excel_file or len(excel_file) == 0:
            raise CommandError("Input Contacts '--excel_file' is mandatory")

        wb = xlrd.open_workbook(filename=excel_file)               

        sheet = wb.sheet_by_index(0)
        row_headers = sheet.row(0)        

        col_num = 0
        for idx, cell_obj in enumerate(row_headers):
            col_num += 1
        if col_num >= 0:  
            count = 0
            for row_num in range(1, sheet.nrows):  
                rating = str(sheet.cell(row_num, 3).value).strip()
                if rating != '6': #do not import rating 6
                    #Create generic object for Contact
                    contact = None
                    person = None
                    c = Object()
                    c.name = str(sheet.cell(row_num, 0).value).strip()
                    c.vatnumber = str(sheet.cell(row_num, 4).value).strip()
                    c.lastmodification = datetime.datetime.now()
                    c.lastmodifiedby = User.objects.get(id=user_id)

                    #Create instances of related Classes
                    pa = {}
                    pha_mobile = {}
                    pha_1 = {}
                    pha_2 = {}
                    pha_fax = {}
                    ea = {}

                    pa['prefix'] = sheet.cell(row_num, 15).value
                    pa['name'] = sheet.cell(row_num, 16).value
                    pa['prename'] = sheet.cell(row_num, 17).value
                    pa['addressline1'] = str(sheet.cell(row_num, 6).value).strip()
                    pa['addressline2'] = str(sheet.cell(row_num, 7).value).strip()
                    #pa['addressline3'] = sheet.cell(row_num, 0).value
                    #pa['addressline4'] = sheet.cell(row_num, 0).value
                    pa['zipcode'] = int(sheet.cell(row_num, 5).value) if not is_empty_string((sheet.cell(row_num, 5).value)) else 0
                    pa['town'] = sheet.cell(row_num, 8).value
                    pa['state'] = sheet.cell(row_num, 9).value
                    pa['country'] = sheet.cell(row_num, 10).value

                    pha_mobile['phone'] = sheet.cell(row_num, 11).value
                    pha_1['phone'] = sheet.cell(row_num, 12).value
                    pha_2['phone'] = sheet.cell(row_num, 13).value
                    pha_fax['phone'] = sheet.cell(row_num, 14).value
                    
                    prename = str(sheet.cell(row_num, 17).value)
                    if not is_empty_string(prename):
                        p = Object()
                        p.prefix = sheet.cell(row_num, 15).value
                        p.name = sheet.cell(row_num, 16).value
                        p.prename = prename
                        p.email = sheet.cell(row_num, 19).value
                        p.phone = sheet.cell(row_num, 11).value
                        p.role = sheet.cell(row_num, 18).value
                        
                        #person, created = Person.objects.update_or_create(vars(p))
                        try:
                            person = Person.objects.get(email=p.email)
                            for key, value in vars(p).items():
                                setattr(person, key, value)  
                            with transaction.atomic():
                                person.save()
                        except Person.DoesNotExist:
                            person = Person(**vars(p))
                            with transaction.atomic():
                                person.save()

                    ea['email'] = sheet.cell(row_num, 20).value

                    #Determine Contact Type (Customer or Supplier)
                    if contact_type == 'C':
                        isLead = str(sheet.cell(row_num, 1).value)
                        c.isLead = True if isLead == '1' else False
                        c.defaultCustomerBillingCycle = CustomerBillingCycle.objects.all()[:1].get()
                        customer_group = str(sheet.cell(row_num, 2).value).strip()
                        
                        try:
                            customer = Customer.objects.filter(name=c.name).first()
                            if customer is None:
                                #raise NameError("address fields: {} - {} - {}".format(pa.addressline1, pa.addressline2, pa.zipcode))
                                address_check = PostalAddressForContact.objects.get(addressline1=pa['addressline1'], addressline2=pa['addressline2'], zipcode=pa['zipcode'])
                                customer = Customer.objects.get(pk=address_check.company_id)
                                #raise NameError("nome del customer = {}".format(customer.name))
                            for key, value in vars(c).items():
                                setattr(customer, key, value)                    
                            with transaction.atomic():
                                customer.save()
                        except PostalAddressForContact.DoesNotExist:
                            #set date of creation only if new Entry
                            #raise NameError("customer non trovato: {}".format(c.name))
                            c.dateofcreation = datetime.datetime.now()
                            customer = Customer(**vars(c))
                            with transaction.atomic():
                                customer.save()
                        if customer_group != '':
                            group, created = CustomerGroup.objects.get_or_create(name=customer_group)
                            customer.ismemberof.add(group)
                        contact = customer
                    elif contact_type == 'S':
                        c.offersShipmentToCustomers = False
                        try:
                            supplier = Supplier.objects.get(name=c.name)
                            for key, value in vars(c).items():
                                setattr(supplier, key, value)                    
                            supplier.save()
                        except Supplier.DoesNotExist:
                            supplier = Supplier(**vars(c))
                            supplier.save()
                        contact = supplier
                    else:
                        raise CommandError("Cannot determine contact type")

                    #region products
                    #Phone system
                    #add phone system only if check field is true
                    if(sheet.cell(row_num, 27).value):
                        p_model = str(sheet.cell(row_num, 29).value) 
                        p_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
                        p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_PHONE_ATTRIBUTE_SET)
                        ps = {}
                        ps['product_number'] = p_model[:30] if not is_empty_string(p_model) else DEFAULT_PHONE_PRODUCT
                        ps['title'] = p_model if not is_empty_string(p_model) else DEFAULT_PHONE_PRODUCT_TITLE
                        ps['description'] = ''
                        ps['default_unit'] = p_unit
                        ps['tax'] = Tax.objects.get(name=DEFAULT_TAX)
                        ps['attribute_set'] = p_attribute_set

                        ps_product, created = Product.objects.update_or_create(**ps)

                        p_supplier = str(sheet.cell(row_num, 30).value) if not is_empty_string(str(sheet.cell(row_num, 30).value)) else DEFAULT_EMPTY_SUPPLIER
                        p_supplier_instance = Supplier.objects.get(name=p_supplier)
                        try:
                            p_expire_date = parse(str(sheet.cell(row_num, 35).value))
                        except ValueError:
                            p_expire_date = None
                        ps_phonesystemforcustomer, created = PhoneSystemForCustomer.objects.get_or_create(
                            customer=contact,
                            product=ps_product,
                        )
                        to_update = PhoneSystemForCustomer.objects.filter(pk=ps_phonesystemforcustomer.pk).update(
                            supplier=p_supplier_instance,
                            service_type='',
                            expire_date=p_expire_date,
                            year=str(sheet.cell(row_num, 28).value).strip(),
                            no_ext_lines=int(sheet.cell(row_num, 24).value) if not is_empty_string(sheet.cell(row_num, 24).value) else None,
                            no_int_lines=int(sheet.cell(row_num, 25).value) if not is_empty_string(sheet.cell(row_num, 25).value) else None,
                            maintainer=sheet.cell(row_num, 31).value
                        )
                        
                        #with transaction.atomic():
                            #ps_phonesystemforcustomer.save()

                    #Internet provider
                    ip = {}

                    #Phone provider
                    pp = {}

                    #Mobile provider
                    mb = {}


                    #endregion
                    
                    #Set objects from inlines
                    if pa['zipcode'] > 0:
                        pa['purpose'] = 'O'
                        pa['company'] = contact
                        postal_address, created = PostalAddressForContact.objects.update_or_create(**pa)
                        '''if created:
                            raise NameError("indirizzo creato: address = {} - contact id = {}".format(pa.addressline1, contact.pk))
                        else:
                            raise NameError("indirizzo aggiornato: address = {} - contact id = {}".format(pa.addressline1, contact.pk))'''

                    if not is_empty_string(pha_mobile['phone']):
                        pha_mobile['purpose'] = 'B'
                        pha_mobile['company'] = contact
                        phone_address_mobile = PhoneAddressForContact.objects.update_or_create(**pha_mobile)

                    if not is_empty_string(pha_1['phone']):
                        pha_1['purpose'] = 'O'
                        pha_1['company'] = contact
                        phone_address_1 = PhoneAddressForContact.objects.update_or_create(**pha_1)

                    if not is_empty_string(pha_2['phone']):
                        pha_2['purpose'] = 'O'
                        pha_2['company'] = contact
                        phone_address_2 = PhoneAddressForContact.objects.update_or_create(**pha_2)

                    if not is_empty_string(pha_fax['phone']):
                        pha_fax['purpose'] = 'F'
                        pha_fax['company'] = contact
                        phone_address_fax = PhoneAddressForContact.objects.update_or_create(**pha_fax)

                    if not is_empty_string(ea['email']):
                        ea['purpose'] = 'O'
                        ea['company'] = contact
                        email_address = EmailAddressForContact.objects.update_or_create(**ea)

                    if person:
                        ContactPersonAssociation.objects.update_or_create(contact=contact, person=person)

                    count += 1
                    print('imported contact {}'.format(contact.name))
                
        return '{}'.format(count)

    