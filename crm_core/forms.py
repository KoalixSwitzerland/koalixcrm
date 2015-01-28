# coding=utf-8
from datetimewidget.widgets import DateWidget
from django import forms
from crispy_forms.helper import FormHelper
from models import PurchaseOrder, PurchaseOrderPosition, SalesContractPosition, Quote, Invoice


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['currency', 'external_reference', 'description']

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_tag = False


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ['currency', 'external_reference', 'description']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_tag = False


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['currency', 'payableuntil', 'external_reference', 'description']

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.fields['payableuntil'] = forms.DateField(widget=DateWidget(bootstrap_version=3, usel10n=True))
        self.helper = FormHelper()
        self.helper.form_tag = False


class PurchaseOrderPositionInlineForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrderPosition
        fields = ['quantity', 'description', 'discount', 'product', 'unit']

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderPositionInlineForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_tag = False


class SalesContractPositionInlineForm(forms.ModelForm):

    class Meta:
        model = SalesContractPosition
        fields = ['quantity', 'description', 'discount', 'product', 'unit']

    def __init__(self, *args, **kwargs):
        super(SalesContractPositionInlineForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_tag = False