import django_tables2 as tables
from crm_core.custom.custom_columns import LabelColumn, ButtonsColumn, RelatedModelDetailLinkColumn
from crm_core.models import Contract
from django.utils.translation import ugettext_lazy as _


class ContractTable(tables.Table):
    quote = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_quote_detail_url }}'",
                "condition": "has_quotes",
            },
            {
                "extra_class": 'btn-info',
                "gl_icon": 'pencil',
                "onclick": "location.href='{{ record.get_quote_edit_url }}'",
                "condition": "has_quotes",
            }
        ],
        attrs={"th": {"width": "120px"}},
        orderable=False
    )
    purchase_order = ButtonsColumn(
        [
            {
                'extra_class': 'btn-default',
                'gl_icon': 'search',
                "onclick": "location.href='{{ record.get_purchaseorder_detail_url }}'",
                "condition": "has_purchaseorders",
            },
            {
                'extra_class': 'btn-info',
                'gl_icon': 'pencil',
                "onclick": "location.href='{{ record.get_purchaseorder_edit_url }}'",
                "condition": "has_purchaseorders",
            }
        ],
        attrs={"th": {"width": "120px"}},
        orderable=False
    )
    invoice = ButtonsColumn(
        [
            {
                'extra_class': 'btn-default',
                'gl_icon': 'search',
                "onclick": "location.href='{{ record.get_invoice_detail_url }}'",
                "condition": "has_invoices",
            },
            {
                'extra_class': 'btn-info',
                'gl_icon': 'pencil',
                "onclick": "location.href='{{ record.get_invoice_edit_url }}'",
                "condition": "has_invoices",
            }
        ],
        attrs={"th": {"width": "120px"}},
        orderable=False
    )
    state = LabelColumn(verbose_name=_('Status'))
    default_customer = RelatedModelDetailLinkColumn(verbose_name=_('Customer'))
    lastmodification = tables.DateTimeColumn()
    description = tables.Column(orderable=False, default="-")

    class Meta:
        model = Contract
        exclude = ('id', 'staff', 'default_supplier', 'default_currency', 'dateofcreation', 'lastmodifiedby')