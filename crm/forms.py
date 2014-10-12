from django.forms.models import inlineformset_factory
from .models import PostalAddress, Contact

PostalAddressFormSet = inlineformset_factory(Contact, PostalAddress)