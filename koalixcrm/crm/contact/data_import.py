from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.purpose import *

class ContactImportData(models.Model):
    data_file = models.FileField(upload_to='data_files', max_length=255)

    contact_type = models.CharField(verbose_name=_("Contact Type"), max_length=1, choices=CONTACTTYPE)

    def file_link(self):
        if self.data_file:
            return "<a href='%s'>download</a>" % (self.data_file.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True

    def __str__(self):
        return '{}'.format(self.data_file.name)

    class Meta:
        """
        """
        verbose_name = 'Contact: Import Data from XLSX file'
        verbose_name_plural = 'Contacts: Import Data from XLSX file'
