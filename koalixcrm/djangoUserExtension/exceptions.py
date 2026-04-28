# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any


class TemplateSetMissingForUserExtension(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class UserExtensionMissing(Exception):

    def __init__(self, value: Any) -> None:
        self.value = value
        self.view = "/koalixcrm/crm/reporting/user_extension_missing"

    def __str__(self) -> str:
        return repr(self.value)


class TooManyUserExtensionsAvailable(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class UserExtensionPhoneAddressMissing(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)


class UserExtensionEmailAddressMissing(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return repr(self.value)
