# -*- coding: utf-8 -*-

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse
from django.template import RequestContext, loader
from django_tables2 import SingleTableView, RequestConfig
from extra_views import UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin, CreateWithInlinesView
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from crm_core.custom.mixins import UpdateWithModifiedByMixin, CreateWithModifieByMixin, \
    CreateWithInlinesAndModifiedByMixin, UpdateWithInlinesAndModifiedByMixin
from crm_core import forms, models
from tables import ContractTable, CustomerTable, SupplierTable, ProductTable, TaxTable, BillingCycleTable, UnitTable, \
    CustomerGroupTable, ProductCategoryTable
from cartridge.shop import models as cartridge_models
from django.conf import settings


# ###################
# ##   Base Views  ##
# ###################

class PaginatedTableView(SingleTableView):

    def __init__(self, **kwargs):
        super(PaginatedTableView, self).__init__(**kwargs)
        self.object_list = self.model.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        config = RequestConfig(request)
        table = self.table_class(self.object_list)
        config.configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=self.table_pagination)
        context[self.context_table_name] = table
        return self.render_to_response(context)


# ######################
# ##   Helper Views   ##
# ######################

def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy('dashboard'), permanent=True)

    return render_to_response('registration/login.html', context_instance=RequestContext(request))


def show_dashboard(request):
    contractcount = models.Contract.objects.all().count()
    invoicecount = models.Invoice.objects.all().count()
    customercount = models.Customer.objects.all().count()
    suppliercount = models.Supplier.objects.all().count()
    productcount = cartridge_models.Product.objects.all().count()
    opencontracts = []
    for contract in models.Contract.objects.exclude(state=20 or 100):
        if contract not in opencontracts:
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


def show_settings(request):
    config = RequestConfig(request)
    template = loader.get_template('settings.html')
    taxtable = TaxTable(models.TaxRate.objects.all(), prefix="tax-")
    billingcycleable = BillingCycleTable(models.CustomerBillingCycle.objects.all(), prefix="billingcycle-")
    unittable = UnitTable(models.Unit.objects.all(), prefix="unit-")
    customergrouptable = CustomerGroupTable(models.CustomerGroup.objects.all(), prefix="customergroup-")
    productcategorytable = ProductCategoryTable(cartridge_models.Category.objects.all(), prefix="productcategory-")
    config.configure(taxtable)
    config.configure(billingcycleable)
    config.configure(unittable)
    config.configure(customergrouptable)
    config.configure(productcategorytable)
    taxtable.paginate(page=request.GET.get('page', 1), per_page=5)
    billingcycleable.paginate(page=request.GET.get('page', 1), per_page=5)
    unittable.paginate(page=request.GET.get('page', 1), per_page=5)
    customergrouptable.paginate(page=request.GET.get('page', 1), per_page=5)
    productcategorytable.paginate(page=request.GET.get('page', 1), per_page=5)
    context = RequestContext(request, {
        'taxtable': taxtable,
        'billingcycletable': billingcycleable,
        'unittable': unittable,
        'customergrouptable': customergrouptable,
        'productcategorytable': productcategorytable
    })
    return HttpResponse(template.render(context))


# ##############################
# ##   CRM Functional Views   ##
# ##############################


def create_contract_from_customer(request, customer_pk):
    customer = models.Customer.objects.get(pk=customer_pk)
    contract = customer.create_contract(request)
    if not customer.default_currency:
        return redirect('contract_edit', pk=contract.pk)
    return redirect('contract_detail', pk=contract.pk)


def create_quote_from_contract(request, contract_pk):
    contract = models.Contract.objects.get(pk=contract_pk)
    quote = contract.create_quote()
    return redirect('quote_edit', pk=quote.pk)


def create_invoice_from_contract(request, contract_pk):
    contract = models.Contract.objects.get(pk=contract_pk)
    invoice = contract.create_invoice()
    return redirect('invoice_edit', pk=invoice.pk)


def create_purchaseorder_from_contract(request, contract_pk):
    contract = models.Contract.objects.get(pk=contract_pk)
    purchase_order = contract.create_purchase_order()
    return redirect('purchaseorder_edit', pk=purchase_order.pk)


# ########################
# ##   Document Views   ##
# ########################


def view_quote_details(request, pk):
    quote = models.Quote.objects.get(pk=int(pk))
    # return HttpResponse(quote.to_html())
    pdf = open(quote.pdf_path, 'rb')
    return HttpResponse(pdf.read(), content_type='application/pdf')


def view_purchaseorder_details(request, pk):
    puchaseorder = models.PurchaseOrder.objects.get(pk=int(pk))
    # return HttpResponse(puchaseorder.to_html())
    pdf = open(puchaseorder.pdf_path, 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    return response


def view_invoice_details(request, pk):
    invoice = models.Invoice.objects.get(pk=int(pk))
    # return HttpResponse(invoice.to_html())
    pdf = open(invoice.pdf_path, 'rb')
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    return response


# ###########################
# ##   Class Based Views   ##
# ###########################

class CustomerPostalAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.CustomerPostalAddress
    permission_required = 'crm_core.view_postaladdress'
    raise_exception = False
    extra = 1
    can_delete = False
    fields = ['addressline1', 'addressline2', 'zipcode', 'city', 'state', 'country', 'purpose']


class SupplierPostalAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.SupplierPostalAddress
    permission_required = 'crm_core.view_postaladdress'
    raise_exception = False
    extra = 1
    can_delete = False
    fields = ['addressline1', 'addressline2', 'zipcode', 'city', 'state', 'country', 'purpose']


class CustomerPhoneAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.CustomerPhoneAddress
    permission_required = 'crm_core.view_phoneaddress'
    raise_exception = False
    extra = 1
    max_num = 4
    can_delete = False
    fields = ['phone', 'purpose']


class SupplierPhoneAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.SupplierPhoneAddress
    permission_required = 'crm_core.view_phoneaddress'
    raise_exception = False
    extra = 1
    max_num = 4
    can_delete = False
    fields = ['phone', 'purpose']


class CustomerEmailAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.CustomerEmailAddress
    permission_required = 'crm_core.view_emailaddress'
    raise_exception = False
    extra = 1
    max_num = 2
    can_delete = False
    fields = ['email', 'purpose']


class SupplierEmailAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = models.SupplierEmailAddress
    permission_required = 'crm_core.view_emailaddress'
    raise_exception = False
    extra = 1
    max_num = 2
    can_delete = False
    fields = ['email', 'purpose']


class UserExtensionInline(InlineFormSet):
    model = models.UserExtension
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()


class ProductUnitInline(InlineFormSet):
    model = models.ProductUnit
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()


class ProductTaxInline(InlineFormSet):
    model = models.ProductTax
    extra = 1
    max_num = 1
    can_delete = False
    exclude = ()


class UpdateUserProfile(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = User
    inlines = [UserExtensionInline, ]
    inlines_names = ['userprofile_formset']
    fields = ['first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'groups']
    success_url = reverse_lazy('home')


class ListCustomers(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL
    fields = ['name', 'firstname', 'billingcycle', 'ismemberof']
    table_class = CustomerTable
    table_data = models.Customer.objects.all()
    context_table_name = 'customertable'
    table_pagination = 10


class ViewCustomer(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL


class CreateCustomer(LoginRequiredMixin, PermissionRequiredMixin,
                     NamedFormsetsMixin, CreateWithInlinesAndModifiedByMixin):
    model = models.Customer
    permission_required = 'crm_core.add_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'default_currency', 'billingcycle', 'ismemberof']
    inlines = [CustomerPostalAddressInline, CustomerPhoneAddressInline, CustomerEmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class EditCustomer(LoginRequiredMixin, PermissionRequiredMixin,
                   NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Customer
    permission_required = 'crm_core.change_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'default_currency', 'billingcycle', 'ismemberof']
    inlines = [CustomerPostalAddressInline, CustomerPhoneAddressInline, CustomerEmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class DeleteCustomer(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Customer
    permission_required = 'crm_core.delete_customer'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customer_list')


class ListSuppliers(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name', 'direct_shipment_to_customers']
    table_class = SupplierTable
    table_data = models.Supplier.objects.all()
    context_table_name = 'suppliertable'
    table_pagination = 10


class ViewSupplier(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL


class CreateSupplier(LoginRequiredMixin, PermissionRequiredMixin,
                     NamedFormsetsMixin, CreateWithInlinesAndModifiedByMixin):
    model = models.Supplier
    permission_required = 'crm_core.add_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'default_currency', 'direct_shipment_to_customers']
    inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class EditSupplier(LoginRequiredMixin, PermissionRequiredMixin,
                   NamedFormsetsMixin, UpdateWithInlinesAndModifiedByMixin):
    model = models.Supplier
    permission_required = 'crm_core.change_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'default_currency', 'direct_shipment_to_customers']
    inlines = [SupplierPostalAddressInline, SupplierPhoneAddressInline, SupplierEmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class DeleteSupplier(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Supplier
    permission_required = 'crm_core.delete_supplier'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('supplier_list')


class CreateTax(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.TaxRate
    permission_required = 'crm_core.add_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')
    fields = ['taxrate_in_percent', 'name']


class EditTax(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.TaxRate
    permission_required = 'crm_core.change_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')
    fields = ['taxrate_in_percent', 'name']


class DeleteTax(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.TaxRate
    permission_required = 'crm_core.delete_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class CreateUnit(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Unit
    permission_required = 'crm_core.add_unit'
    fields = ['shortname', 'description', 'fractionof', 'factor']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditUnit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Unit
    permission_required = 'crm_core.change_unit'
    fields = ['shortname', 'description', 'fractionof', 'factor']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteUnit(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Unit
    permission_required = 'crm_core.delete_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class CreateProductCategory(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = cartridge_models.Category
    permission_required = 'crm_core.add_productcategory'
    login_url = settings.LOGIN_URL
    fields = ['title', 'description']
    success_url = reverse_lazy('settings')


class EditProductCategory(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = cartridge_models.Category
    permission_required = 'crm_core.change_productcategory'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteProductCategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = cartridge_models.Category
    permission_required = 'crm_core.delete_productcategory'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class ListProducts(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = cartridge_models.Product
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL
    table_class = ProductTable
    table_data = cartridge_models.Product.objects.all()
    context_table_name = 'producttable'
    table_pagination = 10


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = cartridge_models.Product
    permission_required = 'crm_core.add_product'
    login_url = settings.LOGIN_URL
    inlines = [ProductUnitInline, ProductTaxInline]
    inlines_names = ['productunit_formset', 'producttax_formset']
    success_url = reverse_lazy('product_list')
    form_class = forms.ProductForm


class EditProduct(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = cartridge_models.Product
    permission_required = 'crm_core.change_product'
    login_url = settings.LOGIN_URL
    inlines = [ProductUnitInline, ProductTaxInline]
    inlines_names = ['productunit_formset', 'producttax_formset']
    success_url = reverse_lazy('product_list')
    form_class = forms.ProductForm


class ViewProduct(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = cartridge_models.Product
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = cartridge_models.Product
    permission_required = 'crm_core.delete_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('product_list')


class CreateBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.CustomerBillingCycle
    permission_required = 'crm_core.add_customerbillingcycle'
    fields = ['name', 'days_to_payment', 'prefix']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.CustomerBillingCycle
    permission_required = 'crm_core.change_customerbillingcycle'
    fields = ['name', 'days_to_payment', 'prefix']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.CustomerBillingCycle
    permission_required = 'crm_core.delete_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditPurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithModifiedByMixin):
    model = models.PurchaseOrder
    form_class = forms.PurchaseOrderForm
    permission_required = 'crm_core.change_purchaseorder'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')

    def get_context_data(self, **kwargs):
        context = super(EditPurchaseOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            context['position_formset'] = forms.PositionFormSet(self.request.POST)
        else:
            purchaseorder_cart = models.PurchaseOrder.objects.get(pk=context.get('object').pk).cart
            formset = forms.PositionFormSet(instance=purchaseorder_cart)
            context['position_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        quote_cart = models.PurchaseOrder.objects.get(pk=kwargs.get('pk')).cart
        formset = forms.PositionFormSet(request.POST, request.FILES, instance=quote_cart)
        if formset.is_valid():
            formset.save()
        return super(EditPurchaseOrder, self).post(request, *args, **kwargs)


class DeletePurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.PurchaseOrder
    permission_required = 'crm_core.delete_purchaseorder'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class CreateCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.CustomerGroup
    permission_required = 'crm_core.add_customergroup'
    fields = ['name']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.CustomerGroup
    permission_required = 'crm_core.change_customergroup'
    fields = ['name']
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.CustomerGroup
    permission_required = 'crm_core.delete_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class ListContracts(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = models.Contract
    permission_required = 'crm_core.view_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier']
    object_list = models.Contract.objects.all().reverse().order_by('lastmodification')
    table_class = ContractTable
    table_data = models.Contract.objects.all()
    context_table_name = 'contracttable'
    table_pagination = 10


class ViewContract(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Contract
    permission_required = 'crm_core.view_contract'
    login_url = settings.LOGIN_URL


class CreateContract(LoginRequiredMixin, PermissionRequiredMixin, CreateWithModifieByMixin):
    model = models.Contract
    permission_required = 'crm_core.add_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier', 'default_currency']
    success_url = reverse_lazy('contract_list')


class EditContract(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithModifiedByMixin):
    model = models.Contract
    permission_required = 'crm_core.change_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier', 'default_currency']
    success_url = reverse_lazy('contract_list')


class DeleteContract(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Contract
    permission_required = 'crm_core.delete_contract'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class EditInvoice(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithModifiedByMixin):
    model = models.Invoice
    form_class = forms.InvoiceForm
    permission_required = 'crm_core.change_invoice'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')

    def get_context_data(self, **kwargs):
        context = super(EditInvoice, self).get_context_data(**kwargs)
        if self.request.POST:
            context['position_formset'] = forms.PositionFormSet(self.request.POST)
        else:
            invoice_cart = models.Invoice.objects.get(pk=context.get('object').pk).cart
            formset = forms.PositionFormSet(instance=invoice_cart)
            context['position_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        invoice_cart = models.Invoice.objects.get(pk=kwargs.get('pk')).cart
        formset = forms.PositionFormSet(request.POST, request.FILES, instance=invoice_cart)
        if formset.is_valid():
            formset.save()
        return super(EditInvoice, self).post(request, *args, **kwargs)


class DeleteInvoice(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Invoice
    permission_required = 'crm_core.delete_invoice'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class EditQuote(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithModifiedByMixin):
    model = models.Quote
    form_class = forms.QuoteForm
    permission_required = 'crm_core.change_quote'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')

    def get_context_data(self, **kwargs):
        context = super(EditQuote, self).get_context_data(**kwargs)
        if self.request.POST:
            context['position_formset'] = forms.PositionFormSet(self.request.POST)
        else:
            quote_cart = models.Quote.objects.get(pk=context.get('object').pk).cart
            formset = forms.PositionFormSet(instance=quote_cart)
            context['position_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        quote_cart = models.Quote.objects.get(pk=kwargs.get('pk')).cart
        formset = forms.PositionFormSet(request.POST, request.FILES, instance=quote_cart)
        if formset.is_valid():
            formset.save()
        return super(EditQuote, self).post(request, *args, **kwargs)


class DeleteQuote(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Quote
    permission_required = 'crm_core.delete_quote'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')
