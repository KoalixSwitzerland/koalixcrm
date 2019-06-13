from rest_framework import serializers
from koalixcrm.djangoUserExtension.user_extension.user_extension import UserExtension
from koalixcrm.crm.rest.currency_rest import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.rest.template_set_rest import TemplateSetJSONSerializer


class OptionUserExtensionJSONSerializer(serializers.HyperlinkedModelSerializer):
    defaultTemplateSet = TemplateSetJSONSerializer(source='default_template_set')
    defaultCurrency = CurrencyJSONSerializer(source='default_currency')

    class Meta:
        model = UserExtension
        fields = ('id',
                  'user',
                  'defaultTemplateSet',
                  'defaultCurrency')
