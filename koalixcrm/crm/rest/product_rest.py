from rest_framework import serializers

from koalixcrm.accounting.accounting.product_category import ProductCategory
from koalixcrm.accounting.rest.product_categorie_rest import ProductCategoryMinimalJSONSerializer
from koalixcrm.crm.product.product_type import ProductType
from koalixcrm.crm.product.tax import Tax
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.rest.tax_rest import OptionTaxJSONSerializer
from koalixcrm.crm.rest.unit_rest import OptionUnitJSONSerializer


class ProductJSONSerializer(serializers.HyperlinkedModelSerializer):
    productNumber = serializers.IntegerField(source='product_number', allow_null=False)
    unit = OptionUnitJSONSerializer(source='default_unit', allow_null=False)
    tax = OptionTaxJSONSerializer(allow_null=False)
    productCategory = ProductCategoryMinimalJSONSerializer(source='accounting_product_categorie', allow_null=False)

    class Meta:
        model = ProductType
        fields = ('id',
                  'productNumber',
                  'title',
                  'unit',
                  'tax',
                  'productCategory')
        depth = 1

    def create(self, validated_data):
        product = ProductType()
        product.product_number = validated_data['product_number']
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
        product_category = validated_data.pop('accounting_product_categorie')
        if product_category:
            if product_category.get('id', None):
                product.accounting_product_category = ProductCategory.objects.get(id=product_category.get('id', None))
            else:
                product.accounting_product_category = None

        product.save()
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.product_number = validated_data['product_number']

        # Deserialize default_unit
        default_unit = validated_data.pop('default_unit')
        if default_unit:
            if default_unit.get('id', instance.default_unit):
                instance.default_unit = Unit.objects.get(id=default_unit.get('id', None))
            else:
                instance.default_unit = instance.default_unit
        else:
            instance.default_unit = None

        # Deserialize tax
        tax = validated_data.pop('tax')
        if tax:
            if tax.get('id', instance.default_unit):
                instance.tax = Tax.objects.get(id=tax.get('id', None))
            else:
                instance.tax = instance.tax
        else:
            instance.tax = None

        # Deserialize product category
        product_category = validated_data.pop('accounting_product_categorie')
        if product_category:
            if product_category.get('id', instance.accounting_product_categorie):
                instance.accounting_product_categorie = ProductCategory.objects.get(
                    id=product_category.get('id', None))
            else:
                instance.accounting_product_categorie = instance.accounting_product_categorie
        else:
            instance.accounting_product_categorie = None

        instance.save()
        return instance
