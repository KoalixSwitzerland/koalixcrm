# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import QuerySet
from django.db.models.fields.files import FieldFile
from django.http import HttpRequest
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.djangoUserExtension.models.document_template import DocumentTemplate

from koalixcrm.contacts.models.address import Address
from koalixcrm.contacts.models.party_email import PartyEmail
from koalixcrm.contacts.models.phone_number import PhoneNumber
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.djangoUserExtension.exceptions import *
from koalixcrm.global_support_functions import xstr


class UserExtension(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=False, null=False)
    default_template_set = models.ForeignKey("TemplateSet", on_delete=models.CASCADE)
    default_currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE)

    @staticmethod
    def objects_to_serialize(object_to_create_pdf: Any, reference_user: AbstractBaseUser) -> list[Any]:
        from django.contrib import auth

        objects = list(auth.models.User.objects.filter(id=reference_user.id))
        user_extension = UserExtension.objects.filter(user=reference_user.id)
        if len(user_extension) == 0:
            raise UserExtensionMissing(_("During " + str(object_to_create_pdf) + " PDF Export"))
        phone_assignments = UserPhoneAssignment.objects.filter(user=reference_user.id)
        if len(phone_assignments) == 0:
            raise UserExtensionPhoneAddressMissing(_("During " + str(object_to_create_pdf) + " PDF Export"))
        email_assignments = UserEmailAssignment.objects.filter(user=reference_user.id)
        if len(email_assignments) == 0:
            raise UserExtensionEmailAddressMissing(_("During " + str(object_to_create_pdf) + " PDF Export"))
        objects += list(user_extension)
        objects += list(PhoneNumber.objects.filter(id=phone_assignments[0].phone_number_id))
        objects += list(PartyEmail.objects.filter(id=email_assignments[0].email_id))
        return objects

    @staticmethod
    def get_user_extension(django_user: AbstractBaseUser) -> "UserExtension":
        user_extensions = UserExtension.objects.filter(user=django_user)
        if len(user_extensions) > 1:
            raise TooManyUserExtensionsAvailable(
                _("More than one User Extension define for user ") + django_user.__str__()
            )
        elif len(user_extensions) == 0:
            raise UserExtensionMissing(_("No User Extension define for user ") + django_user.__str__())
        return user_extensions[0]

    def get_template_set(self, template_set: "DocumentTemplate") -> "DocumentTemplate":
        if template_set == self.default_template_set.work_report_template:
            if self.default_template_set.work_report_template:
                return self.default_template_set.work_report_template
            else:
                raise TemplateSetMissingForUserExtension(
                    (_("Template Set for work report " + "is missing for User Extension" + str(self)))
                )

    def get_fop_config_file(self, template_set: "DocumentTemplate") -> FieldFile:
        template_set = self.get_template_set(template_set)
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set: "DocumentTemplate") -> FieldFile:
        template_set = self.get_template_set(template_set)
        return template_set.get_xsl_file()

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _("User Extension")
        verbose_name_plural = _("User Extension")

    def __str__(self) -> str:
        return xstr(self.id) + " " + xstr(self.user.__str__())


class UserAddressAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="address_assignments",
        verbose_name=_("User"),
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="user_assignments",
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
        app_label = "djangoUserExtension"
        verbose_name = _("Address assignment for User")
        verbose_name_plural = _("Address assignments for User")

    def __str__(self) -> str:
        return f"{self.user_id}-{self.purpose}-{self.address_id}"


class UserPhoneAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="phone_assignments",
        verbose_name=_("User"),
    )
    phone_number = models.ForeignKey(
        PhoneNumber,
        on_delete=models.CASCADE,
        related_name="user_assignments",
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
        app_label = "djangoUserExtension"
        verbose_name = _("Phone assignment for User")
        verbose_name_plural = _("Phone assignments for User")

    def __str__(self) -> str:
        return f"{self.user_id}-{self.purpose}-{self.phone_number_id}"


class UserEmailAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_assignments",
        verbose_name=_("User"),
    )
    email = models.ForeignKey(
        PartyEmail,
        on_delete=models.CASCADE,
        related_name="user_assignments",
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
        app_label = "djangoUserExtension"
        verbose_name = _("Email assignment for User")
        verbose_name_plural = _("Email assignments for User")

    def __str__(self) -> str:
        return f"{self.user_id}-{self.purpose}-{self.email_id}"


class OptionUserExtension(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ("id", "user", "default_template_set", "default_currency")
    list_display_links = ("id", "user")
    list_filter = (
        "workspace",
        "user",
        "default_template_set",
    )
    ordering = ("id",)
    search_fields = ("id", "user")
    fieldsets = ((_("Basics"), {"fields": ("user", "default_template_set", "default_currency")}),)

    def create_work_report_pdf(self, request: HttpRequest, queryset: QuerySet[UserExtension]) -> None:
        """Enqueue async work-report PDFs for the HumanResource attached to
        each selected UserExtension. Mirrors HumanResourceAdminView's
        action; defaults to the trailing 60-day range until #404 lands
        the params field for date-range support.
        """
        from django.contrib import messages

        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from koalixcrm.reporting.models.human_resource import HumanResource

        # No `or Workspace.objects.first()` fallback: attributing an export to
        # whichever tenant happens to sort first is a wrong answer, not a
        # lenient one (REQ-0028 AC-10).
        workspace = getattr(request, "active_workspace", None)
        if workspace is None:
            self.message_user(
                request,
                _("No active workspace \u2014 switch to a workspace before exporting."),
                level=messages.ERROR,
            )
            return
        queued = 0
        for ue in queryset:
            template_set = getattr(ue.default_template_set, "work_report_template", None)
            if not template_set:
                self.message_user(
                    request,
                    _("Work report template missing for %(ue)s") % {"ue": ue},
                    level=messages.ERROR,
                )
                continue
            hr = HumanResource.objects.filter(user=ue).first()
            if hr is None:
                self.message_user(
                    request,
                    _("No HumanResource attached to %(ue)s") % {"ue": ue},
                    level=messages.ERROR,
                )
                continue
            PDFExportProcess.objects.create(
                workspace=workspace,
                source_model="HumanResource",
                source_id=hr.id,
                template_set=template_set,
                triggered_by=request.user,
            )
            queued += 1
        if queued:
            self.message_user(
                request,
                _("%(count)d work report job(s) queued.") % {"count": queued},
                level=messages.SUCCESS,
            )

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf] if apps.is_installed("koalixcrm.reporting") else []
