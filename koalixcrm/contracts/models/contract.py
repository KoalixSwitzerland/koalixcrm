# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES
from koalixcrm.core.const.purpose import *
from koalixcrm.core.exceptions import *
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.djangoUserExtension.models import UserExtension
from koalixcrm.plugin import *


class ContractAddressAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey(
        'Contract', on_delete=models.CASCADE,
        related_name='address_assignments',
        verbose_name=_("Contract"),
    )
    address = models.ForeignKey(
        'contacts.Address', on_delete=models.CASCADE,
        related_name='contract_assignments',
        verbose_name=_("Address"),
    )
    purpose = models.CharField(
        max_length=16, choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_contractaddressassignment"
        verbose_name = _('Contract Address Assignment')
        verbose_name_plural = _('Contract Address Assignments')

    def __str__(self):
        return f"{self.contract_id}-{self.purpose}-{self.address_id}"


class ContractPhoneAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey(
        'Contract', on_delete=models.CASCADE,
        related_name='phone_assignments',
        verbose_name=_("Contract"),
    )
    phone_number = models.ForeignKey(
        'contacts.PhoneNumber', on_delete=models.CASCADE,
        related_name='contract_assignments',
        verbose_name=_("Phone number"),
    )
    purpose = models.CharField(
        max_length=16, choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_contractphoneassignment"
        verbose_name = _('Contract Phone Assignment')
        verbose_name_plural = _('Contract Phone Assignments')

    def __str__(self):
        return f"{self.contract_id}-{self.purpose}-{self.phone_number_id}"


class ContractEmailAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    contract = models.ForeignKey(
        'Contract', on_delete=models.CASCADE,
        related_name='email_assignments',
        verbose_name=_("Contract"),
    )
    email = models.ForeignKey(
        'contacts.PartyEmail', on_delete=models.CASCADE,
        related_name='contract_assignments',
        verbose_name=_("Email"),
    )
    purpose = models.CharField(
        max_length=16, choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_contractemailassignment"
        verbose_name = _('Contract Email Assignment')
        verbose_name_plural = _('Contract Email Assignments')

    def __str__(self):
        return f"{self.contract_id}-{self.purpose}-{self.email_id}"


class Contract(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              verbose_name=_("Staff"),
                              related_name="db_relcontractstaff",
                              blank=True,
                              null=True)
    description = models.TextField(verbose_name=_("Description"))
    buyer_party = models.ForeignKey("contacts.Party",
                                    on_delete=models.PROTECT,
                                    related_name="contracts_as_buyer",
                                    verbose_name=_("Buyer (Party)"),
                                    null=True,
                                    blank=True)
    supplier_party = models.ForeignKey("contacts.Party",
                                       on_delete=models.PROTECT,
                                       related_name="contracts_as_supplier",
                                       verbose_name=_("Supplier (Party)"),
                                       null=True,
                                       blank=True)
    default_currency = models.ForeignKey("core.Currency",
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

    def create_quotation(self):
        quotation = Quotation()
        quotation.create_from_reference(self)
        return quotation

    def create_purchase_order(self):
        purchase_order = PurchaseOrder()
        purchase_order.create_from_reference(self)
        return purchase_order

    def __str__(self):
        return _("Contract") + " " + str(self.id)


