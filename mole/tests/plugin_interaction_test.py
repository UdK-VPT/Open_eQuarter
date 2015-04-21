import unittest
import os, sys, imp
from qgis import utils
from qgis.core import QgsVectorLayer, QgsField, QgsMapLayerRegistry, QGis
from PyQt4.QtCore import QVariant

from qgis_interface import set_up_interface
from mole.qgisinteraction import layer_interaction as li
from mole.qgisinteraction import plugin_interaction as pi


class PstPluginInteractionTest(unittest.TestCase):

    def create_layer_with_features(self, name, type='Polygon'):
        v_layer_name = li.biuniquify_layer_name(name)
        v_layer = QgsVectorLayer('{}?crs=EPSG:3857'.format(type), v_layer_name, 'memory', False)

        provider = v_layer.dataProvider()
        v_layer.startEditing()

        attributes = [QgsField('COLOR_RED', QVariant.String),
                      QgsField('COLOR_GRE', QVariant.String),
                      QgsField('COLOR_BLU', QVariant.String),
                      QgsField('COLOR_ALP', QVariant.String)]
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

    def tearDown(self):
        if self.qgis_app is not None:
            del(self.qgis_app)

    def test_if_plugin_is_available(self):
        self.assertNotEqual(utils.available_plugins, [], 'No plugins were loaded.')
        self.assertIn('pointsamplingtool', utils.available_plugins)

    def test_if_plugin_is_accessible(self):
        self.add_pointsamplingtool_to_plugins()
        psti = pi.PstInteraction(utils.iface)
        self.assertIsNotNone(psti)

    def test_if_layers_can_be_added(self):
        self.add_pointsamplingtool_to_plugins()

        layer = self.create_layer_with_features('layer', 'Point')
        registry = QgsMapLayerRegistry.instance()
        registry.addMapLayer(layer)

        psti = pi.PstInteraction(utils.iface)
        psti.set_input_layer(layer.name())
        self.assertNotEqual(psti.pst_dialog.inData.count(), 0, 'The layers attributes have not been added to the field table.')

    def test_if_all_fields_are_selected(self):
        self.add_pointsamplingtool_to_plugins()

        registry = QgsMapLayerRegistry.instance()
        point_layer = self.create_layer_with_features('point', 'Point')
        poly_layer1 = self.create_layer_with_features('poly1')
        poly_layer2 = self.create_layer_with_features('poly2')
        registry.addMapLayer(point_layer)
        registry.addMapLayer(poly_layer1)
        registry.addMapLayer(poly_layer2)

        psti = pi.PstInteraction(utils.iface)
        psti.set_input_layer(point_layer.name())
        selected_fields = psti.pst_dialog.fieldsTable
        psti.select_and_rename_files_for_sampling()
        fields_point = point_layer.dataProvider().fields()
        fields_poly1 = poly_layer1.dataProvider().fields()
        fields_poly2 = poly_layer2.dataProvider().fields()
        rows_expected = fields_point.count() + fields_poly1.count() + fields_poly2.count()
        self.assertEqual(selected_fields.rowCount(), rows_expected)

    def test_if_field_names_are_unique(self):
        self.add_pointsamplingtool_to_plugins()

        registry = QgsMapLayerRegistry.instance()
        point_layer = self.create_layer_with_features('test_pointlayer', 'Point')
        poly_layer = self.create_layer_with_features('test_polygonlayer')
        registry.addMapLayer(point_layer)
        registry.addMapLayer(poly_layer)

        psti = pi.PstInteraction(utils.iface)
        psti.set_input_layer(point_layer.name())
        map = psti.select_and_rename_files_for_sampling()

        appendix = ['R', 'G', 'B', 'a']
        point_fields = psti.pst_dialog.sampItems[point_layer.name()]
        poly_fields = psti.pst_dialog.polyItems[poly_layer.name()]

        for i in range(1, len(poly_fields)):
            self.assertEqual(point_fields[i][1], '01{}_{}'.format(point_layer.name()[:6], appendix[i-1]))
            self.assertEqual(poly_fields[i][1], '02{}_{}'.format(poly_layer.name()[:6], appendix[i-1]))

        self.assertEqual(map[point_layer.name()], '01{}'.format(point_layer.name()[:6]))
        self.assertEqual(map[poly_layer.name()], '02{}'.format(poly_layer.name()[:6]))




if __name__ == '__main__':
    unittest.main()

