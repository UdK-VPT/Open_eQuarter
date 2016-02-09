from selenium import webdriver
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # self.browser = webdriver.Firefox()
        # Headless test using phantomjs driver
        self.browser = webdriver.PhantomJS('phantomjs')
        self.browser.implicitly_wait(3)

        # The browsers window-size is set to a desktop resolution
        self.browser.set_window_size(1024, 768)

    def tearDown(self):
        self.browser.quit()

    def test_can_register_a_new_user(self):
        # The GIS community has heard of a new tool to analyse a quarter.
        # Mr. Leo Graphy opens his webbrowser and opens the url.
        self.browser.get(self.live_server_url)

        # He expects to find a page where he can logins
        self.assertIn('Open eQuarter - Login', self.browser.title)

        # A login form is available to enter his username and password
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')

        self.assertEqual(login_username.get_attribute('placeholder'), 'Username')
        self.assertEqual(login_password.get_attribute('placeholder'), 'Password')


        # a link is found, which leads those users who do not have an account yet to a page, where they can register
        register_link = self.browser.find_element_by_partial_link_text('egister')
        self.assertIsNotNone(register_link)

        # Leo does not have an account and therefore has to create one first
        register_link.click()

        # Again a form is displayed, which allows a new user to create an account
        reg_username = self.browser.find_element_by_id('id_username')
        reg_email = self.browser.find_element_by_id('id_email')
        reg_password1 = self.browser.find_element_by_id('id_password1')
        reg_password2 = self.browser.find_element_by_id('id_password2')

        self.assertEqual(reg_username.get_attribute('placeholder'), 'Username')
        self.assertEqual(reg_email.get_attribute('placeholder'), 'Email')
        self.assertEqual(reg_password1.get_attribute('placeholder'), 'Password')
        self.assertEqual(reg_password2.get_attribute('placeholder'), 'Password confirmation')

        # Desperate to use the platform, he decides on a username and a password and creates an account
        reg_username.send_keys('LeoGraphy')
        reg_email.send_keys('leo.graphy@ema.il')
        reg_password1.send_keys('LeosPW1234')
        reg_password2.send_keys('LeosPW1234')

        buttons = self.browser.find_elements_by_tag_name('button')
        reg_button = list(filter(lambda button: button.get_attribute('type') == 'submit', buttons))[0]
        reg_button.click()

        # The user is forwarded to a page, which confirms the registration
        self.assertIn('Open eQuarter - Success!', self.browser.title)


class RegisteredUserTest(StaticLiveServerTestCase):

    fixtures = [
        'fixtures/crow_django.json',
    ]

    def setUp(self):
        # self.browser = webdriver.Firefox()
        # Headless test using phantomjs driver
        self.browser = webdriver.PhantomJS('phantomjs')
        self.browser.implicitly_wait(3)

        # The browsers window-size is set to a desktop resolution
        self.browser.set_window_size(1024, 768)

    def tearDown(self):
        self.browser.quit()

    def test_can_login_a_registerd_user(self):

        # The GIS community has heard of a new tool to analyse a quarter.
        # Mr. Leo Graphy just registered as a new user and activated his account already
        # He opens his browser again and navigates back to the website
        self.browser.get(self.live_server_url)
        self.assertIn('Open eQuarter - Login', self.browser.title)

        # The login form is still available to enter his username and password
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')

        login_username.send_keys('LeoGraphy')
        login_password.send_keys('LeoPW1234')

        buttons = self.browser.find_elements_by_tag_name('button')
        login_btn = list(filter(lambda button: button.get_attribute('value') == 'login', buttons))[0]
        login_btn.click()

        # Leo has a typo in his password and sees an error message
        error_box = self.browser.find_element_by_class_name('alert-danger')
        self.assertIn('Please enter a correct username and password. Note that both fields may be case-sensitive.', error_box.text)


        # The username is still displayed
        # He corrects his typo and finally logs himself in to the new website
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')

        login_username.clear()
        login_username.send_keys('LeoGraphy')
        login_password.send_keys('LeosPW1234')

        buttons = self.browser.find_elements_by_tag_name('button')
        login_btn = list(filter(lambda button: button.get_attribute('value') == 'login', buttons))[0]
        login_btn.click()

        # His login was successful, hence his username is visible in the browsers title
        self.assertIn('Open eQuarter - LeoGraphy', self.browser.title)

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
        self.assertIn('Load layer', open_button_link.text,
                      'Load layer - button not found, found {} instead'.format(open_button_link.text))

        # A first layer is already loaded and displayed in the layer-stack
        layer = self.browser.find_element_by_partial_link_text('Heinrich')
        self.assertIsNotNone(layer)

        # A dropdown-menu is displayed, having his user-name as title
        lis = navigation_bar.find_elements_by_tag_name('li')
        dropdowns = list(filter(lambda li: li.get_attribute('class') == 'dropdown', lis))
        self.assertIn('LeoGraphy', dropdowns[-1].text)

        # Once the dropdown is clicked, a logout button becomes visible
        dropdown_lnk = self.browser.find_element_by_xpath('//*[@id="main-navbar"]/ul[2]/li[2]/a')
        logout_btn = dropdown_lnk.click()
        logout_btn = self.browser.find_element_by_xpath('//*[@id="main-navbar"]/ul[2]/li[2]/ul/li[4]/a')
        self.assertTrue(logout_btn.is_displayed())
        self.assertIn('Logout', logout_btn.text)

        # Leo had a nice first impression, he logs out and closes his browser to tell his colleagues about the site.
        logout_btn.click()
        goodbye = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Goodbye.', goodbye.text)
