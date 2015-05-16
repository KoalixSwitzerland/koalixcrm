# -*- coding: utf-8 -*

from django.utils.translation import ugettext_lazy as _


CONTRACT_STATE_CHOICES = (
    (10, _('open')),
    (20, _('payed')),
    (30, _('Invoice created')),
    (40, _('Invoice sent')),
    (50, _('Quote created')),
    (60, _('Quote sent')),
    (70, _('Purchaseorder created')),
    (90, _('Unpayed')),
    (100, _('Deleted'))
)


CONTRACT_LABEL_CLASS_CHOICES = (
    (10, 'danger'),
    (20, 'default'),
    (30, 'warning'),
    (40, 'warning'),
    (50, 'primary'),
    (60, 'primary'),
    (70, 'success'),
    (90, 'info'),
    (100, 'default')
)
