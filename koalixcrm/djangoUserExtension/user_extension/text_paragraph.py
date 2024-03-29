# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.crm.const.purpose import *


class TextParagraphInDocumentTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    document_template = models.ForeignKey("djangoUserExtension.DocumentTemplate", on_delete=models.CASCADE)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    class Meta:
        app_label = "crm"
        verbose_name = _('TextParagraphInDocumentTemplate')
        verbose_name_plural = _('TextParagraphInDocumentTemplates')

    def __str__(self):
        return str(self.id)


class InlineTextParagraph(admin.TabularInline):
    model = TextParagraphInDocumentTemplate
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('purpose', 'text_paragraph',)
        }),
    )
    allow_add = True