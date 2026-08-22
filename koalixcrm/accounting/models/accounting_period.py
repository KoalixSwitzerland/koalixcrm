# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django import forms
from django.contrib import admin, messages
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from koalixcrm.accounting.exceptions import AccountingPeriodNotFound
from koalixcrm.accounting.models.account import Account
from koalixcrm.accounting.models.booking import InlineBookings
from koalixcrm.core.pdf_export_messages import pdf_export_queued_message

if TYPE_CHECKING:
    from django.http import HttpRequest


class AccountingPeriod(models.Model):
    """Accounting period represents the equivalent of the business logic element of a fiscal year
    the accounting period is referred in the booking and is used as a supporting object to generate
    balance sheets and profit/loss statements"""

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))  # For example "Year 2009", "1st Quarter 2009"
    begin = models.DateField(verbose_name=_("Begin"))
    end = models.DateField(verbose_name=_("End"))
    template_set_balance_sheet = models.ForeignKey(
        "djangoUserExtension.DocumentTemplate",
        on_delete=models.CASCADE,
        verbose_name=_("Referred template for balance sheet"),
        related_name="db_balancesheet_template_set",
        null=True,
        blank=True,
    )
    template_profit_loss_statement = models.ForeignKey(
        "djangoUserExtension.DocumentTemplate",
        on_delete=models.CASCADE,
        verbose_name=_("Referred template for profit, loss statement"),
        related_name="db_profit_loss_statement_template_set",
        null=True,
        blank=True,
    )

    def overall_earnings(self) -> Decimal:
        earnings: Decimal = Decimal(0)
        for account in list(Account.objects.all()):
            if account.account_type == "E":
                earnings += account.sum_of_all_bookings_within_accounting_period(self)
        return earnings

    def overall_spendings(self) -> Decimal:
        spendings: Decimal = Decimal(0)
        for account in list(Account.objects.all()):
            if account.account_type == "S":
                spendings += account.sum_of_all_bookings_within_accounting_period(self)
        return spendings

    def overall_assets(self) -> Decimal:
        assets: Decimal = Decimal(0)
        for account in list(Account.objects.all()):
            if account.account_type == "A":
                assets += account.sum_of_all_bookings_through_now(self)
        return assets

    def overall_liabilities(self) -> Decimal:
        liabilities: Decimal = Decimal(0)
        for account in list(Account.objects.all()):
            if account.account_type == "L":
                liabilities += account.sum_of_all_bookings_through_now(self)
        return liabilities

    @staticmethod
    def get_current_valid_accounting_period() -> AccountingPeriod:
        """Returns the accounting period that is currently valid. Valid is an accounting_period when the current date
          lies between begin and end of the accounting_period

        Args:
          no arguments

        Returns:
          accounting_period (AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.begin < date.today() and accounting_period.end > date.today():
                return accounting_period
        raise AccountingPeriodNotFound("The accounting period was not found")

    def get_all_prior_accounting_periods(self) -> list[AccountingPeriod]:
        """Returns the accounting period that is currently valid. Valid is an accountingPeriod when the current date
          lies between begin and end of the accountingPeriod

        Args:
          no arguments

        Returns:
          accounting_period (List of AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        accounting_periods: list[AccountingPeriod] = []
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.end < self.begin:
                accounting_periods.append(accounting_period)
        if not accounting_periods:
            raise AccountingPeriodNotFound("Accounting Period does not exist")
        return accounting_periods

    def __str__(self) -> str:
        return self.title

        # TODO: def createNewAccountingPeriod() Neues Geschäftsjahr erstellen

    class Meta:
        app_label = "accounting"
        verbose_name = _("Accounting Period")
        verbose_name_plural = _("Accounting Periods")


class AccountingPeriodForm(forms.ModelForm):
    """AccountingPeriodForm is used to overwrite the clean method of the
    original form and to add an additional check to the model"""

    class Meta:
        model = AccountingPeriod
        fields = "__all__"

    def clean(self) -> dict[str, Any]:
        super().clean()
        errors: list[str] = []
        try:
            if self.cleaned_data["begin"] > self.cleaned_data["end"]:
                errors.append(_("The begin date cannot be later than the end date."))
        except KeyError:
            errors.append(_("The begin and the end date may not be empty"))
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccountingPeriod(admin.ModelAdmin):
    list_display = ("title", "begin", "end", "template_set_balance_sheet", "template_profit_loss_statement")
    list_display_links = ("title", "begin", "end", "template_set_balance_sheet", "template_profit_loss_statement")
    fieldsets = (
        (
            _("Basics"),
            {"fields": ("title", "begin", "end", "template_set_balance_sheet", "template_profit_loss_statement")},
        ),
    )
    inlines = [
        InlineBookings,
    ]
    save_as = True

    form = AccountingPeriodForm

    def save_formset(self, request: HttpRequest, form: Any, formset: Any, change: bool) -> None:
        instances = formset.save(commit=False)
        for instance in instances:
            if change:
                instance.last_modified_by = request.user
            else:
                instance.last_modified_by = request.user
                instance.staff = request.user
            instance.save()

    def _enqueue_async_pdf(
        self,
        request: HttpRequest,
        queryset: QuerySet[AccountingPeriod],
        template_attr: str,
        label: str,
    ) -> None:
        """Enqueue a PDFExportProcess per selected period for the given report
        (balance sheet or profit/loss statement). The Java pdf-export-service
        picks the message up from SQS and renders the PDF asynchronously —
        watch the PDF Export Processes admin for status / result URL.
        """
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess

        queued = 0
        # No `or Workspace.objects.first()` fallback: attributing an export to
        # whichever tenant happens to sort first is a wrong answer, not a
        # lenient one (REQ-0028 AC-10).
        workspace = getattr(request, "active_workspace", None)
        if workspace is None:
            self.message_user(
                request,
                _("No active workspace — switch to a workspace before exporting."),
                level=messages.ERROR,
            )
            return
        for obj in queryset:
            template = getattr(obj, template_attr)
            if not template:
                self.message_user(
                    request,
                    _("Template missing for %(label)s on %(period)s") % {"label": label, "period": obj},
                    level=messages.ERROR,
                )
                continue
            PDFExportProcess.objects.create(
                workspace=workspace,
                source_model=obj.__class__.__name__,
                source_id=obj.id,
                template_set=template,
                triggered_by=request.user,
            )
            queued += 1
        if queued:
            self.message_user(
                request,
                pdf_export_queued_message(queued, label),
                level=messages.SUCCESS,
            )

    def create_pdf_of_balance_sheet(self, request: HttpRequest, queryset: QuerySet[AccountingPeriod]) -> None:
        self._enqueue_async_pdf(request, queryset, "template_set_balance_sheet", _("Balance Sheet"))

    create_pdf_of_balance_sheet.short_description = _("Create PDF of Balance Sheet")

    def create_pdf_of_profit_loss_statement(self, request: HttpRequest, queryset: QuerySet[AccountingPeriod]) -> None:
        self._enqueue_async_pdf(request, queryset, "template_profit_loss_statement", _("Profit/Loss Statement"))

    create_pdf_of_profit_loss_statement.short_description = _("Create PDF of Profit Loss Statement Sheet")

    actions = ["create_pdf_of_balance_sheet", "create_pdf_of_profit_loss_statement"]
