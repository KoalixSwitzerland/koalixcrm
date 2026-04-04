from rest_framework import serializers
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.crm.serializers.currency_rest import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.serializers.template_set_rest import TemplateSetJSONSerializer


class OptionUserExtensionJSONSerializer(serializers.HyperlinkedModelSerializer):
    defaultTemplateSet = TemplateSetJSONSerializer(source='default_template_set')
    defaultCurrency = CurrencyJSONSerializer(source='default_currency')

    class Meta:
        model = UserExtension
        fields = ('id',
                  'user',
                  'defaultTemplateSet',
                  'defaultCurrency')
