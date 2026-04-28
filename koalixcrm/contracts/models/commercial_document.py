# -*- coding: utf-8 -*-
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

import koalixcrm.contracts.models.calculations
from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES
from koalixcrm.core.const.purpose import *
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.djangoUserExtension.models import (
    TextParagraphInDocumentTemplate,
)


class TextParagraphInCommercialDocument(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    def create_paragraph(
        self,
        default_paragraph: TextParagraphInDocumentTemplate,
        commercial_document: CommercialDocument,
    ) -> None:
        self.commercial_document = commercial_document
        self.purpose = default_paragraph.purpose
        self.text_paragraph = default_paragraph.text_paragraph
        self.save()
        return

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_textparagraphincommercialdocument"
        verbose_name = _("Text Paragraph In Commercial Document")
        verbose_name_plural = _("Text Paragraphs In Commercial Documents")

    def __str__(self) -> str:
        return str(self.id)


class CommercialDocument(WorkspaceScopedModel):
    contract = models.ForeignKey("Contract", on_delete=models.CASCADE, verbose_name=_("Contract"))
    party_reference = models.CharField(verbose_name=_("Party Reference"), max_length=100, blank=True)
    ext_business_appl_references = models.JSONField(
        verbose_name=_("External Business Application References"),
        blank=True,
        default=dict,
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(
        max_digits=17, decimal_places=2, verbose_name=_("Price without Tax "), blank=True, null=True
    )
    last_calculated_tax = models.DecimalField(
        max_digits=17, decimal_places=2, verbose_name=_("Tax"), blank=True, null=True
    )
    party = models.ForeignKey(
        "contacts.Party", on_delete=models.PROTECT, related_name="commercial_documents", verbose_name=_("Party")
    )
    staff = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        blank=True,
        verbose_name=_("Staff"),
        related_name="db_relscstaff",
        null=True,
    )
    currency = models.ForeignKey(
        "core.Currency", on_delete=models.CASCADE, verbose_name=_("Currency"), blank=False, null=False
    )
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    custom_date_field = models.DateField(verbose_name=_("Custom Date"), blank=True, null=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        verbose_name=_("Last modified by"),
        related_name="db_lstscmodified",
        null=True,
        blank="True",
    )
    template_set = models.ForeignKey(
        "djangoUserExtension.DocumentTemplate",
        on_delete=models.CASCADE,
        verbose_name=_("Referred Template"),
        null=True,
        blank=True,
    )
    derived_from_commercial_document = models.ForeignKey(
        "CommercialDocument", on_delete=models.CASCADE, blank=True, null=True
    )
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"), blank=True, null=True)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocument"
        verbose_name = _("Commercial Document")
        verbose_name_plural = _("Commercial Documents")

    def is_complete_with_price(self) -> bool:
        """Checks whether the CommercialDocument is completed with a price, in case the
        CommercialDocument was not completed or the price calculation was not performed,
        the method returns false"""

        if self.last_pricing_date and self.last_calculated_price:
            return True
        else:
            return False

    def create_commercial_document(self, calling_model: models.Model) -> None:
        self.staff = calling_model.staff
        if isinstance(calling_model, koalixcrm.contracts.models.contract.Contract):
            self.contract = calling_model
            self.party = calling_model.buyer_party
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.discount = 0
        elif isinstance(calling_model, CommercialDocument):
            self.derived_from_commercial_document = calling_model
            self.contract = calling_model.contract
            self.party = calling_model.party
            self.currency = calling_model.currency
            self.description = calling_model.description
            self.discount = calling_model.discount

    def attach_text_paragraphs(self) -> None:
        default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=self.template_set)
        for default_paragraph in list(default_paragraphs):
            paragraph = TextParagraphInCommercialDocument()
            paragraph.create_paragraph(default_paragraph, self)

    def attach_commercial_document_positions(self, calling_model: models.Model) -> None:
        if isinstance(calling_model, CommercialDocument):
            commercial_document_positions = CommercialDocumentPosition.objects.filter(
                commercial_document=calling_model.id
            )
            for commercial_document_position in list(commercial_document_positions):
                new_position = CommercialDocumentPosition()
                new_position.create_position(commercial_document_position, self)

    def __str__(self) -> str:
        return _("Commercial Document") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class CommercialDocumentAddressAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        "CommercialDocument",
        on_delete=models.CASCADE,
        related_name="address_assignments",
        verbose_name=_("Commercial Document"),
    )
    address = models.ForeignKey(
        "contacts.Address",
        on_delete=models.CASCADE,
        related_name="commercial_document_assignments",
        verbose_name=_("Address"),
    )
    purpose = models.CharField(
        max_length=16,
        choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocumentaddressassignment"
        verbose_name = _("Commercial Document Address Assignment")
        verbose_name_plural = _("Commercial Document Address Assignments")

    def __str__(self) -> str:
        return f"{self.document_id}-{self.purpose}-{self.address_id}"


class CommercialDocumentPhoneAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        "CommercialDocument",
        on_delete=models.CASCADE,
        related_name="phone_assignments",
        verbose_name=_("Commercial Document"),
    )
    phone_number = models.ForeignKey(
        "contacts.PhoneNumber",
        on_delete=models.CASCADE,
        related_name="commercial_document_assignments",
        verbose_name=_("Phone number"),
    )
    purpose = models.CharField(
        max_length=16,
        choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocumentphoneassignment"
        verbose_name = _("Commercial Document Phone Assignment")
        verbose_name_plural = _("Commercial Document Phone Assignments")

    def __str__(self) -> str:
        return f"{self.document_id}-{self.purpose}-{self.phone_number_id}"


class CommercialDocumentEmailAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        "CommercialDocument",
        on_delete=models.CASCADE,
        related_name="email_assignments",
        verbose_name=_("Commercial Document"),
    )
    email = models.ForeignKey(
        "contacts.PartyEmail",
        on_delete=models.CASCADE,
        related_name="commercial_document_assignments",
        verbose_name=_("Email"),
    )
    purpose = models.CharField(
        max_length=16,
        choices=ASSIGNMENT_PURPOSE_CHOICES,
        verbose_name=_("Purpose"),
    )
    is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
    valid_from = models.DateField(blank=True, null=True, verbose_name=_("Valid from"))
    valid_to = models.DateField(blank=True, null=True, verbose_name=_("Valid to"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocumentemailassignment"
        verbose_name = _("Commercial Document Email Assignment")
        verbose_name_plural = _("Commercial Document Email Assignments")

    def __str__(self) -> str:
        return f"{self.document_id}-{self.purpose}-{self.email_id}"
