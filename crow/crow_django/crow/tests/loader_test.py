from unittest import TestCase
import os

class LoaderTest(TestCase):

    def setUp(self):
        self.loader = JsonLoader()
        file_location = os.path.abspath(os.path.normpath('Raabestr_Berlin.geojson'))
        self.loader.load(file_location)


    def test_if_json_file_has_three_keys(self):
        data = self.loader.data
        self.assertEqual(len(data.keys()), 3, 'Expected the data-dictionary to have three keys in it but found {}.'.format(data.keys()))
        expected_keys = ['crs', 'type', 'features']
        for key in expected_keys:
            self.assertIn(key, data.keys())

    def test_if_loader_finds_a_list_of_features(self):
        data = self.loader.data
        features = data['features']
        self.assertTrue(issubclass(features, list))


class JsonLoader():

    def __init__(self):
        self.data = {}

    def load(self, file):
        self.data = {'crs' : '', 'type': '', 'features': ''}