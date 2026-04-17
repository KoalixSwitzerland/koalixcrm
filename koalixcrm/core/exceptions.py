# -*- coding: utf-8 -*-


class TemplateSetMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TemplateMissingInTemplateSet(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TemplateSetMissingInContract(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TemplateFOPConfigFileMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TemplateXSLTFileMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoSerializationPatternFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class OpenInterestAccountMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IncompleteInvoice(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvoiceAlreadyRegistered(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserIsNoHumanResource(Exception):
    def __init__(self, value):
        self.value = value
        self.view = "/koalixcrm/crm/reporting/user_is_not_human_resource"

    def __str__(self):
        return repr(self.value)


class ReportingPeriodDoneDeleteNotPossible(Exception):
    def __init__(self, value=None):
        self.value = value
        self.view = "/koalixcrm/crm/reporting/reporting_period_done_delete_not_possible"

    def __str__(self):
        return repr(self.value)


class ReportingPeriodNotFound(Exception):
    def __init__(self, value):
        self.value = value
        self.view = "/koalixcrm/crm/reporting/reporting_period_missing"

    def __str__(self):
        return repr(self.value)
