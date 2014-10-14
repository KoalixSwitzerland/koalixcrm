from django.forms.models import inlineformset_factory
from crm.models import PostalAddress, Contact, PhoneAddress, EmailAddress

PostalAddressFormSet = inlineformset_factory(Contact, PostalAddress, extra=1, fields=[
    'addressline1', 'addressline2', 'zipcode', 'town', 'state', 'country', 'purpose'])
PhoneAddressFormSet = inlineformset_factory(Contact, PhoneAddress, extra=1, fields=['phone', 'purpose'])
EmailAddressFormSet = inlineformset_factory(Contact, EmailAddress , extra=1)