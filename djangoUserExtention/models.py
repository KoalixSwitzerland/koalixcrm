# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.db import models
from filebrowser.fields import FileBrowseField
from const.purpose import *
import crm
   
class XSLFile(models.Model):
   title = models.CharField(verbose_name = _("Title"), max_length=100, blank=True, null=True)
   xslfile = FileBrowseField(verbose_name=_("XSL File"), max_length=200)
   
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('XSL File')
      verbose_name_plural = _('XSL Files')
      
   def __unicode__(self):
      return str(self.id) + ' ' + self.title
      
class UserExtention(models.Model):
   user = models.ForeignKey('auth.User')
   defaultTemplateSet = models.ForeignKey('TemplateSet')
   
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('User Extention')
      verbose_name_plural = _('User Extentions')
      
   def __unicode__(self):
      return str(self.id) + ' ' + self.user.__unicode__()
      
class TemplateSet(models.Model):
   title = models.CharField(verbose_name = _("Title"), max_length=100)
   invoiceXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Invoice"), related_name="db_reltemplateinvoice")
   quoteXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Quote"), related_name="db_reltemplatequote")
   purchaseconfirmationXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Purchaseorder"), related_name="db_reltemplatepurchaseorder")
   deilveryorderXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Deilvery Order"), related_name="db_reltemplatedeliveryorder")
   profitLossStatementXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Profit Loss Statement"), related_name="db_reltemplateprofitlossstatement")
   balancesheetXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Balancesheet"), related_name="db_reltemplatebalancesheet")
   logo = FileBrowseField(verbose_name=_("Logo for the PDF generation"), blank=True, null=True, max_length=200)
   fopConfigurationFile = FileBrowseField(verbose_name=_("FOP Configuration File"), blank=True, null=True, max_length=200)
   footerTextsalesorders = models.TextField(verbose_name=_("Footer Text On Salesorders"), blank=True, null=True)
   headerTextsalesorders = models.TextField(verbose_name=_("Header Text On Salesorders"), blank=True, null=True)
   headerTextpurchaseorders = models.TextField(verbose_name=_("Header Text On Purchaseorders"), blank=True, null=True)
   footerTextpurchaseorders = models.TextField(verbose_name=_("Footer Text On Purchaseorders"), blank=True, null=True)
   pagefooterleft = models.CharField(max_length=40, verbose_name=_("Page Footer Left"), blank=True, null=True)
   pagefootermiddle = models.CharField(max_length=40, verbose_name=_("Page Footer Middle"), blank=True, null=True)
      
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('Templateset')
      verbose_name_plural = _('Templatesets')
      
   def __unicode__(self):
      return str(self.id) + ' ' + self.title
   

class UserExtentionPostalAddress(crm.models.PostalAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
   userExtention = models.ForeignKey(UserExtention)
   
   def __unicode__(self):
      return self.name + ' ' + self.prename
   
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('Postal Address for User Extention')
      verbose_name_plural = _('Postal Address for User Extention')
   
class UserExtentionPhoneAddress(crm.models.PhoneAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
   userExtention = models.ForeignKey(UserExtention)
   
   def __unicode__(self):
      return self.phone
   
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('Phonenumber for User Extention')
      verbose_name_plural = _('Phonenumber for User Extention')

class UserExtentionEmailAddress(crm.models.EmailAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINUSEREXTENTION)
   userExtention = models.ForeignKey(UserExtention)
   
   def __unicode__(self):
      return self.email
   
   class Meta:
      app_label = "djangoUserExtention"
      #app_label_koalix = _('Djang User Extention')
      verbose_name = _('Email Address for User Extention')
      verbose_name_plural = _('Email Address for User Extention')