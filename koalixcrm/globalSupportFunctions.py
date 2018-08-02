# -*- coding: utf-8 -*-


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
