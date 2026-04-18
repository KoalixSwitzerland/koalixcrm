"""
This file was generated with the custom dashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'koalixcrm.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from koalixcrm.version import KOALIXCRM_VERSION


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        self.children.append(modules.Group(
            _('koalixcrm Version ' + KOALIXCRM_VERSION),
            column=1,
            collapsible=True,
            children=[
                   modules.ModelList(
                    _('Commercial Documents and Contracts'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.contracts.models.contract.Contract',
                            'koalixcrm.contracts.models.quotation.Quotation',
                            'koalixcrm.contracts.models.sales_order.SalesOrder',
                            'koalixcrm.contracts.models.despatch_advice.DespatchAdvice',
                            'koalixcrm.contracts.models.invoice.Invoice',
                            'koalixcrm.contracts.models.credit_note.CreditNote',
                            'koalixcrm.contracts.models.payment_reminder.PaymentReminder',),
                    ),
                    modules.ModelList(
                        _('Products'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.product.Product',),
                    ),
                    modules.ModelList(
                        _('Parties'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.contacts.models.organization.Organization',
                                'koalixcrm.contacts.models.natural_person.PartyContact',
                                'koalixcrm.contacts.models.party.Party',
                                'koalixcrm.contacts.models.party_role.PartyRole',
                                'koalixcrm.contacts.models.organization_membership.OrganizationMembership',
                                'koalixcrm.contacts.models.organization_relationship.OrganizationRelationship',),
                    ),
                    modules.ModelList(
                        _('Addresses & Contact Mechanisms'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.contacts.models.address.Address',
                                'koalixcrm.contacts.models.address_assignment.AddressAssignment',
                                'koalixcrm.contacts.models.phone_number.PhoneNumber',
                                'koalixcrm.contacts.models.phone_assignment.PhoneAssignment',
                                'koalixcrm.contacts.models.party_email.PartyEmail',
                                'koalixcrm.contacts.models.email_assignment.EmailAssignment',),
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
                        models=('koalixcrm.reporting.models.project.Project',
                                'koalixcrm.reporting.models.reporting_period.ReportingPeriod',
                                'koalixcrm.reporting.models.task.Task',
                                'koalixcrm.reporting.models.agreement.Agreement',
                                'koalixcrm.reporting.models.estimation.Estimation',
                                'koalixcrm.reporting.models.human_resource.HumanResource',
                                'koalixcrm.contracts.models.purchase_order.PurchaseOrder',),
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
                    models=('koalixcrm.contacts.models.customer_billing_cycle.CustomerBillingCycle',
                            'koalixcrm.contacts.models.party_group.PartyGroup',
                            'koalixcrm.contacts.models.party_group_membership.PartyGroupMembership',
                            'koalixcrm.contacts.models.party_identification.PartyIdentification',),
                ),
                modules.ModelList(
                    _('Product settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.core.models.tax.Tax',
                            'koalixcrm.core.models.unit.Unit',
                            'koalixcrm.core.models.currency.Currency'),
                ),
                modules.ModelList(
                    _('Reporting settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.reporting.models.agreement_status.AgreementStatus',
                            'koalixcrm.reporting.models.agreement_type.AgreementType',
                            'koalixcrm.reporting.models.estimation_status.EstimationStatus',
                            'koalixcrm.reporting.models.generic_project_link.GenericProjectLink',
                            'koalixcrm.reporting.models.generic_task_link.GenericTaskLink',
                            'koalixcrm.reporting.models.project_link_type.ProjectLinkType',
                            'koalixcrm.reporting.models.project_status.ProjectStatus',
                            'koalixcrm.reporting.models.reporting_period_status.ReportingPeriodStatus',
                            'koalixcrm.reporting.models.resource.Resource',
                            'koalixcrm.reporting.models.resource_manager.ResourceManager',
                            'koalixcrm.reporting.models.resource_type.ResourceType',
                            'koalixcrm.reporting.models.task_link_type.TaskLinkType',
                            'koalixcrm.reporting.models.task_status.TaskStatus',),
                ),
                modules.ModelList(
                    _('PDF document settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.djangoUserExtension.models.document_template.*',
                            'koalixcrm.djangoUserExtension.models.template_set.TemplateSet',
                            'koalixcrm.djangoUserExtension.models.user_extension.*',),
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


