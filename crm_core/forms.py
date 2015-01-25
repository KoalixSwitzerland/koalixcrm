# coding=utf-8
from django import forms
from crispy_forms.helper import FormHelper
from models import PurchaseOrder, PurchaseOrderPosition


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['contract', 'customer', 'description', 'currency']

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
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