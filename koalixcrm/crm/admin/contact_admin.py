# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.crm.contact.customer import Customer, OptionCustomer
from koalixcrm.crm.contact.supplier import Supplier, OptionSupplier
from koalixcrm.crm.contact.customer_group import CustomerGroup, OptionCustomerGroup
from koalixcrm.crm.contact.customer_billing_cycle import CustomerBillingCycle, OptionCustomerBillingCycle
from koalixcrm.crm.contact.person import Person
from koalixcrm.crm.contact.contact import OptionPerson, CallForContact, VisitForContact
from koalixcrm.crm.contact.call import OptionCall, OptionVisit

admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
admin.site.register(Supplier, OptionSupplier)
admin.site.register(Person, OptionPerson)
admin.site.register(CallForContact, OptionCall)
admin.site.register(VisitForContact, OptionVisit)
