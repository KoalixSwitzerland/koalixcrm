# -*- coding: utf-8 -*-
from koalixcrm.accounting.rest.account_rest import OptionAccountJSONSerializer
from rest_framework import serializers

from koalixcrm.accounting.accounting.product_category import ProductCategory
from koalixcrm.accounting.models import Account


class ProductCategoryMinimalJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'title')


class ProductCategoryJSONSerializer(serializers.HyperlinkedModelSerializer):
    profitAccount = OptionAccountJSONSerializer(source='profit_account')
    lossAccount = OptionAccountJSONSerializer(source='loss_account')

    class Meta:
        model = ProductCategory
        fields = ('id',
                  'title',
                  'profitAccount',
                  'lossAccount')
        depth = 1

    def create(self, validated_data):
        product_category = ProductCategory()
        product_category.title = validated_data['title']

        # Deserialize profit account
        profit_account = validated_data.pop('profit_account')
        if profit_account:
            if profit_account.get('id', None):
                product_category.profit_account = Account.objects.get(id=profit_account.get('id', None))
            else:
                product_category.profit_account = None

        # Deserialize loss account
        loss_account = validated_data.pop('loss_account')
        if loss_account:
            if loss_account.get('id', None):
                product_category.loss_account = Account.objects.get(id=loss_account.get('id', None))
            else:
                product_category.loss_account = None

        product_category.save()
        return product_category

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)

        # Deserialize profit account
        profit_account = validated_data.pop('profit_account')
        if profit_account:
            if profit_account.get('id', instance.profit_account_id):
                instance.profit_account = Account.objects.get(id=profit_account.get('id', None))
            else:
                instance.profit_account = instance.profit_account_id
        else:
            instance.profit_account = None

        # Deserialize loss account
        loss_account = validated_data.pop('loss_account')
        if loss_account:
            if loss_account.get('id', instance.loss_account_id):
                instance.loss_account = Account.objects.get(id=loss_account.get('id', None))
            else:
                instance.loss_account = instance.loss_account_id
        else:
            instance.loss_account = None

        instance.save()
        return instance
