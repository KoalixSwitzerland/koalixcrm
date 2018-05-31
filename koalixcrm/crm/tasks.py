import io

from celery import shared_task
from django.conf import settings
from django.core.management import call_command

from koalixcrm.crm.contact.customer import Customer
from koalixcrm.crm.contact.supplier import Supplier

def import_contact_data(input_file, contact_type, current_user):
    _import_contact_data.delay(input_file, contact_type, current_user)

@shared_task
def _import_contact_data(input_file, contact_type, current_user):
    out = io.StringIO()
    contact = None
    try:
        call_command('importcontactdata',
            excel_file=input_file,
            contact_type=contact_type,
            current_user=str(current_user),
            stdout=out)
        value = out.getvalue()
        print('Number of contacts imported: {}'.format(value))
    
    except ValueError as e:
        value = None
        if contact is not None:
            contact.set_error()
        error_message = "Sorry, the input file is not valid: {}".format(e)
        raise
   
        