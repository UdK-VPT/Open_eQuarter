from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # Headless test using phantomjs driver
        self.browser = webdriver.PhantomJS('phantomjs')

        # The browsers window-size is set to a desktop resolution
        self.browser.set_window_size(1024, 768)

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

        # A dropdown menu is visible in the navigation bar, where Mr. G can chose a project
        dropdown = navigation_bar.find_element_by_class_name('dropdown')
        dropdown_link = dropdown.find_element_by_tag_name('a')
        self.assertIn('Choose project', dropdown_link.text,
                      'Choose project - dropdown not found, found {} instead.'.format(dropdown_link.text))

        # Another link is found, which enables the user to load a layer
        navigation_ul = navigation_bar.find_element_by_css_selector('ul:first-child')
        open_button_link = navigation_ul.find_element_by_class_name('btn-file')
        self.assertIn('Open layer', open_button_link.text,
                      'Open layer - button not found, found {} instead'.format(open_button_link.text))

        self.fail('Finish the test')


if __name__ == '__main__':
    unittest.main()
