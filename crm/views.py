# -*- coding: utf-8 -*-
from os import path
from subprocess import CalledProcessError
from django.contrib.auth.models import User

from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse_lazy
from django.forms import ModelForm
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from crm.models import Customer, Invoice, Supplier, Currency, Unit, Tax, Contract, Product, CustomerBillingCycle, \
    PurchaseOrder, CustomerGroup, Quote, PostalAddress
from crm.forms import PostalAddressFormSet, PhoneAddressFormSet, EmailAddressFormSet


class ListCustomers(ListView):
    model = Customer
    fields = ['name', 'firstname', 'billingcycle', 'ismemberof']


class CreateCustomer(CreateView):
    model = Customer
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    success_url = reverse_lazy('customer_list')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        postal_address_form = PostalAddressFormSet()
        phone_address_form = PhoneAddressFormSet()
        email_address_form = EmailAddressFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  postal_address_form=postal_address_form,
                                  phone_address_form=phone_address_form,
                                  email_address_form=email_address_form))

    def post(self, request, *args, **kwargs):
        print request.POST
        customer = Customer()
        customer.lastmodifiedby = User.objects.get(username=request.user)
        customer.name = request.POST['name']
        customer.billingcycle = CustomerBillingCycle.objects.get(pk=int(request.POST['billingcycle']))
        customer.firstname = request.POST['prename']
        customer.save()
        postal_adress = PostalAddress()
        postal_adress.addressline1 = request.POST['']
        postal_adress.person = customer
        postal_adress.save()
        return redirect(reverse_lazy('customer_list'))


class EditCustomer(UpdateView):
    model = Customer
    fields = ['prefix', 'name', 'firstname', 'billingcycle', 'ismemberof']
    # success_url = reverse_lazy('list_customers')
    #
    # def get(self, request, *args, **kwargs):
    #     """
    #     Handles GET requests and instantiates blank versions of the form
    #     and its inline formsets.
    #     """
    #     self.object = Customer.objects.get(pk=int(kwargs['pk']))
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     postal_address_form = PostalAddressFormSet()
    #     phone_address_form = PhoneAddressFormSet()
    #     email_address_form = EmailAddressFormSet()
    #     context = self.get_context_data(pk=int(kwargs['pk']),
    #                                     form=form,
    #                                     postal_address_form=postal_address_form,
    #                                     phone_address_form=phone_address_form,
    #                                     email_address_form=email_address_form)
    #     return self.render_to_response(context)
    #
    # def post(self, request, *args, **kwargs):
    #     print request
    #     object = get_object_or_404(Customer, pk=int(kwargs['pk']))
    #     form = ModelForm(request.POST or None, instance=object)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('list_customers')
    #     return self.render_to_response(self.get_context_data(form=form))
    #     self.object = Customer.objects.get(pk=int(kwargs['pk']))
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     return super(UpdateView, self).post(request, *args, **kwargs)

class DeleteCustomer(DeleteView):
    model = Customer
    # success_url = reverse_lazy('list_customers')


class ListSuppliers(ListView):
    model = Supplier


class CreateSupplier(CreateView):
    model = Supplier
    success_url = reverse_lazy('list_suppliers')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        postal_address_form = PostalAddressFormSet()
        phone_address_form = PhoneAddressFormSet()
        email_address_form = EmailAddressFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  postal_address_form=postal_address_form,
                                  phone_address_form=phone_address_form,
                                  email_address_form=email_address_form))


class EditSupplier(UpdateView):
    model = Supplier
    success_url = reverse_lazy('list_suppliers')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        postal_address_form = PostalAddressFormSet()
        phone_address_form = PhoneAddressFormSet()
        email_address_form = EmailAddressFormSet()
        context = self.get_context_data(pk=int(kwargs['pk']),
                                        form=form,
                                        postal_address_form=postal_address_form,
                                        phone_address_form=phone_address_form,
                                        email_address_form=email_address_form)
        return self.render_to_response(context)


class DeleteSupplier(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_suppliers')


class ListCurrencies(ListView):
    model = Currency


class CreateCurrency(CreateView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class EditCurrency(UpdateView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class DeleteCurrency(DeleteView):
    model = Currency
    success_url = reverse_lazy('currency_list')


class ListTaxes(ListView):
    model = Tax


class CreateTax(CreateView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class EditTax(UpdateView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class DeleteTax(DeleteView):
    model = Tax
    success_url = reverse_lazy('tax_list')


class ListUnits(ListView):
    model = Unit


class CreateUnit(CreateView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class EditUnit(UpdateView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class DeleteUnit(DeleteView):
    model = Unit
    success_url = reverse_lazy('unit_list')


class ListProducts(ListView):
    model = Product
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


class ListBillingCycles(ListView):
    model = CustomerBillingCycle


class CreateBillingCycle(CreateView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class EditBillingCycle(UpdateView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class DeleteBillingCycle(DeleteView):
    model = CustomerBillingCycle
    success_url = reverse_lazy('billingcycle_list')


class ListPurchaseOrders(ListView):
    model = PurchaseOrder
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


class ListCustomerGroups(ListView):
    model = CustomerGroup


class CreateCustomerGroup(CreateView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class EditCustomerGroup(UpdateView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class DeleteCustomerGroup(DeleteView):
    model = CustomerGroup
    success_url = reverse_lazy('customergroup_list')


class ListContracts(ListView):
    model = Contract
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


class ListInvoice(ListView):
    model = Invoice
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


class ListQuotes(ListView):
    model = Quote
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


def export_pdf(calling_model_admin, request, where_to_create_from, what_to_create, redirect_to):
    """This method exports PDFs provided by different Models in the crm application

        Args:
          calling_model_admin (ModelAdmin):  The calling ModelAdmin must be provided for error message response.
          request: The request User is to know where to save the error message
          where_to_create_from (Model):  The model from which a PDF should be exported
          what_to_create (str): What document Type that has to be
          redirect_to (str): String that describes to where the method sould redirect in case of an error

        Returns:
              HTTpResponse with a PDF when successful
              HTTpResponseRedirect when not successful

        Raises:
          raises Http404 exception if anything goes wrong"""
    try:
        pdf = where_to_create_from.create_pdf(what_to_create)
        response = HttpResponse(FileWrapper(file(pdf)), mimetype='application/pdf')
        response['Content-Length'] = path.getsize(pdf)
    except Exception, e:  # (TemplateSetMissing, UserExtensionMissing, CalledProcessError), e:
        # if type(e) == UserExtensionMissing:
        # response = HttpResponseRedirect(redirect_to)
        # calling_model_admin.message_user(request, _("User Extension Missing"))
        # elif type(e) == TemplateSetMissing:
        # response = HttpResponseRedirect(redirect_to)
        #     calling_model_admin.message_user(request, _("Templateset Missing"))
        if type(e) == CalledProcessError:
            response = HttpResponseRedirect(redirect_to)
            calling_model_admin.message_user(request, e.output)
        else:
            raise Http404
    return response


def selectaddress(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    address = invoice.contract
  

  
   