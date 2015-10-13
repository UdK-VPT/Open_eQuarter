from django.core.urlresolvers import resolve
from django.test import TestCase
from layertree.views import layer_tree


class TreeRootTest(TestCase):

    def test_root_url_resolves_to_layer_tree(self):
        found = resolve('layers')
        self.assertEqual(found.func, layer_tree)
