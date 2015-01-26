# coding=utf-8
from django import forms
from crispy_forms.helper import FormHelper
from models import PurchaseOrder, PurchaseOrderPosition, SalesContractPosition, Quote


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['description', 'currency', 'external_reference']

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
        self.helper = FormHelper()
        self.helper.form_tag = False


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote
        fields = ['description', 'currency', 'external_reference']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.TextInput()
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