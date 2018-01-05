# -*- coding: utf-8 -*-
from koalixcrm.crm.views import *
from koalixcrm.crm.documents.quote import OptionQuote
from koalixcrm.crm.documents.invoice import OptionInvoice
from koalixcrm.crm.documents.purchaseorder import OptionPurchaseOrder
from koalixcrm.crm.documents.contract import OptionContract
from koalixcrm.crm.product.tax import OptionTax
from koalixcrm.crm.product.unit import OptionUnit
from koalixcrm.crm.product.product import OptionProduct
from koalixcrm.crm.product.currency import OptionCurrency
from koalixcrm.crm.contact.customer import OptionCustomer
from koalixcrm.crm.contact.supplier import OptionSupplier
from koalixcrm.crm.contact.customergroup import OptionCustomerGroup
from koalixcrm.crm.contact.customerbillingcycle import OptionCustomerBillingCycle


admin.site.register(Customer, OptionCustomer)
admin.site.register(CustomerGroup, OptionCustomerGroup)
admin.site.register(Supplier, OptionSupplier)
admin.site.register(Quote, OptionQuote)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(Unit, OptionUnit)
admin.site.register(Currency, OptionCurrency)
admin.site.register(Tax, OptionTax)
admin.site.register(CustomerBillingCycle, OptionCustomerBillingCycle)
admin.site.register(Contract, OptionContract)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
admin.site.register(Product, OptionProduct)
