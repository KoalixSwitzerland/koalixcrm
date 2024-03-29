# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.crm.contact.postal_address import PostalAddress
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.djangoUserExtension.const.purpose import *
from koalixcrm.djangoUserExtension.exceptions import *
from koalixcrm.global_support_functions import xstr


class UserExtension(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("auth.User",
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False)
    default_template_set = models.ForeignKey("TemplateSet", on_delete=models.CASCADE)
    default_currency = models.ForeignKey("crm.Currency", on_delete=models.CASCADE)

    @staticmethod
    def objects_to_serialize(object_to_create_pdf, reference_user):
        from koalixcrm.crm.contact.phone_address import PhoneAddress
        from koalixcrm.crm.contact.email_address import EmailAddress
        from django.contrib import auth
        objects = list(auth.models.User.objects.filter(id=reference_user.id))
        user_extension = UserExtension.objects.filter(user=reference_user.id)
        if len(user_extension) == 0:
            raise UserExtensionMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        phone_address = UserExtensionPhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        if len(phone_address) == 0:
            raise UserExtensionPhoneAddressMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        email_address = UserExtensionEmailAddress.objects.filter(
            userExtension=user_extension[0].id)
        if len(email_address) == 0:
            raise UserExtensionEmailAddressMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        objects += list(user_extension)
        objects += list(EmailAddress.objects.filter(id=email_address[0].id))
        objects += list(PhoneAddress.objects.filter(id=phone_address[0].id))
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


class UserExtensionPostalAddress(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension, on_delete=models.CASCADE)

    def __str__(self):
        return xstr(self.name) + ' ' + xstr(self.pre_name)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Postal Address for User Extension')
        verbose_name_plural = _('Postal Address for User Extension')


class UserExtensionPhoneAddress(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension, on_delete=models.CASCADE)

    def __str__(self):
        return xstr(self.phone)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Phone number for User Extension')
        verbose_name_plural = _('Phone number for User Extension')


class UserExtensionEmailAddress(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension, on_delete=models.CASCADE)

    def __str__(self):
        return xstr(self.email)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Email Address for User Extension')
        verbose_name_plural = _('Email Address for User Extension')


class InlineUserExtensionPostalAddress(admin.StackedInline):
    model = UserExtensionPostalAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
                'prefix',
                'pre_name',
                'name',
                'address_line_1',
                'address_line_2',
                'address_line_3',
                'address_line_4',
                'zip_code',
                'town',
                'state',
                'country',
                'purpose')
        }),
    )
    allow_add = True


class InlineUserExtensionPhoneAddress(admin.StackedInline):
    model = UserExtensionPhoneAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('phone',
                       'purpose',)
        }),
    )
    allow_add = True


class InlineUserExtensionEmailAddress(admin.StackedInline):
    model = UserExtensionEmailAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('email',
                       'purpose',)
        }),
    )
    allow_add = True


class OptionUserExtension(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'default_template_set',
                    'default_currency')
    list_display_links = ('id',
                          'user')
    list_filter = ('user',
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
        from koalixcrm.crm.views.create_work_report import create_work_report

        return create_work_report(self, request, queryset)

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf]
    inlines = [InlineUserExtensionPostalAddress,
               InlineUserExtensionPhoneAddress,
               InlineUserExtensionEmailAddress]
