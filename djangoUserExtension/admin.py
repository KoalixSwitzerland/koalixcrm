# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.contrib import admin
from djangoUserExtention.models import *

class InlineUserExtentionPostalAddress(admin.StackedInline):
   model = UserExtentionPostalAddress
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode', 'town', 'state', 'country', 'purpose')
      }),
   )
   allow_add = True
   
class InlineUserExtentionPhoneAddress(admin.StackedInline):
   model = UserExtentionPhoneAddress
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('phone', 'purpose',)
      }),
   )
   allow_add = True
   
class InlineUserExtentionEmailAddress(admin.StackedInline):
   model = UserExtentionEmailAddress
   extra = 1
   classes = ('collapse-open',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('email', 'purpose',)
      }),
   )
   allow_add = True
   
class OptionUserExtention(admin.ModelAdmin):
   list_display = ('id', 'user', 'defaultTemplateSet')
   list_display_links = ('id', 'user')       
   list_filter    = ('user', 'defaultTemplateSet')
   ordering       = ('id', )
   search_fields  = ('id','user')
   fieldsets = (
      (_('Basics'), {
         'fields': ('user', 'defaultTemplateSet')
      }),
   )
   save_as = True
   inlines = [InlineUserExtentionPostalAddress, InlineUserExtentionPhoneAddress, InlineUserExtentionEmailAddress]
   
class OptionTemplateSet(admin.ModelAdmin):
   list_display = ('id', 'title')
   list_display_links = ('id', 'title')
   ordering       = ('id',)
   search_fields  = ('id', 'title', 'organisationname', 'invoiceXSLFile', 'quoteXSLFile', 'purchaseconfirmationXSLFile',
   'deilveryorderXSLFile', 'profitLossStatementXSLFile', 'balancesheetXSLFile', 
   'logo', 'footerTextsalesorders', 'headerTextsalesorders', 
   'headerTextpurchaseorders', 'footerTextpurchaseorders', 'pagefooterleft', 'pagefootermiddle'
   )
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'organisationname', 'invoiceXSLFile', 'quoteXSLFile', 'purchaseconfirmationXSLFile',
   'deilveryorderXSLFile', 'profitLossStatementXSLFile', 'balancesheetXSLFile', 
   'logo', 'fopConfigurationFile', 'footerTextsalesorders', 'headerTextsalesorders', 
   'headerTextpurchaseorders', 'footerTextpurchaseorders', 'pagefooterleft', 'pagefootermiddle')
      }),
   )
   
class OptionXSLFile(admin.ModelAdmin):
   list_display = ('id', 'title')
   list_display_links = ('id', 'title')
   ordering       = ('id',)
   fieldsets = (
      (_('Basics'), {
         'fields': ('title', 'xslfile',)
      }),
   )
   allow_add = True
   
   

admin.site.register(UserExtention, OptionUserExtention)
admin.site.register(TemplateSet, OptionTemplateSet)
admin.site.register(XSLFile, OptionXSLFile)