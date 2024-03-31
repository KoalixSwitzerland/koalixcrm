# -*- coding: utf-8 -*-

from os import path

from koalixcrm import crm
from koalixcrm import djangoUserExtension
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from filebrowser.base import FileObject
from django.utils.translation import gettext as _
from django.conf import settings

DEFAULT_FILE = 'dashboard.py'


class Command(BaseCommand):
    help = (
    'This Command is going to install the default Templates, given by the koalixcrm base installation, in your django instance. Be sure you first run syncdb')
    args = '[]'
    label = 'application name'

    @staticmethod
    def store_default_template_xsl_file(language, file_name):
        file_path = Command.path_of_default_template_file(language, file_name)
        xsl_file = Command.store_xsl_file(file_path)
        return xsl_file

    @staticmethod
    def path_of_default_template_file(language, file_name):
        file_path = path.join(settings.STATIC_ROOT, "default_templates", language, file_name)
        f = None;
        try:
            f = open(file_path,'r')
        except (FileNotFoundError) as e:
            print(_("File not found:") + file_path)
            print(_("Run collectstatic command and fix potential errors"))
        finally:
            if f is not None:
                f.close()
        return file_path

    @staticmethod
    def store_xsl_file(xsl_file_path):
        xsl_file = djangoUserExtension.models.XSLFile()
        xsl_file.title = path.basename(xsl_file_path)
        xsl_file.xslfile = FileObject(xsl_file_path)
        xsl_file.save()
        return xsl_file

    def handle(self, *args, **options):
        template_set = djangoUserExtension.models.TemplateSet()
        template_set.title = 'default_template_set'
        template_set.invoiceXSLFile = Command.store_default_template_xsl_file("en", "invoice.xsl")
        template_set.quoteXSLFile = Command.store_default_template_xsl_file("en", "quote.xsl")
        template_set.purchaseconfirmationXSLFile = Command.store_default_template_xsl_file("en", "purchaseconfirmation.xsl")
        template_set.purchaseorderXSLFile = Command.store_default_template_xsl_file("en", "purchaseorder.xsl")
        template_set.deilveryorderXSLFile = Command.store_default_template_xsl_file("en", "deliveryorder.xsl")

        if 'koalixcrm.accounting' in settings.INSTALLED_APPS:
            template_set.profitLossStatementXSLFile = Command.store_default_template_xsl_file("en", "profitlossstatement.xsl")
            template_set.balancesheetXSLFile = Command.store_default_template_xsl_file("en", "balancesheet.xsl")

        template_set.logo = FileObject(Command.path_of_default_template_file("generic", "logo.jpg"))
        template_set.fopConfigurationFile = FileObject(Command.path_of_default_template_file("generic", "fontconfig.xml"))
        template_set.bankingaccountref = "xx-xxxxxx-x"
        template_set.addresser = _("John Smit, Sample Company, 8976 Smallville")
        template_set.headerTextsalesorders = _(
            "According to your wishes the contract consists of the following positions:")
        template_set.footerTextsalesorders = _("Thank you for your interest in our company \n Best regards")
        template_set.headerTextpurchaseorders = _("We would like to order the following positions:")
        template_set.footerTextpurchaseorders = _("Best regards")
        template_set.pagefooterleft = _("Sample Company")
        template_set.pagefootermiddle = _("Sample Address")
        template_set.save()
        currency = crm.models.Currency()
        currency.description = "US Dollar"
        currency.shortName = "USD"
        currency.rounding = "0.10"
        currency.save()
        user_extension = djangoUserExtension.models.UserExtension()
        user_extension.defaultTemplateSet = template_set
        user_extension.defaultCurrency = currency
        user_extension.user = User.objects.all()[0]
        user_extension.save()
        postaladdress = djangoUserExtension.models.UserExtensionPostalAddress()
        postaladdress.purpose = 'H'
        postaladdress.name = "John"
        postaladdress.prename = "Smith"
        postaladdress.addressline1 = "Ave 1"
        postaladdress.zipcode = 899887
        postaladdress.town = "Smallville"
        postaladdress.userExtension = user_extension
        postaladdress.save()
        phoneaddress = djangoUserExtension.models.UserExtensionPhoneAddress()
        phoneaddress.phone = "1293847"
        phoneaddress.purpose = 'H'
        phoneaddress.userExtension = user_extension
        phoneaddress.save()
        emailaddress = djangoUserExtension.models.UserExtensionEmailAddress()
        emailaddress.email = "john.smith@smallville.com"
        emailaddress.purpose = 'H'
        emailaddress.userExtension = user_extension
        emailaddress.save()
