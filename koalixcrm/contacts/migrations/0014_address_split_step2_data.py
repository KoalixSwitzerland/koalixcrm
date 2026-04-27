# -*- coding: utf-8 -*-
"""Step 2 of the Address field migration: data migrate.

Copies address_line_2/3/4 to additional_address_line_1/2/3 and splits
address_line_1 into street + number using a language-conditional rule
based on settings.LANGUAGE_CODE evaluated at migration time.
"""
from django.conf import settings
from django.db import migrations


LEADING_NUMBER_LOCALES = {"en", "en-us", "en-gb", "en-ca", "en-au"}


def _is_leading_number_locale():
    code = (getattr(settings, "LANGUAGE_CODE", "") or "").lower()
    return code in LEADING_NUMBER_LOCALES


def _split_trailing(value):
    """Trailing token starting with a digit becomes number; rest is street."""
    if not value:
        return (value or None, None)
    tokens = value.rsplit(" ", 1)
    if len(tokens) == 2 and tokens[1] and tokens[1][0].isdigit():
        street = tokens[0].strip() or None
        number = tokens[1].strip() or None
        return (street, number)
    return (value, None)


def _split_leading(value):
    """Leading token starting with a digit becomes number; rest is street."""
    if not value:
        return (value or None, None)
    tokens = value.split(" ", 1)
    if len(tokens) == 2 and tokens[0] and tokens[0][0].isdigit():
        number = tokens[0].strip() or None
        street = tokens[1].strip() or None
        return (street, number)
    return (value, None)


def _split(value):
    if _is_leading_number_locale():
        return _split_leading(value)
    return _split_trailing(value)


def forwards(apps, schema_editor):
    Address = apps.get_model('contacts', 'Address')
    for addr in Address.objects.all():
        addr.additional_address_line_1 = addr.address_line_2
        addr.additional_address_line_2 = addr.address_line_3
        addr.additional_address_line_3 = addr.address_line_4
        street, number = _split(addr.address_line_1)
        addr.street = street
        addr.number = number
        addr.save(update_fields=[
            'street', 'number',
            'additional_address_line_1',
            'additional_address_line_2',
            'additional_address_line_3',
        ])


def backwards(apps, schema_editor):
    Address = apps.get_model('contacts', 'Address')
    for addr in Address.objects.all():
        if addr.street and addr.number:
            addr.address_line_1 = f"{addr.street} {addr.number}".strip()
        elif addr.street:
            addr.address_line_1 = addr.street
        elif addr.number:
            addr.address_line_1 = addr.number
        else:
            addr.address_line_1 = None
        addr.address_line_2 = addr.additional_address_line_1
        addr.address_line_3 = addr.additional_address_line_2
        addr.address_line_4 = addr.additional_address_line_3
        addr.save(update_fields=[
            'address_line_1', 'address_line_2',
            'address_line_3', 'address_line_4',
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0013_address_split_step1_add'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
