# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr


class Contact(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), editable=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact')


class PhoneAddressForContact(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contact')
        verbose_name_plural = _('Phone Address For Contact')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContact(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contact')
        verbose_name_plural = _('Email Address For Contact')

    def __str__(self):
        return str(self.email)


class PostalAddressForContact(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contact')
        verbose_name_plural = _('Postal Address For Contact')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)

class ContactPostalAddress(admin.StackedInline):
    model = PostalAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class ContactPhoneAddress(admin.TabularInline):
    model = PhoneAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class ContactEmailAddress(admin.TabularInline):
    model = EmailAddressForContact
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True
