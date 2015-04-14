import unittest, os
from qgis import utils

from qgis_interface import set_up_interface


class PstPluginInteractionTest(unittest.TestCase):

    def setUp(self):
        self.qgis_app, self.canvas, self.iface = set_up_interface()
        utils.plugin_paths = [os.path.expanduser('~/.qgis2/python/plugins')]
        utils.updateAvailablePlugins()
        utils.loadPlugin('pointsamplingtool')
        utils.iface = self.iface
        utils.startPlugin('pointsamplingtool')

    def test_if_plugin_is_available(self):
        self.assertNotEqual(utils.available_plugins, [], 'No plugins were loaded.')
        self.assertIn('pointsamplingtool', utils.available_plugins)

    def test_if_plugin_is_accessible(self):
        self.fail('Access point sampling tool')

if __name__ == '__main__':
    unittest.main()
