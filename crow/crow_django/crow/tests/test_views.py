from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
from django_webtest import WebTest

from crow.views import home_page
from crow.models import Layer
from crow.forms import EMPTY_COMMENT_ERROR


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


class LayerViewTest(WebTest):

    def setUp(self):
        self.layer = Layer()
        self.layer.name = 'Test layer'
        self.layer.save()
        User = get_user_model()
        self.user = User.objects.create_user(username='Commenter', password='Test')

    def test_basic_view(self):
        response = self.client.get(self.layer.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_name_in_layer(self):
        response = self.client.get(self.layer.get_absolute_url())
        self.assertContains(response, self.layer.name)

    def test_view_page(self):
        page = self.app.get(self.layer.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

    def test_form_error(self):
        page = self.app.get(self.layer.get_absolute_url())
        redirect = page.form.submit()
        self.assertContains(redirect, EMPTY_COMMENT_ERROR)

    def test_form_success(self):
        page = self.app.get(self.layer.get_absolute_url(), user=self.user)
        page.form['text'] = 'This is a comment'
        redirect = page.form.submit()
        self.assertRedirects(redirect, self.layer.get_absolute_url())
