from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

    def test_can_register_a_user_and_create_a_project(self):
		# Leo Graphy has already used the QGIS-mole plugin to quickly analyse a quarter in Berlin.
        # He now heard, there is a webservice which enables him to transfer his results to a website and to watch his layers from everywhere in the world.
        # He opens his browser and navigates to the website.
        self.browser.get(self.live_server_url)

        # The service is only available to registerd users, therefore a login-form is displayed
        self.assertIn('Open eQuarter - Crow - Login', self.browser.title)
        #TODO check for form

        # He does not have an account, so he clicks the "Sign up" button to create one

        # He notices that, though the page did not refresh, a "Sign up" form became visible

        # He selects a username, which is still availble, enters his e-mail, a password and a confirmation and submits the form

        # Again, without refreshing, the page confirms his registration and kindly asks him to confirm his registration by following a link which was sent to his email address

        # He clicks the link and - now correctly registered - gets forwarded to the actual web-service

        # The website shows a menu-bar with a project-dropdown, a search-field and his username

        # Since he just registered to the site, there are no projects waiting for him yet.
        # The dropdown only shows the option to create a new project - which he does.

        # Now a form overlays the screen, which invites him to create a project.

        # He fills in a name and has the option to input a default location and a collaborators username or email-address.
        # But since he just want to gain a first impression, he leaves it with the project-name and clicks the create button.

        # The former project-dropdown now shows the name of the recently created project.

        # An additional site-bar appears, with a list of available layers. So far the list is empty, but a nice '+'-button clearly invites him to add a new layer to the project.

        # Since he does not know what layer to add, he logs out for a short break and to prepare the first layer to upload.
