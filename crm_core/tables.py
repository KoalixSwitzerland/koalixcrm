import django_tables2 as tables
from crm_core.custom.custom_columns import LabelColumn, ButtonsColumn, RelatedModelDetailLinkColumn, \
    ModelDetailLinkColumn, ButtonColumn, IncludeColumn
from crm_core.models import Contract, Customer, Supplier, Product, TaxRate, CustomerBillingCycle, Unit, \
    ProductCategory, CustomerGroup
from django.utils.translation import ugettext_lazy as _


class ContractTable(tables.Table):
    state = LabelColumn(verbose_name=_('Status'))
    name = ModelDetailLinkColumn(sortable=False)
    default_customer = RelatedModelDetailLinkColumn(verbose_name=_('Customer'))
    description = tables.Column(orderable=False, default="-")
    lastmodification = tables.DateTimeColumn()

    quote = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_quote_detail_url }}'",
                "condition": "record.has_quotes",
            },
            {
                "extra_class": 'btn-primary',
                "gl_icon": 'pencil',
                "onclick": "location.href='{{ record.get_quote_edit_url }}'",
                "condition": "record.has_quotes",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    purchase_order = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_purchaseorder_detail_url }}'",
                "condition": "record.has_purchaseorders",
            },
            {
                "extra_class": "btn-success",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_purchaseorder_edit_url }}'",
                "condition": "record.has_purchaseorders",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    invoice = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_invoice_detail_url }}'",
                "condition": "record.has_invoices",
            },
            {
                "extra_class": "btn-warning",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_invoice_edit_url }}'",
                "condition": "record.has_invoices",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    edit_status = IncludeColumn('crm_core/includes/contract_row_actions_toolbar.html',
                                attrs={"th": {"width": "120px"}},
                                verbose_name=" ",
                                orderable=False
                                )
    edit_contract = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{% url 'contract_detail' record.pk %}'"
            },
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'contract_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'contract_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Contract
        exclude = ('id', 'staff', 'default_supplier', 'default_currency', 'dateofcreation', 'lastmodifiedby')
        sequence = ('state', 'name', 'default_customer', 'description', 'lastmodification')


class CustomerTable(tables.Table):
    name_prefix = tables.TemplateColumn("""{{ record.get_prefix }}""", orderable=False, verbose_name=_('Prefix'))
    new_contract = ButtonColumn(onclick="location.href='{% url 'customer_create_contract' record.pk %}'",
                                gl_icon='star', extra_class='btn-success',
                                attrs={"th": {"width": "70px"}}, orderable=False)
    edit_customer = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{% url 'customer_detail' record.pk %}'"
            },
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'customer_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'customer_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Customer
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'contact_ptr')
        sequence = ('name_prefix', 'firstname', 'name', 'default_currency')


class SupplierTable(tables.Table):
    name_prefix = tables.TemplateColumn("""{{ record.get_prefix }}""", orderable=False, verbose_name=_('Prefix'))
    edit_customer = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{% url 'supplier_detail' record.pk %}'"
            },
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'supplier_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'supplier_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Supplier
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'contact_ptr')
        sequence = ('name_prefix', 'name', 'default_currency')


class ProductTable(tables.Table):
    product = tables.Column(accessor='get_product_number', orderable=False, verbose_name=_('Prefix'))
    price = tables.Column(accessor='get_price', orderable=False, verbose_name=_('Price'))
    edit_customer = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{% url 'product_detail' record.pk %}'"
            },
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'product_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'product_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Product
        exclude = ('id', 'item_category', 'item_prefix', 'dateofcreation', 'lastmodification', 'lastmodifiedby',
                   'product_number', 'productitem_ptr')
        sequence = ('product', 'item_title', 'item_description', 'price')


class TaxTable(tables.Table):
    edit_tax = ButtonsColumn(
        [
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'tax_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'tax_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = TaxRate
        exclude = ('id', )


class BillingCycleTable(tables.Table):
    edit_billingcycle = ButtonsColumn(
        [
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'customerbillingcycle_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'customerbillingcycle_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerBillingCycle
        exclude = ('id', )


class UnitTable(tables.Table):
    edit_unit = ButtonsColumn(
        [
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'unit_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'unit_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Unit
        exclude = ('id', )


class ProductCategoryTable(tables.Table):
    edit_productcategory = ButtonsColumn(
        [
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'productcategory_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'productcategory_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = ProductCategory
        exclude = ('id', )


class CustomerGroupTable(tables.Table):
    edit_customergroup = ButtonsColumn(
        [
            {
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{% url 'customergroup_edit' record.pk %}'"
            },
            {
                "extra_class": "btn-danger",
                "gl_icon": "trash",
                "onclick": "location.href='{% url 'customergroup_delete' record.pk %}'"
            }
        ],
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerGroup
        exclude = ('id', )