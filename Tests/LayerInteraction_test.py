from unittest import TestCase
from qgis.core import QgsApplication, QgsProviderRegistry, QgsVectorLayer, QgsMapLayerRegistry
from os import path, remove, walk
from PyQt4 import QtCore
from .. import LayerInteraction
from QgisTestInterface import QgisTestInterface
from copy import deepcopy


class LayerInteraction_test(TestCase):

    def __init__(self, testName, iface = QgisTestInterface()):
        super(LayerInteraction_test, self).__init__(testName)
        self.iface = iface
        self.layer_list = []

    def setUp(self):
        QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
        QgsApplication.initQgis()

        if len(QgsProviderRegistry.instance().providerList()) == 0:
            raise RuntimeError('No data providers available.')

        self.layer_list = []

        QtCore.QCoreApplication.setOrganizationName('QGIS')
        QtCore.QCoreApplication.setApplicationName('QGIS2')

    def tearDown(self):
        for layer_name in self.layer_list:
            layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)
            if( len(layer) == 1):
                QgsMapLayerRegistry.instance().removeMapLayer(layer[0].id())
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
        self.layer_list.append(layer.name())

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
        self.layer_list.append(v1_name)
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v2_name, 'memory', False))
        self.layer_list.append(v2_name)
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v3_name, 'memory', False))
        self.layer_list.append(v3_name)

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

    def test_hide_or_remove_layer(self):

        iface = self.iface

        reg = QgsMapLayerRegistry.instance()
        v1_name = 'layer1'

        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', v1_name, 'memory', False))
        self.layer_list.append(v1_name)
        self.assertEqual(reg.mapLayersByName(v1_name)[0].name(), v1_name, 'Layer was not added.')

        LayerInteraction.hide_or_remove_layer(v1_name, 'hide', iface)
        self.assertFalse(iface.legendInterface().isLayerVisible(LayerInteraction.find_layer_by_name(v1_name)))

        LayerInteraction.hide_or_remove_layer(v1_name, 'remove')
        self.assertEqual(reg.mapLayersByName(v1_name), [], 'Layer was not removed.')

    def test_write_vector_layer_to_disk(self):

        v_layer_name = 'MyWriteTestLayer'
        v_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', v_layer_name, 'memory', False)

        test_path = path.join('/', 'Users', 'VPTtutor', 'Desktop', v_layer_name)


        if path.exists(test_path + '.shp'):
            appendix = 0
            temp_path = test_path
            while path.exists(temp_path + '.shp'):
                appendix += 1
                temp_path = test_path + str(appendix)

            test_path = temp_path
            v_layer_name += str(appendix)

        invalid_path = path.join(test_path, 'InvalidPath')

        return_layer = LayerInteraction.write_vector_layer_to_disk(v_layer, invalid_path)
        self.assertIsNone(return_layer)

        return_layer = LayerInteraction.write_vector_layer_to_disk(None, invalid_path)
        self.assertIsNone(return_layer)

        return_layer = LayerInteraction.write_vector_layer_to_disk(v_layer, test_path)
        self.assertIsNotNone(return_layer)
        self.assertEqual(return_layer.name(), v_layer_name)
        self.assertTrue(path.exists(test_path + '.shp'))

        return_layer = LayerInteraction.write_vector_layer_to_disk(v_layer, test_path + '.shp')
        self.assertIsNotNone(return_layer)
        self.assertEqual(return_layer.name(), v_layer_name + '1')
        self.assertTrue(path.exists(test_path + '1.shp'))


        test_dir = path.dirname(test_path)
        for subdir, dirs, files in walk(test_dir):
            for file in files:
                if file.startswith(v_layer_name) or file.startswith(v_layer_name + '1'):
                    remove(path.join(test_dir, file))

    def test_add_style_to_layer(self):
        pass

    def test_trigger_edit_mode(self):
        iface = self.iface

        reg = QgsMapLayerRegistry.instance()
        edit_layer = 'MylayerForEditing'
        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', edit_layer, 'memory', False))
        self.layer_list.append(edit_layer)

        editing_triggered = [False]
        iface.actionToggleEditing().triggered.connect(lambda who: self.checkSender(who, editing_triggered))
        LayerInteraction.trigger_edit_mode(self.iface, edit_layer)

        self.assertTrue(editing_triggered[1])

        LayerInteraction.trigger_edit_mode(self.iface, edit_layer, 'off')
        self.assertFalse(editing_triggered[2])


    def checkSender(self, sender, edit_list):
        edit_list.append(sender)




