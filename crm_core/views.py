# -*- coding: utf-8 -*-
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse
from django.template import RequestContext, loader
from extra_views import UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin, CreateWithInlinesView
from crm_core.const.states import InvoiceStatesEnum

from crm_core.models import Customer, Invoice, Supplier, Currency, Unit, Tax, Contract, Product, CustomerBillingCycle, \
    PurchaseOrder, CustomerGroup, Quote, PostalAddress, PhoneAddress, EmailAddress, UserExtension
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy('dashboard'))
    return render_to_response('registration/login.html', context_instance=RequestContext(request))


def show_dashboard(request):
    contractcount = Contract.objects.all().count()
    invoicecount = Invoice.objects.all().count()
    customercount = Customer.objects.all().count()
    suppliercount = Supplier.objects.all().count()
    productcount = Product.objects.all().count()
    opencontracts = []
    for invoice in Invoice.objects.all():
        if invoice.state != InvoiceStatesEnum.Payed or invoice.state != InvoiceStatesEnum.Deleted:
            opencontracts.append(invoice.contract)
    for contract in Contract.objects.all():
        opencontracts.append(contract)
    template = loader.get_template('dashboard.html')
    context = RequestContext(request, {
        'contractcount': contractcount,
        'invoicecount': invoicecount,
        'customercount': customercount,
        'suppliercount': suppliercount,
        'productcount': productcount,
        'opencontracts': opencontracts,
    })
    return HttpResponse(template.render(context))


class PostalAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = PostalAddress
    permission_required = 'crm_core.view_postaladdress'
    raise_exception = False
    extra = 1
    can_delete = False
    fields = ['addressline1', 'addressline2', 'zipcode', 'town', 'state', 'country', 'purpose']


class PhoneAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = PhoneAddress
    permission_required = 'crm_core.view_phoneaddress'
    raise_exception = False
    extra = 1
    max_num = 4
    can_delete = False
    fields = ['phone', 'purpose']


class EmailAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = EmailAddress
    permission_required = 'crm_core.view_emailaddress'
    raise_exception = False
    extra = 1
    max_num = 2
    can_delete = False
    fields = ['email', 'purpose']


class UserExtensionInline(InlineFormSet):
    model = UserExtension
    extra = 1
    max_num = 1
    can_delete = False


class UpdateUserProfile(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = User
    inlines = [UserExtensionInline, ]
    inlines_names = ['userprofile_formset']
    fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups']
    success_url = reverse_lazy('home')


class ListCustomers(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL
    fields = ['name', 'firstname', 'billingcycle', 'ismemberof']


class ViewCustomer(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL


class CreateCustomer(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Customer
    permission_required = 'crm_core.add_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class EditCustomer(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Customer
    permission_required = 'crm_core.change_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class DeleteCustomer(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Customer
    permission_required = 'crm_core.delete_customer'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customer_list')


class ListSuppliers(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name', 'direct_shipment_to_customers']


class ViewSupplier(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL


class CreateSupplier(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Supplier
    permission_required = 'crm_core.add_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class EditSupplier(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Supplier
    permission_required = 'crm_core.change_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class DeleteSupplier(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    permission_required = 'crm_core.delete_supplier'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('supplier_list')


class ListCurrencies(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Currency
    permission_required = 'crm_core.view_currency'
    login_url = settings.LOGIN_URL


class CreateCurrency(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Currency
    permission_required = 'crm_core.add_currency'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('currency_list')


class EditCurrency(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Currency
    permission_required = 'crm_core.change_currency'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('currency_list')


class DeleteCurrency(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Currency
    permission_required = 'crm_core.delete_currency'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('currency_list')


class ListTaxes(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tax
    permission_required = 'crm_core.view_tax'
    login_url = settings.LOGIN_URL


class CreateTax(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tax
    permission_required = 'crm_core.add_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('tax_list')


class EditTax(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Tax
    permission_required = 'crm_core.change_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('tax_list')


class DeleteTax(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tax
    permission_required = 'crm_core.delete_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('tax_list')


class ListUnits(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Unit
    permission_required = 'crm_core.view_unit'
    login_url = settings.LOGIN_URL


class CreateUnit(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Unit
    permission_required = 'crm_core.add_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('unit_list')


class EditUnit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Unit
    permission_required = 'crm_core.change_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('unit_list')


class DeleteUnit(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Unit
    permission_required = 'crm_core.delete_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('unit_list')


class ListProducts(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL
    fields = ['product_number', 'product_title', 'product_description', 'defaultunit', 'tax', 'accoutingProductCategorie']


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = 'crm_core.add_product'
    login_url = settings.LOGIN_URL
    fields = ['product_number', 'product_title', 'product_description', 'defaultunit', 'tax', 'accoutingProductCategorie']
    success_url = reverse_lazy('product_list')


class EditProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'crm_core.change_product'
    login_url = settings.LOGIN_URL
    fields = ['product_number', 'product_title', 'product_description', 'defaultunit', 'tax', 'accoutingProductCategorie']
    success_url = reverse_lazy('product_list')


class ViewProduct(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'crm_core.delete_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('product_list')


class ListBillingCycles(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.view_customerbillingcycles'
    login_url = settings.LOGIN_URL


class CreateBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.add_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customerbillingcycle_list')


class EditBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.change_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customerbillingcycle_list')


class DeleteBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.delete_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customerbillingcycle_list')


class ListPurchaseOrders(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PurchaseOrder
    permission_required = 'crm_core.view_purchaseorder'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'supplier', 'state', 'currency', 'lastCalculatedPrice', 'lastPricingDate', ]


class CreatePurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PurchaseOrder
    permission_required = 'crm_core.add_purchaseorder'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'supplier', 'state', 'currency', ]
    success_url = reverse_lazy('purchaseorder_list')


class EditPurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PurchaseOrder
    permission_required = 'crm_core.change_purchaseorder'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'supplier', 'state', 'currency', ]
    success_url = reverse_lazy('purchaseorder_list')


class DeletePurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PurchaseOrder
    permission_required = 'crm_core.delete_purchaseorder'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('purchaseorder_list')


class ListCustomerGroups(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CustomerGroup
    permission_required = 'crm_core.view_customergroup'
    login_url = settings.LOGIN_URL


class CreateCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerGroup
    permission_required = 'crm_core.add_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customergroup_list')


class EditCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerGroup
    permission_required = 'crm_core.change_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customergroup_list')


class DeleteCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerGroup
    permission_required = 'crm_core.delete_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customergroup_list')


class ListContracts(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Contract
    permission_required = 'crm_core.view_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']


class CreateContract(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contract
    permission_required = 'crm_core.add_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']
    success_url = reverse_lazy('contract_list')


class EditContract(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contract
    permission_required = 'crm_core.change_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'defaultcustomer', 'defaultSupplier', 'defaultcurrency']
    success_url = reverse_lazy('contract_list')


class DeleteContract(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Contract
    permission_required = 'crm_core.delete_contract'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class ListInvoice(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Invoice
    permission_required = 'crm_core.view_invoice'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency', 'lastCalculatedPrice',
              'lastPricingDate']


class CreateInvoice(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Invoice
    permission_required = 'crm_core.add_invoice'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency']
    success_url = reverse_lazy('invoice_list')


class EditInvoice(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Invoice
    permission_required = 'crm_core.change_invoice'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency']
    success_url = reverse_lazy('invoice_list')


class DeleteInvoice(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Invoice
    permission_required = 'crm_core.delete_invoice'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('invoice_list')


class ListQuotes(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Quote
    permission_required = 'crm_core.view_quote'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']


class CreateQuote(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Quote
    permission_required = 'crm_core.add_quote'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']
    success_url = reverse_lazy('quote_list')


class EditQuote(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Quote
    permission_required = 'crm_core.change_quote'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'currency', 'validuntil', 'state', 'lastmodifiedby',
              'lastCalculatedPrice', 'lastPricingDate']
    success_url = reverse_lazy('quote_list')


class DeleteQuote(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Quote
    permission_required = 'crm_core.delete_quote'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('quote_list')