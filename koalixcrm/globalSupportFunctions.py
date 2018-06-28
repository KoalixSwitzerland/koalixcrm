# -*- coding: utf-8 -*-


def limit_string_length(input_string, maximum_length):
    if len(input_string) > maximum_length:
        output_string = input_string[:maximum_length]
    else:
        output_string = input_string
    return output_string


def xstr(s):
    if s is None:
        return ""
    else:
        return str(s)
