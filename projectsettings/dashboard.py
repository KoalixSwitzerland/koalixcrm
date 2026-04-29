"""
This file was generated with the custom dashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'koalixcrm.dashboard.CustomIndexDashboard'
"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import Dashboard, modules

from koalixcrm.core.admin.dashboard_modules import WorkspaceSwitcherModule


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        # Workspace switcher — always the first module so the active workspace
        # is immediately visible after login.  CR-8 §8.6.
        self.children.append(WorkspaceSwitcherModule(column=1))

        self.children.append(modules.Group(
            _('koalixcrm Version ' + settings.KOALIXCRM_VERSION),
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
                            'koalixcrm.contracts.models.payment_reminder.PaymentReminder',
                            'koalixcrm.contracts.models.purchase_order.PurchaseOrder',),
                    ),
                    modules.ModelList(
                        _('Products'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.product_type.ProductType',),
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
                                'koalixcrm.reporting.models.human_resource.HumanResource',),
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

        # Support links — top of the right column.
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('koalixcrm on github'),
                    'url': 'https://github.com/KoalixSwitzerland/koalixcrm',
                    'external': True,
                },
            ]
        ))

        # Version Information
        self.children.append(modules.LinkList(
            title=_('Version Information'),
            column=2,
            children=[
                {'title': f'Backend Version: {settings.KOALIXCRM_VERSION}', 'url': '/version/'},
                {'title': 'API Version: v1', 'url': '/version/'},
            ]
        ))

        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Users, Access Rights and Application Settings'),
            column=2,
            collapsible=True,
            children=[
                modules.ModelList(
                    _('Administration'),
                    column=2,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
                modules.ModelList(
                    _('Workspaces'),
                    column=2,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.core.models.workspace.Workspace',),
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

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


