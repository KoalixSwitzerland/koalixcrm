from django.apps import apps
from rest_framework import serializers

from koalixcrm.core.models.tax import Tax


class OptionTaxJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'name')


class _AccountOptionSerializer(serializers.Serializer):
    """Minimal option serializer for `accounting.Account` that avoids a hard
    import from `koalixcrm.accounting` (WFS fork does not install that app).
    Input accepts `{'id': <pk>}` or null; output reads attrs off the Account
    instance via duck typing."""
    id = serializers.IntegerField(required=False, allow_null=True)
    account_number = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


def _get_account_model():
    return apps.get_model('accounting', 'Account')


class TaxJSONSerializer(serializers.ModelSerializer):
    tax_rate = serializers.CharField()
    name = serializers.CharField()
    account_activa = _AccountOptionSerializer(allow_null=True)
    account_passiva = _AccountOptionSerializer(allow_null=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'tax_rate',
                  'name',
                  'account_activa',
                  'account_passiva')

    def _resolve_account(self, payload):
        if not payload:
            return None
        account_id = payload.get('id', None)
        if not account_id:
            return None
        return _get_account_model().objects.get(id=account_id)

    def create(self, validated_data):
        tax = Tax()
        tax.tax_rate = validated_data['tax_rate']
        tax.name = validated_data['name']
        tax.account_activa = self._resolve_account(validated_data.pop('account_activa', None))
        tax.account_passiva = self._resolve_account(validated_data.pop('account_passiva', None))
        tax.save()
        return tax

    def update(self, instance, validated_data):
        instance.tax_rate = validated_data['tax_rate']
        instance.name = validated_data['name']
        instance.account_activa = self._resolve_account(validated_data.pop('account_activa', None))
        instance.account_passiva = self._resolve_account(validated_data.pop('account_passiva', None))
        instance.save()
        return instance
