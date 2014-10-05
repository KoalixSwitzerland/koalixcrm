from mezzanine.pages.models import Page, PageMoveException
from crm.models import Contact, Currency, Customer, CustomerGroup


class CRMpage(Page):

    class Meta:
        verbose_name = "CRM Page"
        verbose_name_plural = "CRM Pages"

    def can_add(self, request):
        return self.children.count() == 0

    def can_delete(self, request):
        return request.user.is_superuser or self.parent is not None

    def can_move(self, request, new_parent):
        if new_parent is None:
            msg = 'An author page cannot be a top-level page'
            raise PageMoveException(msg)