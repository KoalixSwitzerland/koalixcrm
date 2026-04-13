from rest_framework import serializers

from koalixcrm.accounting.models.product_category import ProductCategory
from koalixcrm.accounting.serializers.product_category_serializer import ProductCategoryMinimalJSONSerializer
from koalixcrm.products.models.product_type import ProductType
from koalixcrm.products.models.tax import Tax
from koalixcrm.products.models.unit import Unit
from koalixcrm.products.serializers.tax_serializer import OptionTaxJSONSerializer
from koalixcrm.products.serializers.unit_serializer import OptionUnitJSONSerializer


class ProductJSONSerializer(serializers.ModelSerializer):
    product_type_identifier = serializers.CharField(allow_null=True, required=False)
    default_unit = OptionUnitJSONSerializer(allow_null=True, required=False)
    tax = OptionTaxJSONSerializer(allow_null=True, required=False)
    accounting_product_category = ProductCategoryMinimalJSONSerializer(allow_null=True, required=False)

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
        product.product_type_identifier = validated_data.get('product_type_identifier')
        product.title = validated_data['title']

        # Deserialize default_unit
        default_unit = validated_data.pop('default_unit')
        if default_unit:
            if default_unit.get('id', None):
                product.default_unit = Unit.objects.get(id=default_unit.get('id', None))
            else:
                product.default_unit = None

        # Deserialize tax
        tax = validated_data.pop('tax')
        if tax:
            if tax.get('id', None):
                product.tax = Tax.objects.get(id=tax.get('id', None))
            else:
                product.tax = None

        # Deserialize product category
        product_category = validated_data.pop('accounting_product_category')
        if product_category:
            if product_category.get('id', None):
                product.accounting_product_category = ProductCategory.objects.get(id=product_category.get('id', None))
            else:
                product.accounting_product_category = None

        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.product_type_identifier = validated_data.get('product_type_identifier', instance.product_type_identifier)

        # Deserialize default_unit
        default_unit = validated_data.pop('default_unit', None)
        if default_unit:
            if default_unit.get('id', None):
                instance.default_unit = Unit.objects.get(id=default_unit.get('id', None))
            else:
                instance.default_unit = instance.default_unit
        else:
            instance.default_unit = None

        # Deserialize tax
        tax = validated_data.pop('tax', None)
        if tax:
            if tax.get('id', None):
                instance.tax = Tax.objects.get(id=tax.get('id', None))
            else:
                instance.tax = instance.tax
        else:
            instance.tax = None

        # Deserialize product category
        product_category = validated_data.pop('accounting_product_category', None)
        if product_category:
            if product_category.get('id', None):
                instance.accounting_product_category = ProductCategory.objects.get(
                    id=product_category.get('id', None))
            else:
                instance.accounting_product_category = instance.accounting_product_category
        else:
            instance.accounting_product_category = None

        instance.save()
        return instance
