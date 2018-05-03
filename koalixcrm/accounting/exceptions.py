# -*- coding: utf-8 -*-


class ProgrammingError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NoObjectsToBeSerialzed(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AccountingPeriodNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TemplateSetMissingInAccountingPeriod(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

