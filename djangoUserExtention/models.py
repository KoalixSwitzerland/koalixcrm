# -*- coding: utf-8 -*-
from django.db import models
import crm

class UserExtention(models.Model):
   user = models.OneToOneField(auth.user)
   postalAddress = models.ForeignKey('UserExtentionPostalAddress')
   phoneAddress = models.ForeignKey('UserExtentionPhoneAddress')
   emailAddress = models.ForeignKey('UserExtentionEmailAddress')
   defaultTemplateSet = models.ForeignKey('TemplateSet')
   
   class Meta:
      app_label = "Configuration"
      verbose_name = _('User Extention')
      verbose_name_plural = _('User Extentions')
      
class TemplateSet(models.Model):
   invoiceXSLFiles = models.ForeignKey('XSLFile', verbose_name=_("XSL File for Invoice"))
   quoteXSLFiles = models.ForeignKey('XSLFile', verbose_name=_("XSL File for Quote"))
   purchaseOrderXSLFiles = models.ForeignKey('XSLFile', verbose_name=_("XSL File for Purchaseorder"))
   salesOrderXSLFiles = models.ForeignKey('XSLFile', verbose_name=_("XSL File for Salesorder"))
   logo = models.FileField(verbose_name=_("Logo for the PDF generation"))
   footerText = models.TextField()
   headerText = models.TextField()
      
   class Meta:
      app_label = "Configuration"
      verbose_name = _('User Extention')
      verbose_name_plural = _('User Extentions')

class XSLFile(models.Model)
   
   
class UserExtentionPostalAddress(crm.PostalAddress)
   
class UserExtentionPhoneAddress(crm.PhoneAddress):

class UserExtentionEmailAddress(crm.EmailAddress):
