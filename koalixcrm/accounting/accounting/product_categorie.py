# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _
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