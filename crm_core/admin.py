import reversion
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from crm_core.models import UserExtension, Customer, Invoice, PurchaseOrder, Quote, Supplier


# Define an inline admin descriptor
# which acts a bit like a singleton
class CRMUserProfileInline(admin.TabularInline):
    model = UserExtension
    can_delete = False
    extra = 1
    max_num = 1
    verbose_name_plural = _('User Profile Extensions')


# Define a new User admin
class NewUserAdmin(UserAdmin):
    inlines = (CRMUserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)


# Define reversible models
class CustomerAdmin(reversion.VersionAdmin):
    pass


class InvoiceAdmin(reversion.VersionAdmin):
    pass


class QuoteAdmin(reversion.VersionAdmin):
    pass


class PurchaseorderAdmin(reversion.VersionAdmin):
    pass


class SupplierAdmin(reversion.VersionAdmin):
    pass


# register reversible classes
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(PurchaseOrder, PurchaseorderAdmin)
admin.site.register(Supplier, SupplierAdmin)