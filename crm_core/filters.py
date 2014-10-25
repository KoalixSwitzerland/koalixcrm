import django_filters
from crm_core.models import Customer


class CustomerFilter(django_filters.FilterSet):

    class Meta():
        model = Customer
        fields = ['name', 'firstname', 'addresses__town', 'addresses__zipcode']