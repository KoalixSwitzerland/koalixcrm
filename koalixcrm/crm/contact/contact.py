# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.country import *
from koalixcrm.crm.const.postaladdressprefix import *
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.documents.activity import Call, CallOverdueFilter
from koalixcrm.crm.contact.person import *
from koalixcrm.crm.const.purpose import *
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm.crm.inlinemixin import LimitedAdminInlineMixin
#from koalixcrm.crm.forms import ImportDataContactForm

from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), editable=True)
    vatnumber = models.CharField(max_length=20, verbose_name=_("Vat Number"), blank=True) 
    
    people = models.ManyToManyField("Person", through='ContactPersonAssociation', verbose_name=_('Has contact'), blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact')


class PhoneAddressForContact(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    company = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contact')
        verbose_name_plural = _('Phone Address For Contact')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContact(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    company = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contact')
        verbose_name_plural = _('Email Address For Contact')

    def __str__(self):
        return str(self.email)


class PostalAddressForContact(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    company = models.ForeignKey(Contact)

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

class CallForContact(Call):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSECALLINCUSTOMER)
    company = models.ForeignKey(Contact)
    cperson = models.ForeignKey(Person, verbose_name=_("Person"), blank=True, null=True)
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Call')
        verbose_name_plural = _('Calls')

    def __str__(self):
        return xstr(self.description) + ' ' + xstr(self.date_due)

class VisitForContact(Call):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSECALLINCUSTOMER)
    company = models.ForeignKey(Contact)
    cperson = models.ForeignKey(Person, verbose_name=_("Person"), blank=True, null=True)
    ref_call = models.ForeignKey(CallForContact, verbose_name=_("Reference Call"), blank=True, null=True)
    
    class Meta:
        app_label = "crm"
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')

    def __str__(self):
        return xstr(self.description) + ' ' + xstr(self.date_due)

class ContactCall(LimitedAdminInlineMixin, admin.StackedInline):
    model = CallForContact
    extra = 0
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'description', 'date_due', 'purpose', 'status', 'cperson',)
        }),
    )
    allow_add = True

    def get_filters(self, request, obj):
        return getattr(self, 'filters', ()) if obj is None else (('cperson', dict(companies=obj.id)),)

class ContactVisit(LimitedAdminInlineMixin, admin.StackedInline):
    model = VisitForContact
    extra = 0
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': (
            'description', 'date_due', 'purpose', 'status', 'cperson', 'ref_call',)
        }),
    )
    allow_add = True
    
    def get_filters(self, request, obj):
        return getattr(self, 'filters', ()) if obj is None else (('cperson', dict(companies=obj.id)),('ref_call', dict(company=obj.id, status='S')))

class OptionCall(admin.ModelAdmin):
    list_display = ('id','description','date_due','purpose','get_contactname', 'status', 'is_call_overdue',)
    list_filter = [CallOverdueFilter]

    def get_contactname(self, obj):
        return obj.company.name

    get_contactname.short_description = _("Company")

    def is_call_overdue(self, obj):
        return (obj.date_due < timezone.now() and obj.status not in ['F', 'S'])

    is_call_overdue.short_description = _("Is call overdue")

class ContactPersonAssociation(models.Model):
    contact = models.ForeignKey(Contact, related_name='person_association', blank=True, null=True)
    person = models.ForeignKey(Person, related_name='contact_association', blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return ''

class PeopleInlineAdmin(admin.TabularInline):
    model = ContactPersonAssociation
    extra = 0
    show_change_link = True

class CompaniesInlineAdmin(admin.TabularInline):
    model = ContactPersonAssociation
    extra = 0
    show_change_link = True

class OptionPerson(admin.ModelAdmin):
    list_display = ('id', 'name', 'prename', 'email', 'role', 'get_companies',)
    #filter_horizontal = ('companies',)
    fieldsets = (('', {'fields': ('prefix','name','prename','role','email','phone',)}),)
    allow_add = True
    inlines = [CompaniesInlineAdmin]
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("personInline"))

    actions = []
    pluginProcessor = PluginProcessor()
    inlines.extend(pluginProcessor.getPluginAdditions("personActions"))

    def get_companies(self, obj):
        items = []
        for c in obj.companies.all():
            items.append(c.name)
        return ','.join(items)
    
    get_companies.short_description = _("Works at")

class StateFilter(admin.SimpleListFilter):
    title = _('State')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        items = []
        for a in PostalAddressForContact.objects.values('state').distinct():
            items.append((a['state'], _(a['state'])))
        return (
            items
        )

    def queryset(self, request, queryset):
        for p in PostalAddressForContact.objects.all(): 
            if self.value() == str(p.state):
                address_per_company = PostalAddressForContact.objects.filter(state=p.state)
                ids = [(a.company.id) for a in address_per_company]
                return queryset.filter(pk__in=ids)
        return queryset

class CityFilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        items = []
        state = request.GET.get('state', None)
        unique_list = PostalAddressForContact.objects.all().order_by('town')
        adjusted_queryset = unique_list if state is None else unique_list.filter(state=state)
        for a in adjusted_queryset.values('town').distinct():
            items.append((a['town'], _(a['town'])))
        return (
            items
        )

    def queryset(self, request, queryset):
        for p in PostalAddressForContact.objects.all(): 
            if self.value() == str(p.town):
                address_per_company = PostalAddressForContact.objects.filter(town=p.town)
                ids = [(c.company.id) for c in address_per_company]
                return queryset.filter(pk__in=ids)
        return queryset


#DATA IMPORT
class ContactImportData(models.Model):
    data_file = models.FileField(upload_to='data_files', max_length=255)

    contact_type = models.CharField(verbose_name=_("Contact Type"), max_length=1, choices=CONTACTTYPE)

    def file_link(self):
        if self.data_file:
            return "<a href='%s'>download</a>" % (self.data_file.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True

    def __str__(self):
        return '{}'.format(self.data_file.name)

    class Meta:
        """
        """
        verbose_name = 'Contact: Import Data from XLSX file'
        verbose_name_plural = 'Contacts: Import Data from XLSX file'
