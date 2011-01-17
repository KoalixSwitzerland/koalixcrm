# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from shutil import copy
from os import path
from django.core.management.base import BaseCommand, CommandError
import djangoUserExtention
import crm
from filebrowser.fields import FileBrowseField
from filebrowser import settings

DEFAULT_FILE = 'dashboard.py'

class Command(BaseCommand):
    help = ('This Command is going to install the default Templates, given by the koalixcrm base installation, in your django instance. Be sure you first run syncdb')
    args = '[]'
    label = 'application name'

    def handle(self, **options):
      invoicetemplate = 'invoice.xsl'
      quotetemplate = 'quote.xsl'
      deliveryordertemplate = 'deliveryorder.xsl'
      purchaseordertemplate = 'purchaseordertemplate.xsl'
      purchaseconfirmationtemplate = 'purchaseconfirmation.xsl'
      balancesheettemplate = 'balancesheet.xsl'
      profitlossstatementtemplate = 'profitlossstatement.xls'
      listoftemplatefiles = {'invoice' : invoicetemplate, 
      'quote' : quotetemplate,
      'deliveryorder' : deliveryordertemplate,
      'purchaseconfirmation' : purchaseconfirmationtemplate,
      'balancesheet' : balancesheettemplate,
      'profitlossstatement' : profitlossstatementtemplate,
      }
      
      configfile = 'fontconfig.xml'
      logo = 'logo.jpg'
      listofadditionalfiles = ('dejavusans-bold.xml', 'dejavusans.xml', )
      if path.exists('templatefiles'):
        templateset = djangoUserExtention.models.TemplateSet()
        templateset.title = 'defaultTemplateSet'
        for template in listoftemplatefiles:
          if path.exists('templatefiles/'+listoftemplatefiles[template]):
            copy('templatefiles/'+listoftemplatefiles[template], settings.DIRECTORY+'templatefiles/'+listoftemplatefiles[template])
            xslfile = djangoUserExtention.models.XSLFile()
            xslfile.title(template)
            xslfile.title(settings.DIRECTORY+'templatefiles/'+listoftemplatefiles[template])
            xslfile.save()
            if template == 'invoice' :
              templateset.invoiceXSLFile = xslfile
            elif template == 'quote' :
              templateset.quoteXSLFile = xslfile
            elif template == 'purchaseconfirmation' :
              templateset.purchaseconfirmationXSLFile = xslfile
            elif template == 'deilveryorder' :
              templateset.deilveryorderXSLFile = xslfile
            elif template == 'profitlossstatement' :
              templateset.profitLossStatementXSLFile = xslfile
            elif template == 'balancesheet' :
              templateset.balancesheetXSLFile = xslfile
          else:
            raise FileNotFoundException
        templateset.logo = settings.DIRECTORY+'templatefiles/'+logo
        templateset.bankingaccountref = "xx-xxxxxx-x"
        templateset.addresser = _("undefined")
        templateset.fopConfigurationFile = configfile
        templateset.footerTextsalesorders = _("The following positions:")
        templateset.headerTextsalesorders = _("Thank you for your intrest in our company \n Best regards")
        templateset.headerTextpurchaseorders = _("We would like to order the following positions:")
        templateset.footerTextpurchaseorders = _("Best regards")
        templateset.pagefooterleft = _("Sample Company")
        templateset.pagefootermiddle = _("Sample Address")
        templateset.save()
        userExtention = djangoUserExtention.models.UserExtention()
        userExtention.defaultTemplateSet = templateset
        userExtention = Users.objects.all()[0]
        userExtention.save()
            
        for additionalfile in listofadditionalfiles:
          if os.path.exists('templatefiles'+additionalfile):
            shutil.copy('templatefiles'+additionalfile, settings.DIRECTORY+'templatefiles/')
       
