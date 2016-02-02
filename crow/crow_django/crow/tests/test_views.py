from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth import get_user_model
from django_webtest import WebTest

from crow.views import home_page
from crow.models import Layer


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


class LayerViewTest(TestCase):

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
