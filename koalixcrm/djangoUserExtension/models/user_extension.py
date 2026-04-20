# -*- coding: utf-8 -*-

from django.apps import apps
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.address import Address
from koalixcrm.contacts.models.phone_number import PhoneNumber
from koalixcrm.contacts.models.party_email import PartyEmail
from koalixcrm.core.const.party import ASSIGNMENT_PURPOSE_CHOICES
from koalixcrm.djangoUserExtension.exceptions import *
from koalixcrm.global_support_functions import xstr
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin


class UserExtension(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("auth.User",
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False)
    default_template_set = models.ForeignKey("TemplateSet", on_delete=models.CASCADE)
    default_currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE)

    @staticmethod
    def objects_to_serialize(object_to_create_pdf, reference_user):
        from django.contrib import auth
        objects = list(auth.models.User.objects.filter(id=reference_user.id))
        user_extension = UserExtension.objects.filter(user=reference_user.id)
        if len(user_extension) == 0:
            raise UserExtensionMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        phone_assignments = UserPhoneAssignment.objects.filter(
            user=reference_user.id)
        if len(phone_assignments) == 0:
            raise UserExtensionPhoneAddressMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        email_assignments = UserEmailAssignment.objects.filter(
            user=reference_user.id)
        if len(email_assignments) == 0:
            raise UserExtensionEmailAddressMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        objects += list(user_extension)
        objects += list(PhoneNumber.objects.filter(id=phone_assignments[0].phone_number_id))
        objects += list(PartyEmail.objects.filter(id=email_assignments[0].email_id))
        return objects

    @staticmethod
    def get_user_extension(django_user):
        user_extensions = UserExtension.objects.filter(user=django_user)
        if len(user_extensions) > 1:
            raise TooManyUserExtensionsAvailable(_("More than one User Extension define for user ") + django_user.__str__())
        elif len(user_extensions) == 0:
            raise UserExtensionMissing(_("No User Extension define for user ") + django_user.__str__())
        return user_extensions[0]

    def get_template_set(self, template_set):
        if template_set == self.default_template_set.work_report_template:
            if self.default_template_set.work_report_template:
                return self.default_template_set.work_report_template
            else:
                raise TemplateSetMissingForUserExtension((_("Template Set for work report " +
                                                            "is missing for User Extension" + str(self))))

    def get_fop_config_file(self, template_set):
        template_set = self.get_template_set(template_set)
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set):
        template_set = self.get_template_set(template_set)
        return template_set.get_xsl_file()

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extension')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.user.__str__())


class UserAddressAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='address_assignments',
        verbose_name=_("User"),
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='user_assignments',
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
        app_label = "djangoUserExtension"
        verbose_name = _('Address assignment for User')
        verbose_name_plural = _('Address assignments for User')

    def __str__(self):
        return f"{self.user_id}-{self.purpose}-{self.address_id}"


class UserPhoneAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='phone_assignments',
        verbose_name=_("User"),
    )
    phone_number = models.ForeignKey(
        PhoneNumber,
        on_delete=models.CASCADE,
        related_name='user_assignments',
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
        app_label = "djangoUserExtension"
        verbose_name = _('Phone assignment for User')
        verbose_name_plural = _('Phone assignments for User')

    def __str__(self):
        return f"{self.user_id}-{self.purpose}-{self.phone_number_id}"


class UserEmailAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_assignments',
        verbose_name=_("User"),
    )
    email = models.ForeignKey(
        PartyEmail,
        on_delete=models.CASCADE,
        related_name='user_assignments',
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
        app_label = "djangoUserExtension"
        verbose_name = _('Email assignment for User')
        verbose_name_plural = _('Email assignments for User')

    def __str__(self):
        return f"{self.user_id}-{self.purpose}-{self.email_id}"


class OptionUserExtension(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'default_template_set',
                    'default_currency')
    list_display_links = ('id',
                          'user')
    list_filter = ('workspace',
                   'user',
                   'default_template_set',)
    ordering = ('id',)
    search_fields = ('id',
                     'user')
    fieldsets = (
        (_('Basics'), {
            'fields': ('user',
                       'default_template_set',
                       'default_currency')
        }),
    )

    def create_work_report_pdf(self, request, queryset):
        from koalixcrm.reporting.views.create_work_report import create_work_report

        return create_work_report(self, request, queryset)

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf] if apps.is_installed('koalixcrm.reporting') else []
