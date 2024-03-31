from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class UITests(StaticLiveServerTestCase):

    def setUp(self):
        firefox_options = webdriver.firefox.options.Options()
        firefox_options.add_argument("--headless")
        self.selenium = webdriver.Firefox(options=firefox_options)
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        if len(self._outcome.errors) > 0:
            test_method_name = self._testMethodName
            self.selenium.save_screenshot("test_results/Screenshots/%s.png" % test_method_name)
        self.selenium.quit()
