# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException


def assert_when_element_does_not_exist(testcase, xpath):
    try:
        testcase.selenium.find_element_by_xpath(xpath)
    except NoSuchElementException:
        assert(xpath+" does not exist")


def assert_when_element_exists(testcase, xpath):
    try:
        testcase.selenium.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return
    assert(xpath+" does exist")