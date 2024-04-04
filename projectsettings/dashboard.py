"""
This file was generated with the custom dashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'koalixcrm.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
from koalixcrm.version import KOALIXCRM_VERSION


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        self.children.append(modules.Group(
            _('koalixcrm Version' + KOALIXCRM_VERSION),
            column=1,
            collapsible=True,
            children=[
                   modules.ModelList(
                    _('Sales Documents and Contracts'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.documents.contract.Contract',
                            'koalixcrm.crm.documents.quote.Quote',
                            'koalixcrm.crm.documents.purchase_confirmation.PurchaseConfirmation',
                            'koalixcrm.crm.documents.delivery_note.DeliveryNote',
                            'koalixcrm.crm.documents.invoice.Invoice',
                            'koalixcrm.crm.documents.payment_reminder.PaymentReminder',),
                    ),
                    modules.ModelList(
                        _('Scheduler'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.crm.contact.contact.CallForContact',
                                'koalixcrm.crm.contact.contact.VisitForContact',),
                    ),
                    modules.ModelList(
                        _('Products'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.crm.product.product.Product',),
                    ),
                    modules.ModelList(
                        _('Contacts'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.crm.contact.customer.Customer',
                                'koalixcrm.crm.contact.supplier.Supplier',
                                'koalixcrm.crm.contact.person.Person',),
                    ),
                    modules.ModelList(
                        _('Accounting'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.accounting.*',),
                    ),
                    modules.ModelList(
                        _('Projects'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.crm.reporting.project.Project',
                                'koalixcrm.crm.reporting.reporting_period.ReportingPeriod',
                                'koalixcrm.crm.reporting.task.Task',
                                'koalixcrm.crm.reporting.agreement.Agreement',
                                'koalixcrm.crm.reporting.estimation.Estimation',
                                'koalixcrm.crm.reporting.human_resource.HumanResource',
                                'koalixcrm.crm.documents.purchase_order.PurchaseOrder',),
                    ),
                    modules.LinkList(
                        _('Report Work And Expenses'),
                        column=1,
                        children=[{'title': _('Time Tracking'),
                                   'url': '/koalixcrm/crm/reporting/time_tracking/',
                                   'external': False},
                                  {'title': _('Set Timezone'),
                                   'url': '/koalixcrm/crm/reporting/set_timezone/',
                                   'external': False}]
                    )

            ]
        ))

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Users, Access Rights and Application Settings'),
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    _('Administration'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
                modules.ModelList(
                    _('Contact settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.contact.customer_billing_cycle.CustomerBillingCycle',
                            'koalixcrm.crm.contact.customer_group.CustomerGroup',),
                ),
                modules.ModelList(
                    _('Product settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.product.tax.Tax',
                            'koalixcrm.crm.product.unit.Unit',
                            'koalixcrm.crm.product.currency.Currency'),
                ),
                modules.ModelList(
                    _('Reporting settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.crm.reporting.agreement_status.AgreementStatus',
                            'koalixcrm.crm.reporting.agreement_type.AgreementType',
                            'koalixcrm.crm.reporting.estimation_status.EstimationStatus',
                            'koalixcrm.crm.reporting.generic_project_link.GenericProjectLink',
                            'koalixcrm.crm.reporting.generic_task_link.GenericTaskLink',
                            'koalixcrm.crm.reporting.project_link_type.ProjectLinkType',
                            'koalixcrm.crm.reporting.project_status.ProjectStatus',
                            'koalixcrm.crm.reporting.reporting_period_status.ReportingPeriodStatus',
                            'koalixcrm.crm.reporting.resource.Resource',
                            'koalixcrm.crm.reporting.resource_manager.ResourceManager',
                            'koalixcrm.crm.reporting.resource_type.ResourceType',
                            'koalixcrm.crm.reporting.task_link_type.TaskLinkType',
                            'koalixcrm.crm.reporting.task_status.TaskStatus',),
                ),
                modules.ModelList(
                    _('PDF document settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.djangoUserExtension.user_extension.document_template.*',
                            'koalixcrm.djangoUserExtension.user_extension.template_set.TemplateSet',
                            'koalixcrm.djangoUserExtension.user_extension.user_extension.*',),
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


