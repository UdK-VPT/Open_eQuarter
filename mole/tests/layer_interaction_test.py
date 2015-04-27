from os import path, remove, walk
import unittest

from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsField, QgsFeature
from qgis.utils import iface
from PyQt4.QtCore import QVariant
from mole.qgisinteraction import layer_interaction
from qgis_interface import set_up_interface

class LayerInteraction_test(unittest.TestCase):

    def setUp(self):
        if iface is None:
            self.qgis_app, self.canvas, self.iface = set_up_interface()
        else:
            self.iface = iface

        self.layer_list = []
        self.valid_wms_url = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'

    def tearDown(self):
        for layer_name in self.layer_list:
            layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)
            if( len(layer) == 1):
                QgsMapLayerRegistry.instance().removeMapLayer(layer[0].id())

        if iface is None:
            del(self.qgis_app)
        
    def test_create_temporary_layer(self):

        layer_name = layer_type = ''
        self.assertIsNone(layer_interaction.create_temporary_layer(layer_name,layer_type), 'An error occured when trying to create a layer with an invalid type')

        layer_name = layer_type = None
        self.assertIsNone(layer_interaction.create_temporary_layer(layer_name,layer_type), 'An error occured when trying to create a layer with an invalid type')

        layer_name = layer_interaction.biuniquify_layer_name('MyLayer')
        layer_type = 'Shapefile'
        crs_name = ''
        layer = layer_interaction.create_temporary_layer(layer_name,layer_type, crs_name)
        self.assertIsInstance(layer,QgsVectorLayer, 'An error occured when trying to create a layer')
        self.assertEqual(layer.name(),layer_name, 'An error occured when trying to create a layer: The layers name should be ' + layer_name)
        self.assertEqual(layer.type(),0, 'An error occured when trying to create a layer. The layer type should be 0 (VectorLayer).')
        self.assertEqual(layer.crs().toProj4(), '')

        crs_name = 'Ejkajwdiojkl'
        layer = layer_interaction.create_temporary_layer(layer_name,layer_type, crs_name)
        self.assertIsInstance(layer,QgsVectorLayer, 'An error occured when trying to create a layer with an invalid crs.')
        self.assertEqual(layer.name(),layer_name)
        self.assertEqual(layer.type(),0)
        self.assertEqual(layer.crs().toProj4(), '')

    def test_add_layer_to_registry(self):
        layer_name = layer_interaction.biuniquify_layer_name('this_layer_was_added_for_testing_purpose')

        layer = QgsVectorLayer('Polygon?crs=EPSG:3857', layer_name, 'memory', False)

        number_of_layers = len(QgsMapLayerRegistry.instance().mapLayers())
        layer_interaction.add_layer_to_registry(layer)
        self.layer_list.append(layer.name())

        map_layers = QgsMapLayerRegistry.instance().mapLayers()
        actual = len(map_layers)
        expected = number_of_layers + 1
        message = 'An error occured when adding a layer to the MapLayerRegistry. {} is not {}!'.format(actual, expected)
        self.assertEqual(actual, expected, message)

        layer_added = False
        for layer_key in map_layers:

            if map_layers[layer_key].name() == layer_name:
                layer_added = True
                break

        self.assertTrue(layer_added, 'An error occured when adding a layer to the MapLayerRegistry.')
        number_of_layers = len(map_layers)
        layer_interaction.add_layer_to_registry(None)
        self.assertEqual(len(QgsMapLayerRegistry.instance().mapLayers()), number_of_layers, 'An error occured when trying to add a none-type-layer to the MapLayerRegistry. The number of layers should not increase.')

    def test_find_layer_by_name(self):

        reg = QgsMapLayerRegistry.instance()

        v1_name = layer_interaction.biuniquify_layer_name('layer1')
        v2_name = layer_interaction.biuniquify_layer_name('layer2')
        v3_name = layer_interaction.biuniquify_layer_name('layer3')
        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', v1_name, 'memory', False))
        self.layer_list.append(v1_name)
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v2_name, 'memory', False))
        self.layer_list.append(v2_name)
        reg.addMapLayer(QgsVectorLayer('Point?crs=EPSG:3857', v3_name, 'memory', False))
        self.layer_list.append(v3_name)

        layer = layer_interaction.find_layer_by_name(None)
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing a none-type name.')

        layer = layer_interaction.find_layer_by_name('')
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing an empty name.')

        layer = layer_interaction.find_layer_by_name('awdalwd')
        self.assertIsNone(layer, 'An error occured when trying to find a layer passing a non-existing name.')

        layer1 = layer_interaction.find_layer_by_name(v1_name)
        layer2 = layer_interaction.find_layer_by_name(v2_name)
        layer3 = layer_interaction.find_layer_by_name(v3_name)

        layer1_exists = layer2_exists = layer3_exists = False

        for key, layer_value in reg.mapLayers().iteritems():
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
        v1_name = layer_interaction.biuniquify_layer_name('layer1')

        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', v1_name, 'memory', False))
        self.layer_list.append(v1_name)
        self.assertEqual(reg.mapLayersByName(v1_name)[0].name(), v1_name, 'Layer was not added.')

        layer_interaction.hide_or_remove_layer(v1_name, 'hide', iface)
        self.assertFalse(iface.legendInterface().isLayerVisible(layer_interaction.find_layer_by_name(v1_name)))

        layer_interaction.hide_or_remove_layer(v1_name, 'remove')
        self.assertEqual(reg.mapLayersByName(v1_name), [], 'Layer was not removed.')

    def test_write_vector_layer_to_disk(self):

        v_layer_name = layer_interaction.biuniquify_layer_name('MyWriteTestLayer')
        v_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', v_layer_name, 'memory', False)

        test_path = path.join('./', v_layer_name)

        if path.exists(test_path + '.shp'):
            appendix = 0
            temp_path = test_path
            while path.exists(temp_path + '.shp'):
                appendix += 1
                temp_path = test_path + str(appendix)

            test_path = temp_path
            v_layer_name += str(appendix)

        invalid_path = path.join(test_path, 'InvalidPath')

        return_layer = layer_interaction.write_vector_layer_to_disk(v_layer, invalid_path)
        self.assertIsNone(return_layer)
        return_layer = layer_interaction.write_vector_layer_to_disk(None, invalid_path)
        self.assertIsNone(return_layer)

        return_layer = layer_interaction.write_vector_layer_to_disk(v_layer, test_path)
        self.assertIsNotNone(return_layer)
        self.assertEqual(return_layer.name(), v_layer_name)
        self.assertTrue(path.exists(test_path + '.shp'))

        return_layer = layer_interaction.write_vector_layer_to_disk(v_layer, test_path + '.shp')
        self.assertIsNotNone(return_layer)
        self.assertEqual(return_layer.name(), v_layer_name + '1')
        self.assertTrue(path.exists(test_path + '1.shp'))

        test_dir = path.dirname(test_path)
        for subdir, dirs, files in walk(test_dir):
            for file in files:
                if file.startswith(v_layer_name) or file.startswith(v_layer_name + '1'):
                    try:
                        remove(path.join(test_dir, file))
                    except:
                        print('\tTest layer could not be deleted.')

    def test_add_style_to_layer(self):
        pass

    def test_trigger_edit_mode(self):
        iface = self.iface

        reg = QgsMapLayerRegistry.instance()
        edit_layer_name = layer_interaction.biuniquify_layer_name('MylayerForEditing')
        edit_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', edit_layer_name, 'memory', False)
        reg.addMapLayer(edit_layer)
        self.layer_list.append(edit_layer_name)

        layer_interaction.trigger_edit_mode(self.iface, edit_layer_name)

        self.assertTrue(edit_layer.isEditable())

        layer_interaction.trigger_edit_mode(self.iface, edit_layer_name, 'off')
        self.assertFalse(edit_layer.isEditable())

    def test_get_wms_layer_list(self):
        wms_url_with_parameters = self.valid_wms_url
        # use this list for proper testing...
        visibility = [True, False, True, True, True, False]
        # when debugging, use the list below instead
        # visibility = [True]


        for i, visible in enumerate(visibility):
            layer_name = layer_interaction.biuniquify_layer_name('r{}_visible:{}'.format(i, visible))
            rlayer = QgsRasterLayer(wms_url_with_parameters, layer_name, 'wms')
            self.assertTrue(rlayer.isValid(), layer_name.join(' is not a valid raster layer'))
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            self.iface.legendInterface().setLayerVisible(rlayer, visible)
            self.layer_list.append(layer_name)

        # get a list of all visible wms layers
        expected_layers = {}
        actual_layers = {}
        visible_raster_layers = layer_interaction.get_wms_layer_list(self.iface, 'visible')
        for i, visible in enumerate(visibility):
            if visible:
                expected_layers[self.layer_list[i]] = True

        for layer in visible_raster_layers:
            if '_visible:' in layer.name():
                actual_layers[str(layer.name())] = True

        self.assertDictEqual(expected_layers, actual_layers, 'The returned layers do not match the expected layers.\n\t Expected: {0}\n\t received: {1}.'.format(expected_layers, actual_layers))

        # get a list of all invisible wms layers
        expected_layers = {}
        actual_layers = {}
        invisible_raster_layers = layer_interaction.get_wms_layer_list(self.iface, 'invisible')
        for i, visible in enumerate(visibility):
            if not visible:
                expected_layers[self.layer_list[i]] = False

        for layer in invisible_raster_layers:
            if '_visible:' in layer.name():
                actual_layers[str(layer.name())] = True if layer.name().endswith('True') else False

        self.assertDictEqual(expected_layers, actual_layers, 'The returned layers do not match the expected layers.\n\t Expected: {0}\n\t received: {1}.'.format(expected_layers, actual_layers))

        # get a list of wms layers
        expected_layers = {}
        actual_layers = {}
        invisible_raster_layers = layer_interaction.get_wms_layer_list(self.iface, 'all')
        for i, visible in enumerate(visibility):
            expected_layers[self.layer_list[i]] = visible

        for layer in invisible_raster_layers:
            if '_visible:' in layer.name():
                actual_layers[str(layer.name())] = True if layer.name().endswith('True') else False

        self.assertDictEqual(expected_layers, actual_layers, 'The returned layers do not match the expected layers.\n\t Expected: {0}\n\t received: {1}.'.format(expected_layers, actual_layers))

    def test_open_wms_as_raster(self):

        valid_url = self.valid_wms_url
        invalid_url = valid_url[7:46]
        layer_name = 'Test_opening_a_raster_layer_from_wms_url'
        returned_layer = None

        returned_layer = layer_interaction.open_wms_as_raster(self.iface, invalid_url, layer_name)
        self.assertIsNone(returned_layer)

        returned_layer = layer_interaction.open_wms_as_raster(self.iface, valid_url, layer_name)
        self.assertIsNotNone(returned_layer, 'Tried to open a layer with the url {} failed, but should have passed.'.format(valid_url))
        self.assertTrue(returned_layer.isValid())
        self.assertEqual(layer_name, returned_layer.name())

    def test_zoom_to_layer(self):
        zoom_layer_name = layer_interaction.biuniquify_layer_name('Test_zoom_to_layer')
        zoom_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', zoom_layer_name, 'memory', False)
        inactive_layer_name = layer_interaction.biuniquify_layer_name('Layer_to_be_activated_and_deactivated_again')
        inactive_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', inactive_layer_name, 'memory', False)

        self.layer_list.extend([zoom_layer_name, inactive_layer_name])

        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(zoom_layer)
        reg.addMapLayer(inactive_layer)

        self.iface.setActiveLayer(inactive_layer)
        self.assertEqual(inactive_layer, self.iface.activeLayer(), 'The layer \"{}\" has not been activated'.format(inactive_layer_name))
        # if the given zoom_layer was set active, it has been found and used as the basis for the zoom
        # in that case, the formerly activated layer has to be inactive now!
        layer_interaction.zoom_to_layer(self.iface, zoom_layer_name)
        self.assertEqual(zoom_layer, self.iface.activeLayer())
        self.assertNotEqual(inactive_layer, self.iface.activeLayer())

    def test_biuniquify_layer_name(self):
        layer1_name = 'asdhhkhlu18927309hgdkaghdzuz7817982_unique'
        layer2_name = 'asdhhkhlu18927309hgdkaghdzuz781712ziadgwz_unique'
        layer3_name = ''

        self.assertIsNone(layer_interaction.find_layer_by_name(layer1_name), 'Default layer name (\"{}\") is not unique!'.format(layer1_name))
        self.assertIsNone(layer_interaction.find_layer_by_name(layer2_name), 'Default layer name (\"{}\") is not unique!'.format(layer2_name))

        layer1 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer1_name, 'memory', False)
        layer2 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer2_name, 'memory', False)

        self.layer_list.extend([layer1_name, layer2_name])

        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(layer1)
        reg.addMapLayer(layer2)

        self.assertEqual('', layer_interaction.biuniquify_layer_name(''))
        self.assertEqual('', layer_interaction.biuniquify_layer_name(None))

        # create a new unique name and add a layer with that name, to check the correctness of the functions while loop
        layer3_name = layer_interaction.biuniquify_layer_name(layer1_name)
        self.assertEqual(layer1_name + '0', layer3_name)

        layer3 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer3_name, 'memory', False)
        reg.addMapLayer(layer3)
        self.layer_list.extend([layer3_name])

        self.assertEqual(layer1_name +'1', layer_interaction.biuniquify_layer_name(layer1_name))
        self.assertEqual(layer1_name +'2', layer_interaction.biuniquify_layer_name(layer1_name + str(2)))
        self.assertEqual(layer2_name +'0', layer_interaction.biuniquify_layer_name(layer2_name))

    # ToDo
    def test_gdal_warp_layer_list(self):
        pass

    def test_if_parameter_info_is_added_to_a_layer(self):
        # create a temporary layer
        v_layer_name = layer_interaction.biuniquify_layer_name('my_test_layer')
        v_layer = QgsVectorLayer('Point?crs=EPSG:3857', v_layer_name, 'memory', False)

        provider = v_layer.dataProvider()
        v_layer.startEditing()

        attributes = [QgsField('00Test_no_R', QVariant.Double),
                      QgsField('00Test_no_G', QVariant.Double),
                      QgsField('00Test_no_B', QVariant.Double),
                      QgsField('00Test_no_a', QVariant.Double),
                      QgsField('01Testyl_R', QVariant.Double),
                      QgsField('01Testyl_G', QVariant.Double),
                      QgsField('01Testyl_B', QVariant.Double),
                      QgsField('01Testyl_a', QVariant.Double),
                      QgsField('02Test_no_R', QVariant.Double),
                      QgsField('02Test_no_G', QVariant.Double),
                      QgsField('02Test_no_B', QVariant.Double),
                      QgsField('02Test_no_a', QVariant.Double)]

        provider.addAttributes(attributes)
        name_to_index = provider.fieldNameMap()
        r_index = name_to_index['01Testyl_R']
        g_index = name_to_index['01Testyl_G']
        b_index = name_to_index['01Testyl_B']
        a_index = name_to_index['01Testyl_a']

        # Add features (color-values) to provider
        feature1 = QgsFeature()
        feature1.setAttributes([0, 0, 0, 0, 0, 0.0, 255.0, 255, 0, 0, 0, 0])
        feature2 = QgsFeature()
        feature2.setAttributes([0, 0, 0, 0, 170, 12, 17, 36, 0, 0, 0, 0])
        feature3 = QgsFeature()
        feature3.setAttributes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        provider.addFeatures([feature1, feature2, feature3])

        v_layer.commitChanges()
        # create color values which shall be added
        color_dict = {'RGBa(0, 0, 255, 255)': ('height', 0, 4),
                'RGBa(170, 12, 17, 36)': ('height', 4,8)}
        field_name_prefix = '01Testyl'
        layer_interaction.add_parameter_info_to_layer(color_dict, field_name_prefix, v_layer)

        field_names = provider.fieldNameMap()
        self.assertTrue('01Testyl_L' in field_names)
        self.assertTrue('01Testyl_H' in field_names)
        self.assertTrue('01Testyl_P' in field_names)
        self.assertTrue('01Testyl_0' not in field_names)
        self.assertTrue('01Testyl_1' not in field_names)

        for feat in provider.getFeatures():
            if feat.attribute('01Testyl_R') == 0 and feat.attribute('01Testyl_a') == 255:
                self.assertEqual(feat.attribute('01Testyl_P'), 'height')
                self.assertEqual(feat.attribute('01Testyl_L'), 0)
                self.assertEqual(feat.attribute('01Testyl_H'), 4)
            if feat.attribute('01Testyl_R') == 170 and feat.attribute('01Testyl_a') == 36:
                self.assertEqual(feat.attribute('01Testyl_P'), 'height')
                self.assertEqual(feat.attribute('01Testyl_L'), 4)
                self.assertEqual(feat.attribute('01Testyl_H'), 8)
            if feat.attribute('01Testyl_R') == 0 and feat.attribute('01Testyl_a') == 0:
                self.assertEqual(feat.attribute('01Testyl_P'), None)
                self.assertEqual(feat.attribute('01Testyl_L'), None)
                self.assertEqual(feat.attribute('01Testyl_H'), None)


if __name__ == '__main__':
    unittest.main()