import unittest
import os, sys, imp
from qgis import utils
from qgis.core import QgsVectorLayer, QgsField, QgsMapLayerRegistry
from PyQt4.QtCore import QVariant

from qgis_interface import set_up_interface
from mole.qgisinteraction import layer_interaction as li
from mole.qgisinteraction import plugin_interaction as pi


class PstPluginInteractionTest(unittest.TestCase):

    def create_layer_with_features(self, name):
        v_layer_name = li.biuniquify_layer_name(name)
        v_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', v_layer_name, 'memory', False)

        provider = v_layer.dataProvider()
        v_layer.startEditing()

        attributes = [QgsField('AREA', QVariant.Double),
                      QgsField('PERIMETER', QVariant.Double),
                      QgsField('BLD_ID', QVariant.String)]
        provider.addAttributes(attributes)
        v_layer.commitChanges()
        return v_layer

    def add_pointsamplingtool_to_plugins(self):
        plugin_folder = os.path.join(utils.plugin_paths[0], 'pointsamplingtool', '__init__.py')
        self.assertTrue(os.path.exists(str(plugin_folder)), 'Path to plugin not found. ({})'.format(str(plugin_folder)))
        sys.modules['pointsamplingtool'] = imp.load_source('pointsamplingtool', plugin_folder)

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
        self.add_pointsamplingtool_to_plugins()
        psti = pi.PstInteraction(utils.iface)
        self.assertIsNotNone(psti)

    def test_if_layers_can_be_added(self):
        layer1 = self.create_layer_with_features('layer1')
        layer2 = self.create_layer_with_features('layer2')
        registry = QgsMapLayerRegistry.instance()
        registry.addMapLayer(layer1)
        registry.addMapLayer(layer2)
        self.add_pointsamplingtool_to_plugins()
        psti = pi.PstInteraction(utils.iface)
        psti.set_input_layer(layer1.name())
        self.assertNotEqual(psti.pst_dialog.fieldsTable.rowCount(), 0, 'The layers attributes have not been added to the field table.')

if __name__ == '__main__':
    unittest.main()
