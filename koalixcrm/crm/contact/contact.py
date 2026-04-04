# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from koalixcrm.crm.contact.phone_address import PhoneAddress
from koalixcrm.crm.contact.email_address import EmailAddress
from koalixcrm.crm.contact.postal_address import PostalAddress
from koalixcrm.crm.contact.call import Call
from koalixcrm.crm.contact.person import *
from koalixcrm.crm.const.purpose import *
from koalixcrm.global_support_functions import xstr


class Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300,
                            verbose_name=_("Name"))
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         blank=True,
                                         verbose_name=_("Last modified by"),
                                         editable=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact')

    def __str__(self):
        return self.name


class PhoneAddressForContact(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"),
                               max_length=1,
                               choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contact')
        verbose_name_plural = _('Phone Address For Contact')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContact(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"),
                               max_length=1,
                               choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contact')
        verbose_name_plural = _('Email Address For Contact')

    def __str__(self):
        return str(self.email)


class PostalAddressForContact(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"),
                               max_length=1,
                               choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contact')
        verbose_name_plural = _('Postal Address For Contact')

    def __str__(self):
        return xstr(self.pre_name) + ' ' + xstr(self.name) + ' ' + xstr(self.address_line_1)


class ContactPersonAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='person_association', blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contact_association', blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return ''


class CallForContact(Call):
    company = models.ForeignKey(Contact, on_delete=models.CASCADE)
    cperson = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_("Person"),
                                blank=True,
                                null=True)
    purpose = models.CharField(verbose_name=_("Purpose"),
                               max_length=1,
                               choices=PURPOSECALLINCUSTOMER)

    class Meta:
        app_label = "crm"
        verbose_name = _('Call')
        verbose_name_plural = _('Calls')

    def __str__(self):
        return xstr(self.description) + ' ' + xstr(self.date_due)


class VisitForContact(Call):
    company = models.ForeignKey(Contact, on_delete=models.CASCADE)
    cperson = models.ForeignKey(Person,
                                on_delete=models.CASCADE,
                                verbose_name=_("Person"),
                                blank=True,
                                null=True)
    purpose = models.CharField(verbose_name=_("Purpose"),
                               max_length=1,
                               choices=PURPOSEVISITINCUSTOMER)
    ref_call = models.ForeignKey(CallForContact,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Reference Call"),
                                 blank=True,
                                 null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')

    def __str__(self):
        return xstr(self.description) + ' ' + xstr(self.date_due)



