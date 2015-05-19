# -*- coding: utf-8 -*-
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse
from django.template import RequestContext, loader
from django_tables2 import SingleTableView, RequestConfig
from extra_views import UpdateWithInlinesView, InlineFormSet, NamedFormsetsMixin, CreateWithInlinesView
from crm_core.forms import *
from crm_core.models import *
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from tables import ContractTable, CustomerTable, SupplierTable, ProductTable, TaxTable, BillingCycleTable, UnitTable, \
    CustomerGroupTable, ProductCategoryTable


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
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy('dashboard'), permanent=True)

    return render_to_response('registration/login.html', context_instance=RequestContext(request))


def show_dashboard(request):
    contractcount = Contract.objects.all().count()
    invoicecount = Invoice.objects.all().count()
    customercount = Customer.objects.all().count()
    suppliercount = Supplier.objects.all().count()
    productcount = ProductItem.objects.all().count()
    opencontracts = []
    for contract in Contract.objects.exclude(state=20 or 100):
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
    taxtable = TaxTable(TaxRate.objects.all(), prefix="tax-")
    billingcycleable = BillingCycleTable(CustomerBillingCycle.objects.all(), prefix="billingcycle-")
    unittable = UnitTable(Unit.objects.all(), prefix="unit-")
    customergrouptable = CustomerGroupTable(CustomerGroup.objects.all(), prefix="customergroup-")
    productcategorytable = ProductCategoryTable(ProductCategory.objects.all(), prefix="productcategory-")
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
    customer = Customer.objects.get(pk=customer_pk)
    contract = customer.create_contract(request)
    if not customer.default_currency:
        return redirect('contract_edit', pk=contract.pk)
    return redirect('contract_detail', pk=contract.pk)


def create_quote_from_customer(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    quote = customer.create_quote(request)
    if not customer.default_currency:
        return redirect('contract_edit', pk=quote.contract.pk)
    return redirect('quote_edit', pk=quote.pk)


def create_purchaseorder_from_customer(request, customer_pk):
    customer = Customer.objects.get(pk=customer_pk)
    purchase_order = customer.create_purchase_order(request)
    if not customer.default_currency:
        return redirect('contract_edit', pk=purchase_order.contract.pk)
    return redirect('purchaseorder_edit', pk=purchase_order.pk)


def create_quote_from_contract(request, contract_pk):
    contract = Contract.objects.get(pk=contract_pk)
    quote = contract.create_quote()
    return redirect('quote_edit', pk=quote.pk)


def create_invoice_from_contract(request, contract_pk):
    contract = Contract.objects.get(pk=contract_pk)
    invoice = contract.create_invoice()
    return redirect('invoice_edit', pk=invoice.pk)


def create_purchaseorder_from_contract(request, contract_pk):
    contract = Contract.objects.get(pk=contract_pk)
    purchase_order = contract.create_purchase_order()
    return redirect('purchaseorder_edit', pk=purchase_order.pk)


def create_invoice_from_quote(request, quote_pk):
    quote = Quote.objects.get(pk=quote_pk)
    invoice = quote.create_invoice()
    return redirect('invoice_edit', pk=invoice.pk)


def create_purchaseorder_from_quote(request, quote_pk):
    quote = Quote.objects.get(pk=quote_pk)
    purchase_order = quote.create_purchase_order()
    return redirect('purchaseorder_edit', pk=purchase_order.pk)


# ###################
# ##   PDF Views   ##
# ###################


def view_quote_pdf(request, pk):
    quote = Quote.objects.get(pk=int(pk))
    with open(quote.pdf_path, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=quote.pdf'
        return response


def view_purchaseorder_pdf(request, pk):
    puchaseorder = PurchaseOrder.objects.get(pk=int(pk))
    with open(puchaseorder.pdf_path, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=puchaseorder.pdf'
        return response


def view_invoice_pdf(request, pk):
    invoice = Invoice.objects.get(pk=int(pk))
    with open(invoice.pdf_path, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=invoice.pdf'
        return response


# ###########################
# ##   Class Based Views   ##
# ###########################


class PurchaseOrderPositionInline(InlineFormSet):
    model = PurchaseOrderPosition
    extra = 5
    can_delete = True
    form_class = PurchaseOrderPositionInlineForm
    prefix = 'purchaseorderposition'


class SalesContractPositionInline(InlineFormSet):
    model = SalesContractPosition
    extra = 5
    can_delete = True
    form_class = SalesContractPositionInlineForm
    prefix = 'salescontractposition'


class PostalAddressInline(LoginRequiredMixin, PermissionRequiredMixin, InlineFormSet):
    model = PostalAddress
    permission_required = 'crm_core.view_postaladdress'
    raise_exception = False
    extra = 1
    can_delete = False
    fields = ['addressline1', 'addressline2', 'zipcode', 'city', 'state', 'country', 'purpose']


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


class ListCustomers(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL
    fields = ['name', 'firstname', 'billingcycle', 'ismemberof']
    table_class = CustomerTable
    table_data = Customer.objects.all()
    context_table_name = 'customertable'
    table_pagination = 10


class ViewCustomer(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Customer
    permission_required = 'crm_core.view_customer'
    login_url = settings.LOGIN_URL


class CreateCustomer(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Customer
    permission_required = 'crm_core.add_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'default_currency', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class EditCustomer(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Customer
    permission_required = 'crm_core.change_customer'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'firstname', 'default_currency', 'billingcycle', 'ismemberof']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('customer_list')


class DeleteCustomer(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Customer
    permission_required = 'crm_core.delete_customer'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('customer_list')


class ListSuppliers(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL
    fields = ['name', 'direct_shipment_to_customers']
    table_class = SupplierTable
    table_data = Supplier.objects.all()
    context_table_name = 'suppliertable'
    table_pagination = 10


class ViewSupplier(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Supplier
    permission_required = 'crm_core.view_supplier'
    login_url = settings.LOGIN_URL


class CreateSupplier(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Supplier
    permission_required = 'crm_core.add_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'default_currency', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class EditSupplier(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Supplier
    permission_required = 'crm_core.change_supplier'
    login_url = settings.LOGIN_URL
    fields = ['prefix', 'name', 'default_currency', 'direct_shipment_to_customers']
    inlines = [PostalAddressInline, PhoneAddressInline, EmailAddressInline]
    inlines_names = ['postaladdress_formset', 'phoneaddress_formset', 'emailaddress_formset']
    success_url = reverse_lazy('supplier_list')


class DeleteSupplier(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    permission_required = 'crm_core.delete_supplier'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('supplier_list')


class CreateTax(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TaxRate
    permission_required = 'crm_core.add_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditTax(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TaxRate
    permission_required = 'crm_core.change_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteTax(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TaxRate
    permission_required = 'crm_core.delete_tax'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class CreateUnit(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Unit
    permission_required = 'crm_core.add_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditUnit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Unit
    permission_required = 'crm_core.change_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteUnit(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Unit
    permission_required = 'crm_core.delete_unit'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class CreateProductCategory(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductCategory
    permission_required = 'crm_core.add_productcategory'
    login_url = settings.LOGIN_URL
    fields = ['title', 'description']
    success_url = reverse_lazy('settings')


class EditProductCategory(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductCategory
    permission_required = 'crm_core.change_productcategory'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteProductCategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductCategory
    permission_required = 'crm_core.delete_productcategory'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class ListProducts(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = ProductItem
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL
    table_class = ProductTable
    table_data = ProductItem.objects.all()
    context_table_name = 'producttable'
    table_pagination = 10


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductItem
    permission_required = 'crm_core.add_product'
    login_url = settings.LOGIN_URL
    fields = ['sku', 'title', 'image', 'description', 'unit_price', 'available', 'num_in_stock', 'item_unit',
              'item_tax', 'item_category', 'keywords', 'content', 'sale_price', 'sale_from', 'sale_to',
              'related_products', 'upsell_products', 'publish_date', 'expiry_date']
    success_url = reverse_lazy('product_list')


class EditProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductItem
    permission_required = 'crm_core.change_product'
    login_url = settings.LOGIN_URL
    fields = ['sku', 'title', 'image', 'description', 'unit_price', 'available', 'num_in_stock', 'item_unit',
              'item_tax', 'item_category', 'keywords', 'content', 'sale_price', 'sale_from', 'sale_to',
              'related_products', 'upsell_products', 'publish_date', 'expiry_date']
    success_url = reverse_lazy('product_list')


class ViewProduct(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ProductItem
    permission_required = 'crm_core.view_product'
    login_url = settings.LOGIN_URL


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductItem
    permission_required = 'crm_core.delete_product'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('product_list')


class CreateBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.add_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.change_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteBillingCycle(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerBillingCycle
    permission_required = 'crm_core.delete_customerbillingcycle'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditPurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithInlinesView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    inlines = [PurchaseOrderPositionInline]
    permission_required = 'crm_core.change_purchaseorder'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class DeletePurchaseOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PurchaseOrder
    permission_required = 'crm_core.delete_purchaseorder'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class CreateCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerGroup
    permission_required = 'crm_core.add_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class EditCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerGroup
    permission_required = 'crm_core.change_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class DeleteCustomerGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerGroup
    permission_required = 'crm_core.delete_customergroup'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('settings')


class ListContracts(LoginRequiredMixin, PermissionRequiredMixin, PaginatedTableView):
    model = Contract
    permission_required = 'crm_core.view_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier']
    object_list = Contract.objects.all().reverse().order_by('lastmodification')
    table_class = ContractTable
    table_data = Contract.objects.all()
    context_table_name = 'contracttable'
    table_pagination = 10


class ViewContract(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Contract
    permission_required = 'crm_core.view_contract'
    login_url = settings.LOGIN_URL


class CreateContract(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contract
    permission_required = 'crm_core.add_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier', 'default_currency']
    success_url = reverse_lazy('contract_list')


class EditContract(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contract
    permission_required = 'crm_core.change_contract'
    login_url = settings.LOGIN_URL
    fields = ['description', 'default_customer', 'default_supplier', 'default_currency']
    success_url = reverse_lazy('contract_list')


class DeleteContract(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Contract
    permission_required = 'crm_core.delete_contract'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class EditInvoice(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithInlinesView):
    model = Invoice
    form_class = InvoiceForm
    inlines = [SalesContractPositionInline]
    permission_required = 'crm_core.change_invoice'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'payableuntil', 'state', 'currency']
    success_url = reverse_lazy('contract_list')


class DeleteInvoice(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Invoice
    permission_required = 'crm_core.delete_invoice'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')


class CreateQuote(LoginRequiredMixin, PermissionRequiredMixin, CreateWithInlinesView):
    model = Quote
    inlines = [SalesContractPositionInline]
    form_class = QuoteForm
    permission_required = 'crm_core.add_quote'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'currency', 'lastmodifiedby',
              'last_calculated_price', 'last_pricing_date']
    success_url = reverse_lazy('contract_list')


class EditQuote(LoginRequiredMixin, PermissionRequiredMixin, UpdateWithInlinesView):
    model = Quote
    inlines = [SalesContractPositionInline]
    form_class = QuoteForm
    permission_required = 'crm_core.change_quote'
    login_url = settings.LOGIN_URL
    fields = ['description', 'contract', 'customer', 'currency', 'lastmodifiedby',
              'last_calculated_price', 'last_pricing_date']
    success_url = reverse_lazy('contract_list')


class DeleteQuote(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Quote
    permission_required = 'crm_core.delete_quote'
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy('contract_list')