from subprocess import PIPE, Popen

import pytest
from django.test import TestCase

from koalixcrm.version import KOALIXCRM_VERSION


class VersionIncreaseTest(TestCase):
    @staticmethod
    def get_all_koalixcrm_version_from_pip():
        process_out = Popen(['pip', 'index', 'versions', 'koalix-crm'], stdout=PIPE, stderr=PIPE)
        output, _ = process_out.communicate()
        output_str = output.decode('utf-8')
        # Format: "koalix-crm (1.14.0)\nAvailable versions: 1.14.0, 1.13.0, ..."
        all_versions = []
        for line in output_str.splitlines():
            if line.startswith("Available versions:"):
                versions_str = line.split(":", 1)[1].strip()
                all_versions = [v.strip() for v in versions_str.split(",")]
                break
        return all_versions

    def setUp(self):
        self.available_versions = VersionIncreaseTest.get_all_koalixcrm_version_from_pip()

    @pytest.mark.version_increase
    def test_version_increase(self):
        self.assertNotIn(KOALIXCRM_VERSION, self.available_versions,
                         f"Version {KOALIXCRM_VERSION} already exists on PyPI")
