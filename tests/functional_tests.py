from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # used Chrome webdriver from http://chromedriver.storage.googleapis.com/index.html?path=2.27/
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_search_for_yamaha_and_get_results(self):
        self.browser.get('http://localhost:8000')

        assert 'FindMyWheels' in self.browser.title


if __name__ == '__main__':
    unittest.main()


