import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django import forms
from django.forms import models
from koalixcrm.crm.contact.data_import import ContactImportData
from koalixcrm.crm.tasks import import_contact_data

class ImportDataContactForm(models.ModelForm):

    class Meta:
        model = ContactImportData
        fields = ('contact_type', 'data_file',)

    def clean_data_file(self):
        file_xlsx = self.cleaned_data['data_file']
        path = default_storage.save('tmp/'+file_xlsx.name,
                                    ContentFile(file_xlsx.read()))
        
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        contact_type = self.cleaned_data['contact_type']
        current_user = self.current_user.id
        import_contact_data(tmp_file, contact_type, current_user)

        return file_xlsx