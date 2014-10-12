from django.forms.models import inlineformset_factory
from crm.models import PostalAddress, Contact, PhoneAddress, EmailAddress

PostalAddressFormSet = inlineformset_factory(Contact, PostalAddress, extra=1)
PhoneAddressFormSet = inlineformset_factory(Contact, PhoneAddress, extra=1)
EmailAddressFormSet = inlineformset_factory(Contact, EmailAddress, extra=1)