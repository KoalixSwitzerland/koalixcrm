# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from shutil import copy
from os import path
from os import mkdir
from django.core.management.base import BaseCommand, CommandError
import djangoUserExtention
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from filebrowser.settings import DIRECTORY
from filebrowser.settings import MEDIA_ROOT
from settings import PROJECT_ROOT

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
      profitlossstatementtemplate = 'profitlossstatement.xsl'
      listoftemplatefiles = {'invoice' : invoicetemplate, 
      'quote' : quotetemplate,
      'deliveryorder' : deliveryordertemplate,
      'purchaseconfirmation' : purchaseconfirmationtemplate,
      'balancesheet' : balancesheettemplate,
      'profitlossstatement' : profitlossstatementtemplate,
      }
      
      configfile = 'fontconfig.xml'
      dejavusansfile = 'dejavusans-bold.xml'
      dejavusansboldfile = 'dejavusans.xml'
      logo = 'logo.jpg'
      copy('templatefiles/generic/'+configfile, MEDIA_ROOT+DIRECTORY+'templatefiles/'+configfile)
      copy('templatefiles/generic/'+logo, MEDIA_ROOT+DIRECTORY+'templatefiles/'+logo)
      copy('templatefiles/generic/'+dejavusansfile, MEDIA_ROOT+DIRECTORY+'templatefiles/'+dejavusansfile)
      copy('templatefiles/generic/'+dejavusansboldfile, MEDIA_ROOT+DIRECTORY+'templatefiles/'+dejavusansboldfile)
      listofadditionalfiles = ('dejavusans-bold.xml', 'dejavusans.xml', )
      if path.exists('templatefiles'):
        templateset = djangoUserExtention.models.TemplateSet()
        templateset.title = 'defaultTemplateSet'
        if (path.exists(MEDIA_ROOT+DIRECTORY+'templatefiles') == False):
          mkdir(MEDIA_ROOT+DIRECTORY+'templatefiles')
        for template in listoftemplatefiles:
          if path.exists(PROJECT_ROOT+'templatefiles/en/'+listoftemplatefiles[template]):
            copy('templatefiles/en/'+listoftemplatefiles[template], MEDIA_ROOT+DIRECTORY+'templatefiles/'+listoftemplatefiles[template])
            xslfile = djangoUserExtention.models.XSLFile()
            xslfile.title = template
            xslfile.xslfile = DIRECTORY+'templatefiles/'+listoftemplatefiles[template]
            xslfile.save()
            if template == 'invoice' :
              templateset.invoiceXSLFile = xslfile
            elif template == 'quote' :
              templateset.quoteXSLFile = xslfile
            elif template == 'purchaseconfirmation' :
              templateset.purchaseconfirmationXSLFile = xslfile
            elif template == 'deliveryorder' :
              templateset.deilveryorderXSLFile = xslfile
            elif template == 'profitlossstatement' :
              templateset.profitLossStatementXSLFile = xslfile
            elif template == 'balancesheet' :
              templateset.balancesheetXSLFile = xslfile
            print(listoftemplatefiles[template])
          else:
            print(listoftemplatefiles)
            print(listoftemplatefiles[template])
            print(template)
            print(MEDIA_ROOT+DIRECTORY+'templatefiles/'+listoftemplatefiles[template])
            raise FileNotFoundException
        templateset.logo = DIRECTORY+'templatefiles/'+logo
        templateset.bankingaccountref = "xx-xxxxxx-x"
        templateset.addresser = _("John Smit, Sample Company, 8976 Smallville")
        templateset.fopConfigurationFile = DIRECTORY+'templatefiles/'+configfile
        templateset.headerTextsalesorders = _("According to your wishes the contract consists of the following positions:")
        templateset.footerTextsalesorders = _("Thank you for your interest in our company \n Best regards")
        templateset.headerTextpurchaseorders = _("We would like to order the following positions:")
        templateset.footerTextpurchaseorders = _("Best regards")
        templateset.pagefooterleft = _("Sample Company")
        templateset.pagefootermiddle = _("Sample Address")
        templateset.save()
        userExtention = djangoUserExtention.models.UserExtention()
        userExtention.defaultTemplateSet = templateset
        userExtention.user = User.objects.all()[0]
        userExtention.save()
        postaladdress = djangoUserExtention.models.UserExtentionPostalAddress()
        postaladdress.purpose = 'H'
        postaladdress.name = "John"
        postaladdress.prename = "Smith"
        postaladdress.addressline1 = "Ave 1"
        postaladdress.zipcode = 899887
        postaladdress.town = "Smallville"
        postaladdress.userExtention = userExtention
        postaladdress.save()
        phoneaddress = djangoUserExtention.models.UserExtentionPhoneAddress()
        phoneaddress.phone = "1293847"
        phoneaddress.purpose = 'H'
        phoneaddress.userExtention = userExtention
        phoneaddress.save()
        emailaddress = djangoUserExtention.models.UserExtentionEmailAddress()
        emailaddress.email = "john.smith@smallville.com"
        emailaddress.purpose = 'H'
        emailaddress.userExtention = userExtention
        emailaddress.save()
            
        for additionalfile in listofadditionalfiles:
          if path.exists('templatefiles'+additionalfile):
            shutil.copy('templatefiles'+additionalfile, DIRECTORY+'templatefiles/')
       
