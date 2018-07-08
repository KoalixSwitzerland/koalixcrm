# -*- coding: utf-8 -*-

from django import forms


class TemplateSetMissingForUserExtension(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserExtensionMissing(Exception):
    class UserExtensionMissingForm(forms.Form):
        NEXT_STEPS = (
            ('create_user_extension', 'Create User Extension'),
            ('Return to Start', 'Return To Start'),
        )
        next_steps = forms.MultipleChoiceField(required=True,
                                               widget=forms.CheckboxSelectMultiple,
                                               choices=NEXT_STEPS)

    def __init__(self, value):
        self.value = value
        self.title = "User Extension Required"
        self.description = "You need to create a User Extension to access this view"

    def __str__(self):
        return repr(self.value)


class TooManyUserExtensionsAvailable(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserExtensionPhoneAddressMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UserExtensionEmailAddressMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)