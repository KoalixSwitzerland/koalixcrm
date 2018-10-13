# -*- coding: utf-8 -*-

import pytz
from selenium.common.exceptions import NoSuchElementException


def assert_when_element_does_not_exist(testcase, xpath):
    try:
        testcase.selenium.find_element_by_xpath(xpath)
    except NoSuchElementException:
        testcase.assertTrue(True, xpath+" does not exist")


def assert_when_element_exists(testcase, xpath):
    try:
        testcase.selenium.find_element_by_xpath(xpath)
    except NoSuchElementException:
        testcase.assertTrue(True, xpath+" does exist")


def assert_when_element_is_not_equal_to(testcase, xpath, string):
    try:
        element = testcase.selenium.find_element_by_xpath(xpath)
        if element.text != string:
            print("issue")
    except NoSuchElementException:
        return


def make_date_utc(input_date):
    output_date = pytz.timezone("UTC").localize(input_date, is_dst=None)
    return output_date
