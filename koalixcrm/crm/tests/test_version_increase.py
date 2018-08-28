from django.test import TestCase
from koalixcrm.global_support_functions import get_string_between
from subprocess import Popen, PIPE
from koalixcrm.version import KOALIXCRM_VERSION
import pytest


class VersionIncreaseTest(TestCase):
    @staticmethod
    def get_all_koalixcrm_version_from_pip():
        process_out = Popen(['pip install koalix-crm=='], shell=True, stderr=PIPE)
        output, string_containing_all_version = process_out.communicate()
        all_koalixcrm_version_csv = get_string_between(string_containing_all_version.__str__(), "koalix-crm== (", ")")
        all_koalixcrm_version = all_koalixcrm_version_csv.split(", ")
        return all_koalixcrm_version

    def setUp(self):
        self.available_versions = VersionIncreaseTest.get_all_koalixcrm_version_from_pip()

    @pytest.mark.version_increase
    def test_version_increase(self):
        last_version = ""
        for version in self.available_versions:
            last_version = version
            if version == KOALIXCRM_VERSION:
                break
        self.assertNotEqual(last_version, KOALIXCRM_VERSION)

