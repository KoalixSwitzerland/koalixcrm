from django.contrib import admin
# from mezzanine.core import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from crm_core.models import UserExtension


# Define an inline admin descriptor
# which acts a bit like a singleton
class CRMUserProfileInline(admin.TabularInline):
    model = UserExtension
    can_delete = False
    extra = 1
    max_num = 1
    verbose_name_plural = _('User Profile Extensions')


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (CRMUserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)