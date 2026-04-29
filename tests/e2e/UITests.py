from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class UITests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.selenium = webdriver.Chrome(options=chrome_options)
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
