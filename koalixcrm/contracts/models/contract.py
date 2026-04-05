# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.plugin import *
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.postal_address import PostalAddress
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.quote import Quote
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.global_support_functions import xstr
from koalixcrm.crm.const.purpose import *
from koalixcrm.crm.exceptions import *
from koalixcrm.djangoUserExtension.models import UserExtension
import koalixcrm.contracts.models.calculations
import koalixcrm.crm.documents.pdf_export

class PostalAddressForContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_postaladdressforcontract"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PhoneAddressForContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_phoneaddressforcontract"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey('Contract', on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_emailaddressforcontract"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


class Contract(models.Model):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              verbose_name=_("Staff"),
                              related_name="db_relcontractstaff",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name=_("Description"))
    default_customer = models.ForeignKey("crm.Customer",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Customer"),
                                         null=True,
                                         blank=True)
    default_supplier = models.ForeignKey("crm.Supplier",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Supplier"),
                                         null=True,
                                         blank=True)
    default_currency = models.ForeignKey("products.Currency",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Default Currency"),
                                         blank=False,
                                         null=False)
    default_template_set = models.ForeignKey("djangoUserExtension.TemplateSet",
                                             on_delete=models.CASCADE,
                                             verbose_name=_("Default Template Set"),
                                             null=True,
                                             blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_contractlstmodified")

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_contract"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def get_template_set(self, calling_model):
        if self.default_template_set:
            required_template_set = str(type(calling_model).__name__)
            return self.default_template_set.get_template_set(required_template_set)
        else:
            raise TemplateSetMissingInContract("The Contract has no Default Template Set selected")

    def create_from_reference(self, calling_model, staff):
        staff_user_extension = UserExtension.get_user_extension(staff.id)
        self.default_customer = calling_model
        self.default_currency = staff_user_extension.defaultCurrency
        self.default_template_set = staff_user_extension.defaultTemplateSet
        self.last_modified_by = staff
        self.staff = staff
        self.save()
        return self

    def create_invoice(self):
        invoice = Invoice()
        invoice.create_from_reference(self)
        return invoice

    def create_quote(self):
        quote = Quote()
        quote.create_from_reference(self)
        return quote

    def create_purchase_order(self):
        purchase_order = PurchaseOrder()
        purchase_order.create_from_reference(self)
        return purchase_order

    def __str__(self):
        return _("Contract") + " " + str(self.id)


