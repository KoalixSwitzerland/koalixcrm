import django_tables2 as tables
from crm_core.custom.custom_columns import LabelColumn, ButtonsColumn, RelatedModelDetailLinkColumn, \
    ModelDetailLinkColumn
from crm_core.models import Contract
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
                "extra_class": 'btn-info',
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
                "extra_class": "btn-info",
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
                "extra_class": "btn-info",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_invoice_edit_url }}'",
                "condition": "record.has_invoices",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False
    )
    edit_status = ButtonsColumn(
        [
            {
                "extra_class": "btn-primary",
                "gl_icon": "list-alt",
                "onclick": "location.href='{% url 'contract_create_quote' record.pk %}'",
                "condition": "not record.has_quotes"
            },
            {
                "extra_class": "btn-success",
                "gl_icon": "shopping-cart",
                "onclick": "location.href='{% url 'contract_create_purchaseorder' record.pk %}'",
                "condition": "not record.has_purchaseorders"
            },
            {
                "extra_class": "btn-warning",
                "gl_icon": "usd",
                "onclick": "location.href='{% url 'contract_create_invoice' record.pk %}'",
                "condition": "not record.has_invoices"
            }
        ],
        attrs={"th": {"width": "120px"}},
        orderable=False
    )
    edit_contract = ButtonsColumn(
        [
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
        attrs={"th": {"width": "90px"}},
        orderable=False
    )

    class Meta:
        model = Contract
        exclude = ('id', 'staff', 'default_supplier', 'default_currency', 'dateofcreation', 'lastmodifiedby')
        sequence = ('state', 'name', 'default_customer', 'description', 'lastmodification')