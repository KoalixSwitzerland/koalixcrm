import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from crm import models
from filebrowser import settings

DEFAULT_FILE = 'dashboard.py'

class Command(BaseCommand):
    help = ('This Command is going to install the default Templates, given by the koalixcrm base installation, in your
django instance. Be sure you first run syncdb')
    args = '[]'
    label = 'application name'

    def handle(self, **options):
      listofxslflistoftemplatefilesiles = ['balancesheet.xsl', 'profitlossstatement.xsl', 'invoice.xsl', 'deliveryorder.xsl', 'profitlossstatement.xsl', 'purchaseconfirmation.xsl',  'quote.xsl']
      listofconfigfiles = ['dejavusans-bold.xml', 'dejavusans.xml', 'fontconfig.xml']
      listofadditionalfiles = ['logo.jpg',]
      if os.path.exists('templatefiles'):
        for template in listoftemplatefiles:
          if os.path.exists('templatefiles'+template):
            os.path.copy('templatefiles'+additionalfile, settings.DIRECTORY+'templatefiles/')
        for configfile in listofconfigfiles:
          if os.path.exists('templatefiles'+configfile):
            os.path.copy('templatefiles'+additionalfile, settings.DIRECTORY+'templatefiles/')
        for additionalfile in listofadditionalfiles:
          if os.path.exists('templatefiles'+additionalfile):
            os.path.copy('templatefiles'+additionalfile, settings.DIRECTORY+'templatefiles/')

