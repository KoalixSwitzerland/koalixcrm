"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'koalixcrm.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.Group(
            _('CRMLite (based on koalixcrm V1.12dev2)'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Projects'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.documents.contract.Contract',
                            'koalixcrm.crm.documents.purchaseorder.PurchaseOrder',),
                ),
                modules.ModelList(
                    _('Sales Documents'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.documents.quote.Quote',
                            'koalixcrm.crm.documents.purchaseconfirmation.PurchaseConfirmation',
                            'koalixcrm.crm.documents.deliverynote.DeliveryNote',
                            'koalixcrm.crm.documents.invoice.Invoice',
                            'koalixcrm.crm.documents.paymentreminder.PaymentReminder',),
                ),
                modules.ModelList(
                    _('Scheduler'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.contact.contact.CallForContact',
                            'koalixcrm.crm.documents.visit.Visit',
                            'koalixcrm.crm.contact.data_import.ContactImportData'),
                ),
                modules.ModelList(
                    _('Data Import'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.contact.contact.ContactImportData'),
                ),
                modules.ModelList(
                    _('Products'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.product.product.Product',
                            'koalixcrm.crm.product.attribute.AttributeSet',
                            'koalixcrm.crm.product.attribute.Attribute'),
                ),
                modules.ModelList(
                    _('Contacts'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.contact.customer.Customer',
                            'koalixcrm.crm.contact.supplier.Supplier',
                            'koalixcrm.crm.contact.person.Person'),
                ),
                modules.ModelList(
                    _('Accounting'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.accounting.*',),
                ),
            ]
        ))

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Group: Administration & Applications'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    _('Administration'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
                modules.ModelList(
                    _('Settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.contact.customerbillingcycle.CustomerBillingCycle',
                            'koalixcrm.crm.contact.customergroup.CustomerGroup',
                            'koalixcrm.crm.product.tax.Tax',
                            'koalixcrm.crm.product.unit.Unit',
                            'koalixcrm.crm.product.currency.Currency',
                            'koalixcrm.djangoUserExtension.*'),
                ),
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('koalixcrm on github'),
                    'url': 'https://github.com/scaphilo/koalixcrm/',
                    'external': True,
                },
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


