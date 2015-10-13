from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS('phantomjs')

    def tearDown(self):
        self.browser.quit()

    def test_can_view_an_open_layers_map(self):
        # The GIS community has heard of a new tool to analyse a quarter.
        # Mr. G. opens his webbrowser and opens the url.
        self.browser.get('http://localhost:8000')

        # He expects the title of the tool to be in the browser
        self.assertIn('Open eQuarter - Crow', self.browser.title)

        # A header navigation-bar is displayed, which shows the clickable companies logo as a first entry
        navigation_bar = self.browser.find_element_by_tag_name('nav')
        logo_link = navigation_bar.find_element_by_tag_name('a')
        logo = logo_link.find_element_by_tag_name('img')
        self.assertTrue(logo.get_attribute('src'))

        self.fail('Finish the test')
if __name__ == '__main__':
    unittest.main()
