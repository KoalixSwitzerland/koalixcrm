# -*- coding: utf-8 -*-

class OptionUserExtention(admin.ModelAdmin):
   list_display = ('id', 'description', 'defaultcustomer', 'defaultdistributor', 'staff')
   list_display_links = ('id','description', 'defaultcustomer', 'defaultdistributor')       
   list_filter    = ('defaultcustomer', 'defaultdistributor', 'staff')
   ordering       = ('id', 'defaultcustomer')
   search_fields  = ('id','contract')
   fieldsets = (
      (_('Basics'), {
         'fields': ('description', 'defaultcustomer', 'defaultdistributor')
      }),
   )
   save_as = True
   inlines = [UserExtentionPostalAddress, UserExtentionPhoneAddress, UserExtentionEmailAddress]
   