from django.test import TestCase
from django.core.urlresolvers import resolve
from django.contrib.auth.views import login
from django.http import HttpRequest
from django.template.loader import render_to_string


class AuthenticationTest(TestCase):

    def test_log_url_resolves_to_login(self):
        found = resolve('/accounts/login/')
        self.assertEqual(found.func, login)

    def test_login_template_is_rendered(self):
        request = HttpRequest()
        response = login(request)
        expected_html = render_to_string('registration/login.html')
        self.assertEqual(response.content.decode(), expected_html)