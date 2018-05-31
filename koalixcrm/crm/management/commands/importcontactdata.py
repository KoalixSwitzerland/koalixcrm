from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import re

from django.contrib.auth.models import User

from koalixcrm.crm.contact.contact import Contact, PostalAddressForContact, PhoneAddressForContact, EmailAddressForContact, ContactPersonAssociation, CallForContact
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.contact.customer import Customer, SwitchboardForCustomer, AnalogPhoneForCustomer, DigitalPhoneForCustomer, InternetForCustomer, MobileForCustomer
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.contact.customerbillingcycle import CustomerBillingCycle
from koalixcrm.crm.contact.customergroup import CustomerGroup
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.product.tax import Tax
from koalixcrm.crm.product.attribute import AttributeSet
from koalixcrm.crm.const.purpose import *
from koalixcrm.crm.const.contactimport import *

import xlrd
from xlrd.sheet import ctype_text
from dateutil.parser import parse
import datetime


class Object(object):
    pass

class Command(BaseCommand):
    help = 'Import Contact Data.'

    USERID = 0
    def set_user_id(self, user_id):
        with open('log.txt', 'w') as logfile:
            logfile.write("User id : %s" %  user_id)
        self.USERID = user_id

    def get_user_id(self):
        return self.USERID

    def format_phone_number(self, value):
        res = str(value).replace(" ", "")
        res = re.sub(r"^[a-zA-Z]+(\d+)$", r"\1", res)
        res = re.sub(r"^(\d+)[a-zA-Z]+$", r"\1", res)
        res = re.sub(r"\.0$", r"", res)
        return res

    def format_city_name(self, value):
        res = str(value).strip()
        res = re.sub(r"^(.*)\s?\([a-zA-Z]+\)$", r"\1", res)
        return res.title()

    def format_state_name(self, value):
        if str(value):
            return str(value).strip().upper()
        return value

    def format_int_string(self, value):
        if str(value):
            res = str(value).strip()
            res = re.sub(r".0$", r"", res)
            return res

    def prepare_product_args(self, product_type, sheet, row_num):
        DEFAULT_RETURN = None, None
        specific_product_args = None

        if product_type == PHONE_SYSTEM_P_TYPE:
            check_field = sheet.cell(row_num, HASSWITCHBOARD).value
            if not check_field: return DEFAULT_RETURN
            model_name = str(sheet.cell(row_num, SWITCHBOARDMODEL).value)
            
            p_product_number = model_name[:30] if model_name else DEFAULT_PHONE_PRODUCT
            p_title = model_name if model_name else DEFAULT_PHONE_PRODUCT_TITLE
            p_description = None
            p_default_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
            p_tax, created = Tax.objects.get_or_create(name=DEFAULT_TAX) 
            p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_PHONE_ATTRIBUTE_SET)
            supplier_name = str(sheet.cell(row_num, SWITCHBOARDPROVIDER).value) if str(sheet.cell(row_num, SWITCHBOARDPROVIDER).value) else DEFAULT_EMPTY_SUPPLIER
            p_service_type = DEFAULT_PHONE_SERVICE_TYPE
            try:
                p_expire_date = parse(str(sheet.cell(row_num, PHONEEXPIREDATE).value))
            except ValueError:
                p_expire_date = None
            p_year = str(sheet.cell(row_num, YEAROFINSTALLATION).value).strip()
            p_quantity = 1        
            p_maintainer = sheet.cell(row_num, MAINTAINER).value
            p_internal_lines = int(sheet.cell(row_num, INTERNALLINES).value) if sheet.cell(row_num, INTERNALLINES).value else 0
            p_external_lines = int(sheet.cell(row_num, EXTERNALLINES).value) if sheet.cell(row_num, EXTERNALLINES).value else 0

            specific_product_args = {
                'internal_lines': p_internal_lines,
                'external_lines': p_external_lines
            }
        
        elif product_type == ANALOG_PHONE_P_TYPE:
            check_field = sheet.cell(row_num, ANALOGPHONES).value
            if not check_field: return DEFAULT_RETURN
            model_name = str(sheet.cell(row_num, PHONEMANUFACTURER1).value)
            
            p_product_number = model_name[:30] if model_name else DEFAULT_PHONE_PRODUCT
            p_title = model_name if model_name else DEFAULT_PHONE_PRODUCT_TITLE
            p_description = None
            p_default_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
            p_tax, created = Tax.objects.get_or_create(name=DEFAULT_TAX)
            p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_PHONE_ATTRIBUTE_SET)
            supplier_name = str(sheet.cell(row_num, PHONEMANUFACTURER1).value) if str(sheet.cell(row_num, PHONEMANUFACTURER1).value) else DEFAULT_EMPTY_SUPPLIER
            p_service_type = DEFAULT_ANALOG_PHONE_SERVICE_TYPE
            p_expire_date = None
            p_year = None
            p_quantity = ANALOGPHONES
            p_maintainer = None

        elif product_type == DIGITAL_PHONE_P_TYPE:
            check_field = sheet.cell(row_num, DIGITALPHONES).value
            if not check_field: return DEFAULT_RETURN
            model_name = str(sheet.cell(row_num, PHONEMANUFACTURER1).value)
            
            p_product_number = model_name[:30] if model_name else DEFAULT_PHONE_PRODUCT2
            p_title = model_name if model_name else DEFAULT_PHONE_PRODUCT_TITLE2
            p_description = None
            p_default_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
            p_tax, created = Tax.objects.get_or_create(name=DEFAULT_TAX)
            p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_PHONE_ATTRIBUTE_SET2)
            supplier_name = str(sheet.cell(row_num, PHONEMANUFACTURER1).value) if str(sheet.cell(row_num, PHONEMANUFACTURER1).value) else DEFAULT_EMPTY_SUPPLIER
            p_service_type = DEFAULT_DIGITAL_PHONE_SERVICE_TYPE
            p_expire_date = None
            p_year = None
            p_quantity = DIGITALPHONES
            p_maintainer = None

        elif product_type == MOBILE_P_TYPE:
            check_field = sheet.cell(row_num, MOBILEPROVIDER).value
            if not check_field: return DEFAULT_RETURN
            model_name = str(sheet.cell(row_num, PHONEMANUFACTURER2).value)
            
            p_product_number = model_name[:30] if model_name else DEFAULT_PHONE_PRODUCT2
            p_title = model_name if model_name else DEFAULT_PHONE_PRODUCT_TITLE2
            p_description = None
            p_default_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
            p_tax, created = Tax.objects.get_or_create(name=DEFAULT_TAX)
            p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_PHONE_ATTRIBUTE_SET2)
            supplier_name = str(sheet.cell(row_num, PHONEMANUFACTURER2).value) if str(sheet.cell(row_num, PHONEMANUFACTURER2).value) else DEFAULT_EMPTY_SUPPLIER
            p_service_type = DEFAULT_MOBILE_SERVICE_TYPE
            p_expire_date = None
            p_year = None
            p_quantity = None
            p_maintainer = None

        elif product_type == INTERNET_P_TYPE:
            check_field = sheet.cell(row_num, TYPEOFINTERNETCONNECTION).value
            if not check_field: return DEFAULT_RETURN
            model_name = str(sheet.cell(row_num, TYPEOFINTERNETCONNECTION).value)

            p_product_number = model_name[:30] if model_name else DEFAULT_INTERNET_PRODUCT
            p_title = model_name if model_name else DEFAULT_INTERNET_PRODUCT_TITLE
            p_description = None
            p_default_unit, created = Unit.objects.get_or_create(short_name=DEFAULT_UNIT, description=DEFAULT_UNIT_DESCRIPTION)
            p_tax, created = Tax.objects.get_or_create(name=DEFAULT_TAX)
            p_attribute_set, created = AttributeSet.objects.get_or_create(name=DEFAULT_INTERNET_ATTRIBUTE_SET)
            supplier_name = str(sheet.cell(row_num, INTERNETPROVIDER).value) if str(sheet.cell(row_num, INTERNETPROVIDER).value) else DEFAULT_EMPTY_SUPPLIER
            p_service_type = DEFAULT_INTERNET_SERVICE_TYPE
            try:
                p_expire_date = parse(str(sheet.cell(row_num, INTERNETEXPIREDATE).value))
            except ValueError:
                p_expire_date = None
            p_year = str(sheet.cell(row_num, YEAROFINSTALLATION).value).strip(),
            p_quantity = 1
            p_maintainer = None


        product_args = {
            'product_number': p_product_number,
            'title': p_title,
            'description': p_description,
            'default_unit': p_default_unit,
            'tax': p_tax,
            'attribute_set': p_attribute_set
        }

        relation_args = {
            'supplier': self.get_or_create_supplier_by_name(supplier_name),
            'service_type': p_service_type,
            'quantity': p_quantity,
            'expire_date': p_expire_date,
            'year': p_year,
            'maintainer': p_maintainer
        }
        if specific_product_args:
            relation_args = { **relation_args, **specific_product_args }

        return product_args, relation_args

    
    def add_product(self, product_type, contact, sheet, row_num):
        product_args, relation_args = self.prepare_product_args(product_type, sheet, row_num)
        if product_args is None: return

        product, created = Product.objects.update_or_create(**product_args)
        if product_type == PHONE_SYSTEM_P_TYPE:
            switchboard, created = SwitchboardForCustomer.objects.get_or_create(
                customer=contact,
                product=product,
            )
            
            updated = SwitchboardForCustomer.objects.filter(pk=switchboard.pk).update(**relation_args)
        elif product_type == ANALOG_PHONE_P_TYPE:
            analogphone, created = AnalogPhoneForCustomer.objects.get_or_create(
                customer=contact,
                product=product,
            )
            updated = AnalogPhoneForCustomer.objects.filter(pk=analogphone.pk).update(**relation_args)
        elif product_type == DIGITAL_PHONE_P_TYPE:
            digitalphone, created = DigitalPhoneForCustomer.objects.get_or_create(
                customer=contact,
                product=product,
            )
            updated = DigitalPhoneForCustomer.objects.filter(pk=digitalphone.pk).update(**relation_args)
        elif product_type == MOBILE_P_TYPE:
            mobilephone, created = MobileForCustomer.objects.get_or_create(
                customer=contact,
                product=product,
            )
            updated = MobileForCustomer.objects.filter(pk=mobilephone.pk).update(**relation_args)
        elif product_type == INTERNET_P_TYPE:
            internet, created = InternetForCustomer.objects.get_or_create(
                customer=contact,
                product=product,
            )
            updated = InternetForCustomer.objects.filter(pk=internet.pk).update(**relation_args)


    def get_or_create_supplier_by_name(self, name):
        with open('log.txt', 'w') as logfile:
            logfile.write("get User id : %s" %  self.get_user_id())
        supplier_args = {
            'name': name,
            'lastmodifiedby': User.objects.get(id=self.get_user_id()),
            'vatnumber': '0',
            'offersShipmentToCustomers': False
        }
        supplier, created = Supplier.objects.get_or_create(**supplier_args)
        return supplier
    
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

        self.set_user_id(user_id)   

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
                #check rating
                if str(sheet.cell(row_num, RATING).value) != SKIP_ROW_VALUE:
                    #Create generic object for Contact
                    contact = None
                    person = None
                    c = Object()
                    c.name = str(sheet.cell(row_num, COMPANY).value).strip()
                    c.vatnumber = str(sheet.cell(row_num, VAT).value).strip()
                    c.lastmodification = datetime.datetime.now()
                    c.lastmodifiedby = User.objects.get(id=user_id)

                    #Initialize dictionaries for related Classes
                    pa = {}
                    pha_mobile = {}
                    pha_1 = {}
                    pha_2 = {}
                    pha_fax = {}
                    ea = {}
                    call = {}

                    _pa_prename = sheet.cell(row_num, LASTNAME).value
                    pa['prefix'] = sheet.cell(row_num, PERSONPREFIX).value
                    pa['name'] = sheet.cell(row_num, NAME).value
                    pa['addressline1'] = str(sheet.cell(row_num, ADDRESS).value).strip()
                    pa['addressline2'] = self.format_int_string(sheet.cell(row_num, ADDRESS_NO).value)
                    #pa['addressline3'] = sheet.cell(row_num, 0).value
                    #pa['addressline4'] = sheet.cell(row_num, 0).value
                    pa['zipcode'] = int(sheet.cell(row_num, ZIPCODE).value) if (sheet.cell(row_num, ZIPCODE).value) else 0
                    pa['town'] = self.format_city_name(sheet.cell(row_num, CITY).value)
                    pa['state'] = self.format_state_name(sheet.cell(row_num, STATE).value)
                    pa['country'] = sheet.cell(row_num, COUNTRY).value

                    _mobile = str(sheet.cell(row_num, MOBILE1).value)
                    _phone_1 = str(sheet.cell(row_num, PHONE1).value)
                    _phone_2 = str(sheet.cell(row_num, PHONE2).value)
                    _fax = str(sheet.cell(row_num, FAX).value)
                    pha_mobile['phone'] = self.format_phone_number(_mobile)[:20]
                    pha_1['phone'] = self.format_phone_number(_phone_1)[:20]
                    pha_2['phone'] = self.format_phone_number(_phone_2)[:20]
                    pha_fax['phone'] = self.format_phone_number(_fax)[:20]
                    
                    #create record for Person if prename and email found
                    prename = str(sheet.cell(row_num, LASTNAME).value)
                    email = str(sheet.cell(row_num, PERSONEMAIL).value)
                    if prename and email:
                        person, created = Person.objects.get_or_create(email=email)
                        person.prefix = sheet.cell(row_num, PERSONPREFIX).value
                        person.name = sheet.cell(row_num, NAME).value
                        person.prename = prename
                        person.phone = self.format_phone_number(_mobile)[:20]
                        person.role = sheet.cell(row_num, ROLE).value
                        with transaction.atomic():
                            person.save()

                    ea['email'] = sheet.cell(row_num, COMPANYEMAIL).value

                    #Determine Contact Type (Customer or Supplier)
                    if contact_type == 'C':
                        isLead = str(sheet.cell(row_num, ISLEAD).value)
                        c.isLead = isLead == '1'
                        c.defaultCustomerBillingCycle = CustomerBillingCycle.objects.all()[:1].get()
                        customer_group = str(sheet.cell(row_num, TYPEOFACTIVITY).value).strip()
                        
                        try:
                            customer = Customer.objects.get(name__iexact=c.name.lower())
                            for key, value in vars(c).items():
                                setattr(customer, key, value)                    
                            with transaction.atomic():
                                customer.save()
                        except Customer.DoesNotExist:
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

                        #region products
                        #Switchboard
                        self.add_product(PHONE_SYSTEM_P_TYPE, contact, sheet, row_num)

                        #Analog phones
                        self.add_product(ANALOG_PHONE_P_TYPE, contact, sheet, row_num)

                        #Digital phones
                        self.add_product(DIGITAL_PHONE_P_TYPE, contact, sheet, row_num)

                        #Internet provider
                        self.add_product(INTERNET_P_TYPE, contact, sheet, row_num)

                        #Phone provider
                        pp = {}

                        #Mobile provider
                        mb = {}
                        self.add_product(MOBILE_P_TYPE, contact, sheet, row_num)

                        #endregion
                        
                        #Set objects from inlines
                        if pa['zipcode'] > 0:
                            pa['purpose'] = 'O'
                            pa['company'] = contact
                            postal_address, created = PostalAddressForContact.objects.get_or_create(company=contact, purpose='O', prename=_pa_prename)
                            updated = PostalAddressForContact.objects.filter(pk=postal_address.pk).update(**pa)

                        if pha_mobile['phone']:
                            pha_mobile['purpose'] = 'B'
                            pha_mobile['company'] = contact
                            phone_address_mobile = PhoneAddressForContact.objects.update_or_create(**pha_mobile)

                        if pha_1['phone']:
                            pha_1['purpose'] = 'O'
                            pha_1['company'] = contact
                            phone_address_1 = PhoneAddressForContact.objects.update_or_create(**pha_1)

                        if pha_2['phone']:
                            pha_2['purpose'] = 'O'
                            pha_2['company'] = contact
                            phone_address_2 = PhoneAddressForContact.objects.update_or_create(**pha_2)

                        if pha_fax['phone']:
                            pha_fax['purpose'] = 'F'
                            pha_fax['company'] = contact
                            phone_address_fax = PhoneAddressForContact.objects.update_or_create(**pha_fax)

                        if ea['email']:
                            ea['purpose'] = 'O'
                            ea['company'] = contact
                            email_address = EmailAddressForContact.objects.update_or_create(**ea)

                        #create a call to report existing notes on Lead
                        if str(sheet.cell(row_num, MEETINGNOTES).value):
                            call['description'] = str(sheet.cell(row_num, MEETINGNOTES).value)
                            call['status'] = 'D'
                            call['purpose'] = 'S'
                            call['company'] = contact
                            call_for_contact = CallForContact.objects.update_or_create(**call)

                        if person:
                            ContactPersonAssociation.objects.update_or_create(contact=contact, person=person)

                        count += 1
                        print('imported contact {}'.format(contact.name))

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
                
        return '{}'.format(count)

    