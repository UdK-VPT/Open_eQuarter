from unittest import TestCase
from os import path, remove, walk

from qgis.core import QgsApplication, QgsProviderRegistry, QgsVectorLayer, QgsMapLayerRegistry, QgsRasterLayer, QgsCoordinateReferenceSystem
from PyQt4 import QtCore

from Open_eQuarter.qgisinteraction import LayerInteraction
from QgisTestInterface import QgisTestInterface


class LayerInteraction_test(TestCase):

    def __init__(self, testName, iface = QgisTestInterface()):
        super(LayerInteraction_test, self).__init__(testName)
        self.iface = iface
        self.layer_list = []
        self.valid_wms_url = 'crs=EPSG:3068&dpiMode=7&format=image/png&layers=0&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/k5'

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

        layer_name = LayerInteraction.biuniquify_layer_name('MyLayer')
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
        layer_name = LayerInteraction.biuniquify_layer_name('this_layer_was_added_for_testing_purpose')

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

        v1_name = LayerInteraction.biuniquify_layer_name('layer1')
        v2_name = LayerInteraction.biuniquify_layer_name('layer2')
        v3_name = LayerInteraction.biuniquify_layer_name('layer3')
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
        v1_name = LayerInteraction.biuniquify_layer_name('layer1')

        reg.addMapLayer(QgsVectorLayer('Polygon?crs=EPSG:3857', v1_name, 'memory', False))
        self.layer_list.append(v1_name)
        self.assertEqual(reg.mapLayersByName(v1_name)[0].name(), v1_name, 'Layer was not added.')

        LayerInteraction.hide_or_remove_layer(v1_name, 'hide', iface)
        self.assertFalse(iface.legendInterface().isLayerVisible(LayerInteraction.find_layer_by_name(v1_name)))

        LayerInteraction.hide_or_remove_layer(v1_name, 'remove')
        self.assertEqual(reg.mapLayersByName(v1_name), [], 'Layer was not removed.')

    def test_write_vector_layer_to_disk(self):

        v_layer_name = LayerInteraction.biuniquify_layer_name('MyWriteTestLayer')
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
        edit_layer_name = LayerInteraction.biuniquify_layer_name('MylayerForEditing')
        edit_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', edit_layer_name, 'memory', False)
        reg.addMapLayer(edit_layer)
        self.layer_list.append(edit_layer_name)

        LayerInteraction.trigger_edit_mode(self.iface, edit_layer_name)

        self.assertTrue(edit_layer.isEditable())

        LayerInteraction.trigger_edit_mode(self.iface, edit_layer_name, 'off')
        self.assertFalse(edit_layer.isEditable())

    def test_get_wms_layer_list(self):
        wms_url_with_parameters = self.valid_wms_url
        # use this list for proper testing...
        visibility = [True, False, True, True, True, False]
        # when debuggng, use the list below instead
        # visibility = [True]


        for i, visible in enumerate(visibility):
            layer_name = LayerInteraction.biuniquify_layer_name('r{0}_visible:{1}'.format(i, visible))
            rlayer = QgsRasterLayer(wms_url_with_parameters, layer_name, 'wms')
            self.assertTrue(rlayer.isValid(), layer_name.join(' is not a valid raster layer'))
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            self.iface.legendInterface().setLayerVisible(rlayer, visible)
            self.layer_list.append(layer_name)

        # get a list of all visible wms layers
        expected_layers = {}
        actual_layers = {}
        visible_raster_layers = LayerInteraction.get_wms_layer_list(self.iface, 'visible')
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
        invisible_raster_layers = LayerInteraction.get_wms_layer_list(self.iface, 'invisible')
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
        invisible_raster_layers = LayerInteraction.get_wms_layer_list(self.iface, 'all')
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

        returned_layer = LayerInteraction.open_wms_as_raster(self.iface, invalid_url, layer_name)
        self.assertIsNone(returned_layer)

        returned_layer = LayerInteraction.open_wms_as_raster(self.iface, valid_url, layer_name)
        self.assertIsNotNone(returned_layer, 'Tried to open a layer with the url {} failed, but should have passed.'.format(valid_url))
        self.assertTrue(returned_layer.isValid())
        self.assertEqual(layer_name, returned_layer.name())

    def test_zoom_to_layer(self):
        zoom_layer_name = LayerInteraction.biuniquify_layer_name('Test_zoom_to_layer')
        zoom_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', zoom_layer_name, 'memory', False)
        inactive_layer_name = LayerInteraction.biuniquify_layer_name('Layer_to_be_activated_and_deactivated_again')
        inactive_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', inactive_layer_name, 'memory', False)

        self.layer_list.extend([zoom_layer_name, inactive_layer_name])

        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(zoom_layer)
        reg.addMapLayer(inactive_layer)

        self.iface.setActiveLayer(inactive_layer)
        self.assertEqual(inactive_layer, self.iface.activeLayer(), 'The layer \"{}\" has not been activated'.format(inactive_layer_name))
        LayerInteraction.zoom_to_layer(self.iface, zoom_layer_name)

        # if the passed zoom_layer was set active, it has been found and used as the basis for the zoom
        # in that case, the formerly activated layer has to be inactive now!
        self.assertEqual(zoom_layer, self.iface.activeLayer())
        self.assertNotEqual(inactive_layer, self.iface.activeLayer())

    def test_biuniquify_layer_name(self):
        layer1_name = 'asdhhkhlu18927309hgdkaghdzuz7817982_unique'
        layer2_name = 'asdhhkhlu18927309hgdkaghdzuz781712ziadgwz_unique'
        layer3_name = ''

        self.assertIsNone(LayerInteraction.find_layer_by_name(layer1_name), 'Default layer name (\"{}\") is not unique!'.format(layer1_name))
        self.assertIsNone(LayerInteraction.find_layer_by_name(layer2_name), 'Default layer name (\"{}\") is not unique!'.format(layer2_name))

        layer1 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer1_name, 'memory', False)
        layer2 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer2_name, 'memory', False)

        self.layer_list.extend([layer1_name, layer2_name])

        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(layer1)
        reg.addMapLayer(layer2)

        self.assertEqual('', LayerInteraction.biuniquify_layer_name(''))
        self.assertEqual('', LayerInteraction.biuniquify_layer_name(None))

        # create a new unique name and add a layer with that name, to check the correctness of the functions while loop
        layer3_name = LayerInteraction.biuniquify_layer_name(layer1_name)
        self.assertEqual(layer1_name + '0', layer3_name)

        layer3 = QgsVectorLayer('Polygon?crs=EPSG:3857', layer3_name, 'memory', False)
        reg.addMapLayer(layer3)
        self.layer_list.extend([layer3_name])

        self.assertEqual(layer1_name +'1', LayerInteraction.biuniquify_layer_name(layer1_name))
        self.assertEqual(layer1_name +'2', LayerInteraction.biuniquify_layer_name(layer1_name + str(2)))
        self.assertEqual(layer2_name +'0', LayerInteraction.biuniquify_layer_name(layer2_name))

    def test_change_group_crs(self):
        layer1_name = 'asdhhkhlu18927309hgdkaghdzuz7817982_unique'
        layer2_name = 'asdhhkhlu18927309hgdkaghdzuz781712ziadgwz_unique'
        layer1 = QgsVectorLayer('Polygon?crs=EPSG:3068', layer1_name, 'memory', False)
        layer2 = QgsVectorLayer('Polygon?crs=EPSG:4326', layer2_name, 'memory', False)
        self.layer_list.extend([layer1_name, layer2_name])

        reg = QgsMapLayerRegistry.instance()
        reg.addMapLayer(layer1)
        reg.addMapLayer(layer2)

        layer_group = [layer1.name(), layer2.name()]
        target_crs = QgsCoordinateReferenceSystem('EPSG:3857')
        LayerInteraction.change_crs_of_layers(layer_group,target_crs)

        self.assertEqual(layer1.crs(), target_crs, 'The crs of the layer {} is not equal to the target crs.'.format(layer1.name()))
        self.assertEqual(layer2.crs(), target_crs, 'The crs of the layer {} is not equal to the target crs.'.format(layer2.name()))

    # ToDo
    def test_gdal_warp_layer_list(self):
        pass



