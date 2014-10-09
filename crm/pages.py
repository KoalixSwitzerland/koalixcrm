from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import Page
from django.utils.translation import gettext as _


class CustomersPage(Page):

    class Meta:
        verbose_name = _("Customers Page")
        verbose_name_plural = _("Customers Pages")

    def can_delete(self, request):
        return request.user.is_superuser


class CurrenciesPage(Page):

    title = _("Currencies Page")
    login_required = True

    class Meta:
        verbose_name = _("Currencies Page")
        verbose_name_plural = _("Currencies Pages")

    def can_delete(self, request):
        return request.user.is_superuser

admin.site.register(CustomersPage, PageAdmin)
admin.site.register(CurrenciesPage, PageAdmin)