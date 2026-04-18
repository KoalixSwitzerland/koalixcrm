from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class UITests(StaticLiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.add_argument("--headless")
        self.selenium = webdriver.Firefox(options=firefox_options)
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        # Python 3.11 removed `_outcome.errors`; inspect the current test
        # result instead (when available) to decide whether to capture a
        # screenshot on failure.
        errors = getattr(self._outcome, 'errors', None)
        if errors is None:
            result = getattr(self._outcome, 'result', None)
            if result is not None:
                errors = (
                    getattr(result, 'errors', [])
                    + getattr(result, 'failures', [])
                )
            else:
                errors = []
        if len(errors) > 0:
            test_method_name = self._testMethodName
            self.selenium.save_screenshot("test_results/Screenshots/%s.png" % test_method_name)
        self.selenium.quit()
