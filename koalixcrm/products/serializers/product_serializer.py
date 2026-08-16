# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.core.models.tax import Tax
from koalixcrm.core.models.unit import Unit
from koalixcrm.core.serializers.tax_serializer import OptionTaxJSONSerializer
from koalixcrm.core.serializers.unit_serializer import OptionUnitJSONSerializer
from koalixcrm.products.models.choices import ProductKind, ProductLifecycleStatus
from koalixcrm.products.models.product import Product
from koalixcrm.products.services.product_lifecycle import validate_lifecycle_transition


class ProductJSONSerializer(serializers.ModelSerializer):
    """`Product` serializer (renamed from `ProductType` — ADR-0003
    Amendment 2026-06-27). The accounting product-category linkage is owned
    by `accounting.ProductCategoryAssignment` since CR-2c and surfaced
    through accounting-side serializers only."""
    product_type_identifier = serializers.CharField(allow_null=True, required=False)
    kind = serializers.ChoiceField(choices=ProductKind.choices)
    lifecycle_status = serializers.ChoiceField(choices=ProductLifecycleStatus.choices, required=False)
    base_uom = OptionUnitJSONSerializer(allow_null=True, required=False)
    tax_class = OptionTaxJSONSerializer(allow_null=True, required=False)

    class Meta:
        model = Product
        fields = ('id',
                  'product_type_identifier',
                  'title',
                  'description',
                  'kind',
                  'lifecycle_status',
                  'base_uom',
                  'tax_class',
                  'brand',
                  'manufacturer_party',
                  'country_of_origin',
                  'product_family')
        depth = 1

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        new_status = attrs.get('lifecycle_status')
        if new_status is not None:
            old_status = self.instance.lifecycle_status if self.instance is not None else None
            validate_lifecycle_transition(old_status, new_status)
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Product:
        product = Product()
        product.workspace = validated_data.get('workspace')
        product.product_type_identifier = validated_data.get('product_type_identifier')
        product.title = validated_data['title']
        product.description = validated_data.get('description')
        product.kind = validated_data['kind']
        product.lifecycle_status = validated_data.get('lifecycle_status', ProductLifecycleStatus.DRAFT)
        product.brand = validated_data.get('brand')
        product.manufacturer_party = validated_data.get('manufacturer_party')
        product.country_of_origin = validated_data.get('country_of_origin')
        product.product_family = validated_data.get('product_family')

        base_uom = validated_data.pop('base_uom', None)
        if base_uom and base_uom.get('id', None):
            product.base_uom = Unit.objects.get(id=base_uom.get('id'))

        tax_class = validated_data.pop('tax_class', None)
        if tax_class and tax_class.get('id', None):
            product.tax_class = Tax.objects.get(id=tax_class.get('id'))

        product.save()
        return product

    def update(self, instance: Product, validated_data: dict[str, Any]) -> Product:
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.product_type_identifier = validated_data.get(
            'product_type_identifier', instance.product_type_identifier
        )
        instance.kind = validated_data.get('kind', instance.kind)
        instance.lifecycle_status = validated_data.get('lifecycle_status', instance.lifecycle_status)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.manufacturer_party = validated_data.get('manufacturer_party', instance.manufacturer_party)
        instance.country_of_origin = validated_data.get('country_of_origin', instance.country_of_origin)
        instance.product_family = validated_data.get('product_family', instance.product_family)

        base_uom = validated_data.pop('base_uom', None)
        if base_uom and base_uom.get('id', None):
            instance.base_uom = Unit.objects.get(id=base_uom.get('id'))

        tax_class = validated_data.pop('tax_class', None)
        if tax_class and tax_class.get('id', None):
            instance.tax_class = Tax.objects.get(id=tax_class.get('id'))

        instance.save()
        return instance
