# -*- coding: utf-8 -*-
from __future__ import annotations


class ProgrammingError(Exception):
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class NoObjectsToBeSerialzed(Exception):
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class AccountingPeriodNotFound(Exception):
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class TemplateSetMissingInAccountingPeriod(Exception):
    def __init__(self, value: object) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)
