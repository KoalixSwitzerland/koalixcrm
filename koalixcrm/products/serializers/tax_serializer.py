from rest_framework import serializers

from koalixcrm.accounting.models.account import Account
from koalixcrm.accounting.serializers.account_serializer import OptionAccountJSONSerializer
from koalixcrm.products.models.tax import Tax


class OptionTaxJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'name')


class TaxJSONSerializer(serializers.ModelSerializer):
    tax_rate = serializers.CharField()
    name = serializers.CharField()
    account_activa = OptionAccountJSONSerializer(allow_null=True)
    account_passiva = OptionAccountJSONSerializer(allow_null=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'tax_rate',
                  'name',
                  'account_activa',
                  'account_passiva')

    def create(self, validated_data):
        tax = Tax()
        tax.tax_rate = validated_data['tax_rate']
        tax.name = validated_data['name']

        # Deserialize account activa
        account_activa = validated_data.pop('account_activa')
        if account_activa:
            if account_activa.get('id', None):
                tax.account_activa = Account.objects.get(id=account_activa.get('id', None))
            else:
                tax.account_activa = None

        # Deserialize account passiva
        account_passiva = validated_data.pop('account_passiva')
        if account_passiva:
            if account_passiva.get('id', None):
                tax.account_passiva = Account.objects.get(id=account_passiva.get('id', None))
            else:
                tax.account_passiva = None

        tax.save()
        return tax

    def update(self, instance, validated_data):
        instance.tax_rate = validated_data['tax_rate']
        instance.name = validated_data['name']

        # Deserialize account activa
        account_activa = validated_data.pop('account_activa')
        if account_activa:
            if account_activa.get('id', instance.account_activa):
                instance.account_activa = Account.objects.get(id=account_activa.get('id', None))
            else:
                instance.account_activa = instance.account_activa_id
        else:
            instance.account_activa = None

        # Deserialize account passiva
        account_passiva = validated_data.pop('account_passiva')
        if account_passiva:
            if account_passiva.get('id', instance.account_passiva):
                instance.account_passiva = Account.objects.get(id=account_passiva.get('id', None))
            else:
                instance.account_passiva = instance.account_passiva_id
        else:
            instance.account_passiva = None

        instance.save()
        return instance
