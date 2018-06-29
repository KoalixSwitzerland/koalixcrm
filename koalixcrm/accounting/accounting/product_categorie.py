# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
from rest_framework import serializers

from koalixcrm.accounting.accounting.account import AccountMinimalJSONSerializer
from koalixcrm.accounting.models import Account


class ProductCategorie(models.Model):
    title = models.CharField(verbose_name=_("Product Categorie Title"),
                             max_length=50)
    profit_account = models.ForeignKey(Account,
                                       verbose_name=_("Profit Account"),
                                       limit_choices_to={"account_type": "E"},
                                       related_name="db_profit_account")
    loss_account = models.ForeignKey(Account,
                                     verbose_name=_("Loss Account"),
                                     limit_choices_to={"account_type": "S"},
                                     related_name="db_loss_account")

    class Meta:
        app_label = "accounting"
        verbose_name = _('Product Categorie')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return self.title


class OptionProductCategorie(admin.ModelAdmin):
    list_display = ('title',
                    'profit_account',
                    'loss_account')
    list_display_links = ('title',
                          'profit_account',
                          'loss_account')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title',
                       'profit_account',
                       'loss_account')
        }),
    )
    save_as = True


class ProductCategoryJSONSerializer(serializers.HyperlinkedModelSerializer):
    profitAccount = AccountMinimalJSONSerializer(source='profit_account')
    lossAccount = AccountMinimalJSONSerializer(source='loss_account')

    class Meta:
        model = ProductCategorie
        fields = ('id',
                  'title',
                  'profitAccount',
                  'lossAccount')
        depth = 1

    def create(self, validated_data):
        product_category = ProductCategorie()
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
