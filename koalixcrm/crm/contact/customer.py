# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact

import koalixcrm.crm.documents.contract

class Customer(Contact):
    defaultCustomerBillingCycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField("CustomerGroup", verbose_name=_('Is member of'), blank=True)

    def createContract(self, request):
        contract = koalixcrm.crm.documents.contract.Contract()
        contract.defaultcustomer = self
        contract.defaultcurrency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.lastmodifiedby = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def createInvoice(self):
        contract = self.createContract()
        invoice = contract.createInvoice()
        return invoice

    def createQuote(self):
        contract = self.createContract()
        quote = contract.createQuote()
        return quote

    def isInGroup(self, customerGroup):
        for customerGroupMembership in self.ismemberof.all():
            if (customerGroupMembership.id == customerGroup.id):
                return 1
        return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return str(self.id) + ' ' + self.name