from django.apps import apps
from rest_framework import serializers

from koalixcrm.products.models.product_type import ProductType
from koalixcrm.core.models.tax import Tax
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.tax_serializer import OptionTaxJSONSerializer
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer


class _ProductCategoryOptionSerializer(serializers.Serializer):
    """Minimal option serializer for `accounting.ProductCategory`.

    Avoids a hard import from `koalixcrm.accounting` — that app is not
    installed in the WFS fork. Input accepts `{'id': <pk>}` or null; output
    reads attrs off the ProductCategory instance via duck typing."""
    id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(read_only=True)


def _resolve_product_category(payload):
    if not payload or not apps.is_installed('koalixcrm.accounting'):
        return None
    category_id = payload.get('id', None)
    if not category_id:
        return None
    product_category_model = apps.get_model('accounting', 'ProductCategory')
    return product_category_model.objects.get(id=category_id)


class ProductJSONSerializer(serializers.ModelSerializer):
    product_type_identifier = serializers.CharField(allow_null=True, required=False)
    default_unit = OptionUnitJSONSerializer(allow_null=True, required=False)
    tax = OptionTaxJSONSerializer(allow_null=True, required=False)
    accounting_product_category = _ProductCategoryOptionSerializer(allow_null=True, required=False)

    class Meta:
        model = ProductType
        fields = ('id',
                  'product_type_identifier',
                  'title',
                  'default_unit',
                  'tax',
                  'accounting_product_category')
        depth = 1

    def create(self, validated_data):
        product = ProductType()
        product.workspace = validated_data.get('workspace')
        product.product_type_identifier = validated_data.get('product_type_identifier')
        product.title = validated_data['title']

        default_unit = validated_data.pop('default_unit', None)
        if default_unit and default_unit.get('id', None):
            product.default_unit = Unit.objects.get(id=default_unit.get('id'))
        else:
            product.default_unit = None

        tax = validated_data.pop('tax', None)
        if tax and tax.get('id', None):
            product.tax = Tax.objects.get(id=tax.get('id'))
        else:
            product.tax = None

        product.accounting_product_category = _resolve_product_category(
            validated_data.pop('accounting_product_category', None)
        )

        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.product_type_identifier = validated_data.get(
            'product_type_identifier', instance.product_type_identifier
        )

        default_unit = validated_data.pop('default_unit', None)
        if default_unit and default_unit.get('id', None):
            instance.default_unit = Unit.objects.get(id=default_unit.get('id'))
        else:
            instance.default_unit = None

        tax = validated_data.pop('tax', None)
        if tax and tax.get('id', None):
            instance.tax = Tax.objects.get(id=tax.get('id'))
        else:
            instance.tax = None

        instance.accounting_product_category = _resolve_product_category(
            validated_data.pop('accounting_product_category', None)
        )

        instance.save()
        return instance
