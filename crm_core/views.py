# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from extra_views import UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin, CreateWithInlinesView
from braces.views import LoginRequiredMixin

from crm_core.models import Customer, Invoice, Supplier, Currency, Unit, Tax, Contract, Product, CustomerBillingCycle, \
    PurchaseOrder, CustomerGroup, Quote, PostalAddress, PhoneAddress, EmailAddress


class PostalAddressInline(InlineFormSet):
    model = PostalAddress
    extra = 1
    can_delete = False
    fields = ['addressline1', 'addressline2', 'zipcode', 'town', 'state', 'country', 'purpose']


class PhoneAddressInline(InlineFormSet):
    model = PhoneAddress
    extra = 1
    max_num = 4
    can_delete = False
    fields = ['phone', 'purpose']


class EmailAddressInline(InlineFormSet):
    model = EmailAddress
    extra = 1
    max_num = 2
    can_delete = False
    fields = ['email', 'purpose']


class ListCustomers(ListView, LoginRequiredMixin):
    model = Customer
    login_url = '/login/'
    fields = ['name', 'firstname', 'billingcycle', 'ismemberof']


class CreateCustomer(NamedFormsetsMixin, CreateWithInlinesView):
    model = Customer
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class EditCustomer(NamedFormsetsMixin, UpdateWithInlinesView):
    model = Customer
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class DeleteCustomer(DeleteView):
    model = Customer
    success_url = reverse_lazy('list_customers')


class ListSuppliers(ListView, LoginRequiredMixin):
    model = Supplier
    login_url = '/login/'


class CreateSupplier(NamedFormsetsMixin, CreateWithInlinesView):
    model = Supplier
    fields = ['prefix', 'name', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class EditSupplier(NamedFormsetsMixin, UpdateWithInlinesView):
    model = Supplier
    fields = ['prefix', 'name', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class DeleteSupplier(DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier_list')


class ListCurrencies(ListView, LoginRequiredMixin):
    model = Currency
    login_url = '/login/'


class CreateCurrency(CreateView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class EditCurrency(UpdateView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class DeleteCurrency(DeleteView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class ListTaxes(ListView, LoginRequiredMixin):
    model = Tax
    login_url = '/login/'


class CreateTax(CreateView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class EditTax(UpdateView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class DeleteTax(DeleteView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class ListUnits(ListView, LoginRequiredMixin):
    model = Unit
    login_url = '/login/'


class CreateUnit(CreateView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class EditUnit(UpdateView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class DeleteUnit(DeleteView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class ListProducts(ListView, LoginRequiredMixin):
    model = Product
    login_url = '/login/'
    fields = ['product_number', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie']


class CreateProduct(CreateView):
    model = Product
    fields = ['product_number', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie']
    success_url = reverse_lazy('product_list')


class EditProduct(UpdateView):
    model = Product
    fields = ['product_number', 'title', 'description', 'defaultunit', 'tax', 'accoutingProductCategorie']
    success_url = reverse_lazy('product_list')


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class ListBillingCycles(ListView, LoginRequiredMixin):
    model = CustomerBillingCycle
    login_url = '/login/'


class CreateBillingCycle(CreateView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class EditBillingCycle(UpdateView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class DeleteBillingCycle(DeleteView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class ListPurchaseOrders(ListView, LoginRequiredMixin):
    model = PurchaseOrder
    login_url = '/login/'
    fields = ['description', 'contract', 'supplier', 'state', 'currency', 'lastCalculatedPrice', 'lastPricingDate', ]


class CreatePurchaseOrder(CreateView):
    model = PurchaseOrder
    fields = ['description', 'contract', 'supplier', 'state', 'currency', ]
    success_url = reverse_lazy('purchaseorder_list')


class EditPurchaseOrder(UpdateView):
    model = PurchaseOrder
    fields = ['description', 'contract', 'supplier', 'state', 'currency', ]
    success_url = reverse_lazy('purchaseorder_list')


class DeletePurchaseOrder(DeleteView):
    model = PurchaseOrder
    success_url = reverse_lazy('purchaseorder_list')


class ListCustomerGroups(ListView, LoginRequiredMixin):
    model = CustomerGroup
    login_url = '/login/'


class CreateCustomerGroup(CreateView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class EditCustomerGroup(UpdateView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class DeleteCustomerGroup(DeleteView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class ListContracts(ListView, LoginRequiredMixin):
    model = Contract
    login_url = '/login/'
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']


class CreateContract(CreateView):
    model = Contract
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']
    success_url = reverse_lazy('contract_list')


class EditContract(UpdateView):
    model = Contract
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']
    success_url = reverse_lazy('contract_list')


class DeleteContract(DeleteView):
    model = Contract
    success_url = reverse_lazy('contract_list')


class ListInvoice(ListView, LoginRequiredMixin):
    model = Invoice
    login_url = '/login/'
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency', 'lastCalculatedPrice',
              'lastPricingDate']


class CreateInvoice(CreateView):
    model = Invoice
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency']
    success_url = reverse_lazy('invoice_list')


class EditInvoice(UpdateView):
    model = Invoice
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency']
    success_url = reverse_lazy('invoice_list')


class DeleteInvoice(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice_list')


class ListQuotes(ListView, LoginRequiredMixin):
    model = Quote
    login_url = '/login/'
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']


class CreateQuote(CreateView):
    model = Quote
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']
    success_url = reverse_lazy('quote_list')


class EditQuote(UpdateView):
    model = Quote
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']
    success_url = reverse_lazy('quote_list')


class DeleteQuote(DeleteView):
    model = Quote
    success_url = reverse_lazy('quote_list')