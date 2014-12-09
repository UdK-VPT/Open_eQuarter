from unittest import TestCase
from qgis.gui import *
from qgis.core import QgsApplication, QgsProviderRegistry, QgsVectorLayer, QgsMapLayerRegistry
from PyQt4 import QtCore
import LayerInteraction


class LayerInteraction_test(TestCase):

    def setUp(self):
        QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
        QgsApplication.initQgis()

        if len(QgsProviderRegistry.instance().providerList()) == 0:
            raise RuntimeError('No data providers available.')

        QtCore.QCoreApplication.setOrganizationName('QGIS')
        QtCore.QCoreApplication.setApplicationName('QGIS2')

    def tearDown(self):
        QgsApplication.exitQgis

    def test_create_temporary_layer(self):

        layer_name = layer_type = ''
        self.assertIsNone(LayerInteraction.create_temporary_layer(layer_name,layer_type), 'An error occured when trying to create a layer with an invalid type')

        layer_name = layer_type = None
        self.assertIsNone(LayerInteraction.create_temporary_layer(layer_name,layer_type), 'An error occured when trying to create a layer with an invalid type')

        layer_name = 'MyLayer'
        layer_type = 'Shapefile'
        crs_name = ''
        layer = LayerInteraction.create_temporary_layer(layer_name,layer_type, crs_name)
        self.assertIsInstance(layer,QgsVectorLayer, 'An error occured when trying to create a layer')
        self.assertEqual(layer.name(),layer_name, 'An error occured when trying to create a layer: The layers name should be ' + layer_name)
        self.assertEqual(layer.type(),0, 'An error occured when trying to create a layer. The layer type should be 0 (VectorLayer).')
        self.assertEqual(layer.crs().toProj4(), '')

        crs_name = 'Ejkajwdiojkl'
        layer = LayerInteraction.create_temporary_layer(layer_name,layer_type, crs_name)
        self.assertIsInstance(layer,QgsVectorLayer, 'An error occured when trying to create a layer with an invalid crs.')
        self.assertEqual(layer.name(),layer_name)
        self.assertEqual(layer.type(),0)
        self.assertEqual(layer.crs().toProj4(), '')

    def test_add_layer_to_registry(self):
        layer_name = 'this_layer_was_added_for_testing_purpose'

        layer = QgsVectorLayer('Polygon?crs=EPSG:3857', layer_name, 'memory', False)

        number_of_layers = len(QgsMapLayerRegistry.instance().mapLayers())

        LayerInteraction.add_layer_to_registry(layer)

        map_layers = QgsMapLayerRegistry.instance().mapLayers()
        self.assertEqual(len(map_layers), number_of_layers + 1, 'An error occured when adding a layer to the MapLayerRegistry.')

        layer_added = False
        for layer_key in map_layers:

            if map_layers[layer_key].name() == layer_name:
                layer_added = True
                break

        self.assertTrue(layer_added, 'An error occured when adding a layer to the MapLayerRegistry.')

        number_of_layers = len(map_layers)

        LayerInteraction.add_layer_to_registry(None)

        self.assertEqual(len(QgsMapLayerRegistry.instance().mapLayers()), number_of_layers, 'An error occured when trying to add a none-type-layer to the MapLayerRegistry. The number of layers should not increase.')

    def test_find_layer_by_name(self):

        reg = QgsMapLayerRegistry.instance()
        v1_name = 'layer1'
        v2_name = 'layer2'
        v3_name = 'layer3'
        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', v1_name, 'memory', False))
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v2_name, 'memory', False))
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v3_name, 'memory', False))

        layer = LayerInteraction.find_layer_by_name(None)
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing a none-type name.')

        layer = LayerInteraction.find_layer_by_name('')
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing an empty name.')

        layer = LayerInteraction.find_layer_by_name('awdalwd')
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing a non-existing name.')

        layer1 = LayerInteraction.find_layer_by_name(v1_name)
        layer2 = LayerInteraction.find_layer_by_name(v2_name)
        layer3 = LayerInteraction.find_layer_by_name(v3_name)

        layer1_exists = layer2_exists = layer3_exists = False
        for layer_key in reg.mapLayers():
            layer_value = reg.mapLayers()[layer_key]

            if layer_value == layer1:
                layer1_exists = True
            elif layer_value == layer2:
                layer2_exists = True
            elif layer_value == layer3:
                layer3_exists = True

        self.assertTrue(layer1_exists, 'An error occured when trying to find the previously added layer ' + layer1.name() + '.')
        self.assertTrue(layer2_exists, 'An error occured when trying to find the previously added layer ' + layer2.name() + '.')
        self.assertTrue(layer3_exists, 'An error occured when trying to find the previously added layer ' + layer3.name() + '.')


