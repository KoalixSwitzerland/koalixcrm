from rest_framework import serializers

from koalixcrm.core.models.currency import Currency


class CurrencyJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    short_name = serializers.CharField(required=False)
    rounding = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = Currency
        fields = ('id',
                  'description',
                  'short_name',
                  'rounding')
