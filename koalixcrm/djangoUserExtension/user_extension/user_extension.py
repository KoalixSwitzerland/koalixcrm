# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _

from koalixcrm.crm.exceptions import *
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.documents.pdfexport import PDFExport
from koalixcrm.djangoUserExtension.const.purpose import *
from koalixcrm.djangoUserExtension.exceptions import TemplateSetMissingForUserExtension
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.reporting.work import Work


class UserExtension(models.Model):
    user = models.ForeignKey("auth.User", blank=False, null=False)
    default_template_set = models.ForeignKey("TemplateSet")
    default_currency = models.ForeignKey("crm.Currency")

    @staticmethod
    def objects_to_serialize(object_to_create_pdf, reference_user):
        from koalixcrm.crm.contact.phoneaddress import PhoneAddress
        from koalixcrm.crm.contact.emailaddress import EmailAddress
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

    def create_pdf(self, template_set, printed_by):
        return PDFExport.create_pdf(self, template_set, printed_by)

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

    def serialize_to_xml(self, **kwargs):
        date_from = kwargs.get('date_from', datetime.date.today()-datetime.timedelta(days=60))
        date_to = kwargs.get('date_to', datetime.date.today())
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        date = date_from
        days = dict()
        weeks = dict()
        months = dict()
        while date < date_to:
            days[date] = 0
            month_key = str(date.month)+"/"+str(date.year)
            week_key = str(date.isocalendar()[1])+"/"+str(date.year)
            if not (week_key in weeks):
                weeks[week_key] = 0
            if not (month_key in months):
                months[month_key] = 0
            date += datetime.timedelta(days=1)
        works = Work.objects.filter(employee=self, date__range=(date_from, date_to))
        for work in works:
            days[work.date] += work.effort_hours()
            month_key = str(work.date.month)+"/"+str(work.date.year)
            week_key = str(work.date.isocalendar()[1])+"/"+str(work.date.year)
            weeks[week_key] += work.effort_hours()
            months[month_key] += work.effort_hours()
        for day_key in days.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Day_Work_Hours",
                                                           str(days[day_key]),
                                                           attributes={"day": str(day_key.day),
                                                                       "week": str(day_key.isocalendar()[1]),
                                                                       "week_day": str(day_key.isoweekday()),
                                                                       "month": str(day_key.month),
                                                                       "year": str(day_key.year)})
        for week_key in weeks.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Week_Work_Hours",
                                                           str(weeks[week_key]),
                                                           attributes={"week": str(week_key)})
        for month_key in months.keys():
            main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                           "object/[@model='djangoUserExtension.userextension']",
                                                           "Month_Work_Hours",
                                                           str(months[month_key]),
                                                           attributes={"week": str(month_key)})
        return main_xml

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extension')

    def __str__(self):
        return xstr(self.id) + ' ' + xstr(self.user.__str__())


class UserExtensionPostalAddress(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return xstr(self.name) + ' ' + xstr(self.pre_name)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Postal Address for User Extension')
        verbose_name_plural = _('Postal Address for User Extension')


class UserExtensionPhoneAddress(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

    def __str__(self):
        return xstr(self.phone)

    class Meta:
        app_label = "djangoUserExtension"
        verbose_name = _('Phone number for User Extension')
        verbose_name_plural = _('Phone number for User Extension')


class UserExtensionEmailAddress(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
    userExtension = models.ForeignKey(UserExtension)

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
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/djangoUserExtension/"+obj.__class__.__name__.lower()+"/"),
                                                obj.default_template_set.work_report_template)
        return response

    create_work_report_pdf.short_description = _("Work Report PDF")

    save_as = True
    actions = [create_work_report_pdf]
    inlines = [InlineUserExtensionPostalAddress,
               InlineUserExtensionPhoneAddress,
               InlineUserExtensionEmailAddress]