# -*- coding: utf-8 -*-

from os import mkdir
from os import path
from shutil import copy

from apps import crm
from apps import djangoUserExtension
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.conf import settings

DEFAULT_FILE = 'dashboard.py'


class Command(BaseCommand):
    help = (
    'This Command is going to install the default Templates, given by the koalixcrm base installation, in your django instance. Be sure you first run syncdb')
    args = '[]'
    label = 'application name'

    def handle(self, *args, **options):
        invoicetemplate = 'invoice.xsl'
        quotetemplate = 'quote.xsl'
        deliveryordertemplate = 'deliveryorder.xsl'
        purchaseordertemplate = 'purchaseorder.xsl'
        purchaseconfirmationtemplate = 'purchaseconfirmation.xsl'
        balancesheettemplate = 'balancesheet.xsl'
        profitlossstatementtemplate = 'profitlossstatement.xsl'
        listoftemplatefiles = {'invoice': invoicetemplate,
                               'quote': quotetemplate,
                               'deliveryorder': deliveryordertemplate,
                               'purchaseconfirmation': purchaseconfirmationtemplate,
                               'purchaseorder': purchaseordertemplate,
                               'balancesheet': balancesheettemplate,
                               'profitlossstatement': profitlossstatementtemplate,
                               }

        configfile = 'fontconfig.xml'
        dejavusansfile = 'dejavusans-bold.xml'
        dejavusansboldfile = 'dejavusans.xml'
        logo = 'logo.jpg'
        listofadditionalfiles = ('dejavusans-bold.xml', 'dejavusans.xml',)
        if path.exists('apps/templatefiles'):
            templateset = djangoUserExtension.models.TemplateSet()
            templateset.title = 'defaultTemplateSet'
            if (path.exists(settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles') == False):
                mkdir(settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles')
            copy(settings.PROJECT_ROOT + '/apps/templatefiles/generic/' + configfile,
                 settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + configfile)
            copy(settings.PROJECT_ROOT + '/apps/templatefiles/generic/' + logo,
                 settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + logo)
            copy(settings.PROJECT_ROOT + '/apps/templatefiles/generic/' + dejavusansfile,
                 settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + dejavusansfile)
            copy(settings.PROJECT_ROOT + '/apps/templatefiles/generic/' + dejavusansboldfile,
                 settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + dejavusansboldfile)
            for template in listoftemplatefiles:
                if path.exists(settings.PROJECT_ROOT + '/apps/templatefiles/en/' + listoftemplatefiles[template]):
                    copy(settings.PROJECT_ROOT + '/apps/templatefiles/en/' + listoftemplatefiles[template],
                         settings.MEDIA_ROOT + settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + listoftemplatefiles[template])
                    xslfile = djangoUserExtension.models.XSLFile()
                    xslfile.title = template
                    xslfile.xslfile = settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + listoftemplatefiles[template]
                    xslfile.save()
                    if template == 'invoice':
                        templateset.invoiceXSLFile = xslfile
                    elif template == 'quote':
                        templateset.quoteXSLFile = xslfile
                    elif template == 'purchaseconfirmation':
                        templateset.purchaseconfirmationXSLFile = xslfile
                    elif template == 'purchaseorder':
                        templateset.purchaseorderXSLFile = xslfile
                    elif template == 'deliveryorder':
                        templateset.deilveryorderXSLFile = xslfile
                    elif template == 'profitlossstatement':
                        templateset.profitLossStatementXSLFile = xslfile
                    elif template == 'balancesheet':
                        templateset.balancesheetXSLFile = xslfile
                    print(listoftemplatefiles[template])
                else:
                    print(listoftemplatefiles)
                    print(listoftemplatefiles[template])
                    print(template)
                    print(settings.PROJECT_ROOT + 'apps/templatefiles/en/' + listoftemplatefiles[template])
                    raise FileNotFoundException
            templateset.logo = settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + logo
            templateset.bankingaccountref = "xx-xxxxxx-x"
            templateset.addresser = _("John Smit, Sample Company, 8976 Smallville")
            templateset.fopConfigurationFile = settings.FILEBROWSER_DIRECTORY + 'templatefiles/' + configfile
            templateset.headerTextsalesorders = _(
                "According to your wishes the contract consists of the following positions:")
            templateset.footerTextsalesorders = _("Thank you for your interest in our company \n Best regards")
            templateset.headerTextpurchaseorders = _("We would like to order the following positions:")
            templateset.footerTextpurchaseorders = _("Best regards")
            templateset.pagefooterleft = _("Sample Company")
            templateset.pagefootermiddle = _("Sample Address")
            templateset.save()
            currency = crm.models.Currency()
            currency.description = "US Dollar"
            currency.shortName = "USD"
            currency.rounding = "0.10"
            currency.save()
            userExtension = djangoUserExtension.models.UserExtension()
            userExtension.defaultTemplateSet = templateset
            userExtension.defaultCurrency = currency
            userExtension.user = User.objects.all()[0]
            userExtension.save()
            postaladdress = djangoUserExtension.models.UserExtensionPostalAddress()
            postaladdress.purpose = 'H'
            postaladdress.name = "John"
            postaladdress.prename = "Smith"
            postaladdress.addressline1 = "Ave 1"
            postaladdress.zipcode = 899887
            postaladdress.town = "Smallville"
            postaladdress.userExtension = userExtension
            postaladdress.save()
            phoneaddress = djangoUserExtension.models.UserExtensionPhoneAddress()
            phoneaddress.phone = "1293847"
            phoneaddress.purpose = 'H'
            phoneaddress.userExtension = userExtension
            phoneaddress.save()
            emailaddress = djangoUserExtension.models.UserExtensionEmailAddress()
            emailaddress.email = "john.smith@smallville.com"
            emailaddress.purpose = 'H'
            emailaddress.userExtension = userExtension
            emailaddress.save()

            for additionalfile in listofadditionalfiles:
                if path.exists(settings.PROJECT_ROOT + '/apps/templatefiles' + additionalfile):
                    copy(settings.PROJECT_ROOT + '/apps/templatefiles' + additionalfile, settings.FILEBROWSER_DIRECTORY + 'templatefiles/')
