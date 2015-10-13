from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_view_an_open_layers_map(self):
        # The GIS community has heard of a new tool to analyse a quarter.
        # Mr. G. opens his webbrowser and opens the url.
        self.browser.get('http://localhost:8000')

        # He expects the title of the tool to be in the browser
        self.assertIn('Open eQuarter - Crow', self.browser.title)
        self.fail('Finish the test')

        # A header navigation is displayed, which shows the companies logo

if __name__ == '__main__':
    unittest.main()
