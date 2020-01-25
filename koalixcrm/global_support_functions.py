# -*- coding: utf-8 -*-

import datetime

import pytz


def limit_string_length(input_string, maximum_length):
    if len(input_string) > maximum_length:
        output_string = input_string[:maximum_length]
    else:
        output_string = input_string
    return output_string


def get_string_between(input_string, search_start, search_end):
    pos_start = input_string.index(search_start)
    pos_end = input_string.index(search_end)
    output_string = input_string[pos_start:pos_end]
    return output_string


def xstr(s):
    if s is None:
        return ""
    else:
        return str(s)


def get_today_date():
    return datetime.date.today()


def get_today_datetime():
    return datetime.datetime.today()


class ConditionalMethodDecorator(object):
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)


def make_date_utc(input_date):
    output_date = pytz.timezone("UTC").localize(input_date, is_dst=None)
    return output_date
