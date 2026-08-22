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
                    # ADR-0003 Amendment 2026-06-27 renamed `ProductType` ->
                    # `Product` and moved it to `models/product.py`. This list
                    # still pointed at the old module, and because
                    # `modules.ModelList` silently drops patterns that match
                    # nothing, the panel rendered empty rather than erroring.
                    modules.ModelList(
                        _('Products'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.product.Product',
                                'koalixcrm.products.models.product_family.ProductFamily',
                                'koalixcrm.products.models.product_variant.ProductVariant',
                                'koalixcrm.products.models.product_media.ProductMedia',),
                    ),
                    # `ProductTranslation` and `CustomerGroupTransform` are
                    # deliberately absent: both are registered as inlines
                    # (on Product and PriceList respectively), not as
                    # standalone ModelAdmins, so a ModelList entry for them
                    # would never render.
                    modules.ModelList(
                        _('Pricing'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.price_list.PriceList',
                                'koalixcrm.products.models.product_price.ProductPrice',
                                'koalixcrm.products.models.unit_of_measure_conversion.'
                                'UnitOfMeasureConversion',),
                    ),
                    modules.ModelList(
                        _('Classification and Attributes'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.classification.Classification',
                                'koalixcrm.products.models.classification.ClassificationNode',
                                'koalixcrm.products.models.product_classification.ProductClassification',
                                'koalixcrm.products.models.attribute_group.AttributeGroup',
                                'koalixcrm.products.models.attribute_definition.AttributeDefinition',
                                'koalixcrm.products.models.attribute_set.AttributeSet',
                                'koalixcrm.products.models.attribute_validation_rule.'
                                'AttributeValidationRule',
                                'koalixcrm.products.models.product_attribute_mapping.'
                                'ProductAttributeMapping',),
                    ),
                    modules.ModelList(
                        _('Attribute Values (typed EAV tables)'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.product_attribute_string.'
                                'ProductAttributeString',
                                'koalixcrm.products.models.product_attribute_int.ProductAttributeInt',
                                'koalixcrm.products.models.product_attribute_decimal.'
                                'ProductAttributeDecimal',
                                'koalixcrm.products.models.product_attribute_bool.ProductAttributeBool',
                                'koalixcrm.products.models.product_attribute_enum.ProductAttributeEnum',
                                'koalixcrm.products.models.product_attribute_reference.'
                                'ProductAttributeReference',
                                'koalixcrm.products.models.product_attribute_mirror.'
                                'ProductAttributeMirror',),
                    ),
                    modules.ModelList(
                        _('Sourcing, Manufacturing and Compliance'),
                        column=1,
                        css_classes=('collapse closed',),
                        models=('koalixcrm.products.models.product_supply.ProductSupply',
                                'koalixcrm.products.models.bill_of_materials.BillOfMaterials',
                                'koalixcrm.products.models.bom_item.BomItem',
                                'koalixcrm.products.models.service_profile.ServiceProfile',
                                'koalixcrm.products.models.product_passport.ProductPassport',),
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

        # Stock domain (ADR-0009 … ADR-0017). Its own group rather than more
        # entries in the group above: the stock backbone is a peer domain of
        # products, not a subsection of it, and the combined list is long
        # enough that one collapsed group per domain stays scannable.
        # `GoodsReceiptLine` and `ProductionOrderComponent` are absent because
        # they are inlines on their parent aggregate, as are the movement
        # reason-code extensions.
        self.children.append(modules.Group(
            _('Stock'),
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    _('Warehouse Structure'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.stock.models.location.Location',
                            'koalixcrm.stock.models.handling_unit.HandlingUnit',),
                ),
                modules.ModelList(
                    _('Tracked Units'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.stock.models.serial_unit.SerialUnit',
                            'koalixcrm.stock.models.batch.Batch',),
                ),
                modules.ModelList(
                    _('Stock Levels and Movements'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.stock.models.on_hand_record.OnHandRecord',
                            'koalixcrm.stock.models.stock_balance.StockBalance',
                            'koalixcrm.stock.models.stock_movement.StockMovement',
                            'koalixcrm.stock.models.stock_reservation.StockReservation',),
                ),
                modules.ModelList(
                    _('Stock Operations'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.stock.models.goods_receipt.GoodsReceipt',
                            'koalixcrm.stock.models.production_order.ProductionOrder',
                            'koalixcrm.stock.models.rental_assignment.RentalAssignment',
                            'koalixcrm.stock.models.bill_of_materials_explosion.'
                            'BillOfMaterialsExplosion',),
                ),
                modules.ModelList(
                    _('Stock Settings'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.stock.models.movement_reason_code.MovementReasonCode',
                            'koalixcrm.stock.models.movement_reason_code_extension.'
                            'MovementReasonCodeExtension',
                            'koalixcrm.stock.models.retention_policy.RetentionPolicy',),
                ),
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
                # Superuser-only administration of the two authority signals:
                # which IdP issuers may provision groups (koalixcrm#430) and
                # which users are unrestricted service accounts (#432).
                # Grappelli hides entries the current user has no module
                # permission for, so this stays invisible to staff users.
                modules.ModelList(
                    _('Federated identity'),
                    column=2,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.core.models.oidc_tenant.OidcTenant',
                            'koalixcrm.core.models.service_account_grant.'
                            'ServiceAccountGrant',),
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
                # Operational view on async PDF jobs. Without this entry the
                # ModelAdmin is registered but unreachable from the dashboard,
                # so the "job(s) queued" messages point nowhere.
                modules.ModelList(
                    _('PDF exports'),
                    column=1,
                    css_classes=('collapse closed',),
                    models=('koalixcrm.core.models.pdf_export_process.'
                            'PDFExportProcess',),
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


