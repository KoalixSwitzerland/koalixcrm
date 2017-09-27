# -*- coding: utf-8 -*-


class TemplateSetMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserExtensionMissing(Exception):
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