from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.core.models.tax import Tax
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.tax_serializer import OptionTaxJSONSerializer
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer
from koalixcrm.products.models.product_type import ProductType


class ProductJSONSerializer(serializers.ModelSerializer):
    """Core-level ProductType serializer. The accounting product-category
    linkage is owned by `accounting.ProductCategoryAssignment` since CR-2c
    and surfaced through accounting-side serializers only."""
    product_type_identifier = serializers.CharField(allow_null=True, required=False)
    default_unit = OptionUnitJSONSerializer(allow_null=True, required=False)
    tax = OptionTaxJSONSerializer(allow_null=True, required=False)

    class Meta:
        model = ProductType
        fields = ('id',
                  'product_type_identifier',
                  'title',
                  'default_unit',
                  'tax')
        depth = 1

    def create(self, validated_data: dict[str, Any]) -> ProductType:
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

        product.save()
        return product

    def update(self, instance: ProductType, validated_data: dict[str, Any]) -> ProductType:
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

        instance.save()
        return instance
