# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _
from koalixcrm.crm.contact.contact import Contact


class Customer(Contact):
    default_customer_billing_cycle = models.ForeignKey('CustomerBillingCycle',
                                                       on_delete=models.CASCADE,
                                                       verbose_name=_('Default Billing Cycle'))
    is_member_of = models.ManyToManyField("CustomerGroup",
                                          verbose_name=_('Is member of'),
                                          blank=True)
    is_lead = models.BooleanField(default=True)

    def create_contract(self, request):
        from koalixcrm.contracts.models.contract import Contract
        contract = Contract()
        contract.create_from_reference(self, request.user)
        return contract

    def create_invoice(self, request):
        contract = self.create_contract(request)
        invoice = contract.create_invoice()
        return invoice

    def create_quote(self, request):
        contract = self.create_contract(request)
        quote = contract.create_quote()
        return quote

    def is_in_group(self, customer_group):
        for customer_group_membership in self.is_member_of.all():
            if customer_group_membership.id == customer_group.id:
                return 1
        return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return str(self.id) + ' ' + self.name
