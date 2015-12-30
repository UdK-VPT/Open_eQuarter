from PyQt4 import QtCore
from qgis.core import QgsMapLayerRegistry, QgsCoordinateReferenceSystem, QgsMapLayer, QgsRasterLayer, QgsVectorLayer
from qgis.core import QgsField, QgsFeature, QgsDistanceArea, QgsPoint
from qgis import utils
from os import path
import sys

from mole.qgisinteraction.layer_interaction import find_layer_by_name, add_attributes_if_not_exists, delete_layer_files
from mole.qgisinteraction import legend
from mole.project import config

def get_plugin_ifexists(plugin_name):
    """
    Check if a plugin with the given name exists.

    :param plugin_name: Name of the plugin to check existence of.
    :type plugin_name: str

    :return plugin: Return the plugin if it was found or None otherwise
    :rtype: plugin instance
    """
    from mole import oeq_global
    try:
        plugin = utils.plugins[plugin_name]
        return plugin
    except KeyError:
        oeq_global.OeQ_push_warning(title="Mandatory Plugins: ", message="Please install Plugin '" + plugin_name + "' ")
        return None

class PstInteraction(object):

    def __init__(self, iface, plugin_name='pointsamplingtool'):
        if isinstance(plugin_name, str):
            try:
                self.plugin_folder = path.dirname(sys.modules[plugin_name].__file__)
                # if the pst is not part of the path, add it to the path, so the modules can be imported
                if self.plugin_folder not in sys.path:
                    sys.path.insert(0, self.plugin_folder)
            except KeyError:
                print(KeyError, plugin_name)

        from doPointSamplingTool import Dialog

        self.pst_dialog = Dialog(iface)
        self.path_to_output_layer = ''

    def set_input_layer(self, layer_name):
        layernode = legend.nodeByName(layer_name,'layer')
        if len(layernode) == 0:
            return None
        in_layer = self.pst_dialog.inSample
        index = in_layer.findText(layer_name)
        in_layer.setCurrentIndex(index)
        #if layer_name is not None and not layer_name.isspace():
        #    layer_registry = QgsMapLayerRegistry.instance()
        #    layer_available = layer_registry.mapLayersByName(layer_name)

        #    if layer_available:
                # drop down menu, listing all available layers


    def select_and_rename_files_for_sampling(self):
        """
        Select all available layers for the point sampling and rename multiple occurrences of the same name.
        Prepend an index, to separate the layers and append the information, which color value is displayed.
        :return plugin: Return the plugin if it was found or None otherwise
        :rtype: plugin instance
        """
        import mole.extensions as extensions

        sample_list = self.pst_dialog.inData
        table = self.pst_dialog.fieldsTable
        number_of_samples = len(sample_list)

        RGBa_appendices = ['R', 'G', 'B', 'a']
        RGBa_index = 0
        last_name = ''
        prefix = 0

        replacement_map = {}

        for i in range(number_of_samples):
            # select all fields via the inData-view,
            # so the point sampling tool can manage its model accordingly/appropriately
            sample_list.setItemSelected(sample_list.item(i), True)

            # Get the source-name (as displayed in the field-table) and check if it was used already
            # (the name has to be split, since it is displayed in the form 'layer_name : Band x' to get the layer_name)
            table_index = table.rowCount()-1
            table_text = table.item(table_index, 0).text().split(' : ')
            layer_name = table_text[0]
            band_name = table_text[1]
            layer = find_layer_by_name(layer_name)

            # Check if the layer was already used
            if last_name != layer_name:
                last_name = layer_name
                prefix += 1
                RGBa_index = 0


            if (layer.name() == config.housing_layer_name and
                    (band_name.startswith('AREA') or band_name.startswith('PERIMETER') or band_name.startswith('BLD_ID'))):
                continue
            elif (layer.type() == QgsMapLayer.RasterLayer and
                  layer.rasterType() == QgsRasterLayer.Multiband and
                  layer.bandCount() == 4
                  ):
                # Truncate the name to a maximum of 6 characters, since QGIS limits the length of a feature's name to 10
                # prepend prefix (with leading zero), truncated name and RGBa-appendix
                try:
                    rgba = RGBa_appendices[RGBa_index]
                    RGBa_index += 1
                except IndexError as IError:
                    RGBa_index = 0
                    print(self.__module__, 'IndexError when appending the RGBa-Appendix: {}'.format(IError))
                if extensions.by_layername(layer_name, 'Import') == []:
                    export_name = '{:02d}{}_{}'.format(prefix, layer_name[0:6], rgba)
                else:
                    export_name = extensions.by_layername(layer_name, 'Import')[0].field_id + '_' + rgba

                replacement_map[layer_name] = export_name[:-2]
                # Change the text in the table, so the pst can manage its model accordingly/appropriately
                table.item(table_index, 1).setText(export_name)
            else:
                sample_list.setItemSelected(sample_list.item(i), False)
                continue

        return replacement_map

    def start_sampling(self, path_to_layer, layer_name):
        if not path_to_layer or path_to_layer.isspace() or not layer_name or layer_name.isspace():
            return ''
        else:
            delete_layer_files(layer_name)
            full_path = path.join(path_to_layer, layer_name + '.shp')
            self.set_input_layer(config.pst_input_layer_name)
            self.pst_dialog.sampling(full_path)
            return full_path


class OlInteraction(object):


    def __init__(self, plugin_name = 'openlayers_plugin'):
        """
        Make the plugin accessible by looking it up in the plugin-dictionary
        :param plugin_name: Name of the open-layers-plugin (as stored in utils.plugins)
        :type plugin_name: str
        :return:
        :rtype:
        """
        self.plugin = None

        try:
            plugin = utils.plugins[plugin_name]
        except KeyError as ke:
            print "The open layers plugin has not been found under the given name " + plugin_name
            return None

        if plugin is not None:
            self.plugin = plugin

    def open_osm_layer(self, layer_type_id):
        """
        Interact with the Open-Street-Map plugin and open an open street map according to open_layer_type_id
        :param open_layer_type_id: ID of the open-layer type
        :type open_layer_type_id: int
        :return:
        :rtype:
        """

        open_layer = self.plugin._olLayerTypeRegistry.getById(layer_type_id)

        number_of_layers = len(QgsMapLayerRegistry.instance().mapLayers())
        self.plugin.addLayer(open_layer)

        return (number_of_layers+1) == len(QgsMapLayerRegistry.instance().mapLayers())

    def set_map_crs(self, crs_string):
        """
        Use the openlayer-plugin to set the project crs to the given crs and to do a re-projection to keep the currently viewed extent focused
        :param crs: The new crs to set the project to
        :type crs: str
        :return:
        :rtype:
        """
        # if the given crs is valid
        if not crs_string.isspace() and QgsCoordinateReferenceSystem().createFromUserInput(crs_string):
            self.plugin.setMapCrs(QgsCoordinateReferenceSystem(crs_string, QgsCoordinateReferenceSystem.EpsgCrsId))


class RealCentroidInteraction(object):

    def __init__(self, plugin_name='realcentroid'):
        """
        Make the plugin accessible by looking it up in the plugin-dictionary
        :param plugin_name: Name of the realcentroids-plugin (as stored in utils.plugins)
        :type plugin_name: str
        :return:
        :rtype:
        """
        self.plugin = None

        try:
            plugin = utils.plugins[plugin_name]
            self.plugin = plugin
            self.plugin.__init__(utils.iface)
        except KeyError as KError:
            print(KError, 'The realcentroid plugin has not been found by the given name "{}"'.format(plugin_name))

    def create_centroids(self, polygon_name, path_to_output_shape):
        self.plugin.dlg.showEvent(QtCore.QEvent.Show)
        polygon_combobox = self.plugin.dlg.ui.layerBox

        for i in range(polygon_combobox.count()):
            if polygon_combobox.itemText(i) == polygon_name:
                polygon_combobox.setCurrentIndex(i)
                break
        else:
            print('Layer {} not found in combobox.'.format(polygon_name))
            return None

        self.plugin.dlg.shapefileName = path_to_output_shape
        self.plugin.dlg.encoding = sys.getfilesystemencoding()
        self.plugin.centroids()

        file_info = QtCore.QFileInfo(path_to_output_shape)
        if file_info.exists():
            layer_name = file_info.completeBaseName()
            output_layer = QgsVectorLayer(path_to_output_shape,layer_name, "ogr")
            return output_layer
        else:
            return None

    def calculate_accuracy(self, polygon_layer, point_layer):
        """
        Calculate the distance of each centroid on a point-layer to their surrounding polygons
        :param polygon_layer: A layer containing polygons
        :type polygon_layer: QgsVectorLayer
        :param point_layer: A layer containing the (supposed to be) centroids of that polygon
        :type point_layer: QgsVectorLayer
        :return:
        :rtype:
        """
        point_provider = point_layer.dataProvider()
        add_attributes_if_not_exists(point_layer, [QgsField('DIST', QtCore.QVariant.Double)])

        distance_area = QgsDistanceArea()
        poly_iterator = polygon_layer.dataProvider().getFeatures()
        point_iterator = point_provider.getFeatures()
        poly_feature = QgsFeature()
        point_feature = QgsFeature()
        field_index = point_provider.fieldNameIndex('DIST')

        while (poly_iterator.nextFeature(poly_feature) and
               point_iterator.nextFeature(point_feature)):
            geom= poly_feature.geometry()
            if geom is not None:
                try:
                        poly_point = geom.asPolygon()[0]
                        centroid = geom.asPoint()
                except IndexError:
                    continue
                distances = {}
                for i, point in enumerate(poly_point):
                    end = poly_point[(i+1) % len(poly_point)]
                    try:
                        intersect = self.intersect_point_to_line(centroid, point, end)
                        if intersect != centroid:
                            dist = distance_area.measureLine(centroid, intersect)
                            distances[intersect] = dist
                    except ZeroDivisionError as InvalidMath:
                        continue
                values = {field_index: min(distances.values())}
                point_provider.changeAttributeValues({point_feature.id(): values})



    def intersect_point_to_line(self, point, line_start, line_end):
        """
        Finds the point i on a line which, given a point p describes a line ip, orthogonal to a given line
        (as found on http://gis.stackexchange.com/questions/59169/how-to-draw-perpendicular-lines-in-qgis)
        :param point: The point p
        :type point: QgsPoint
        :param line_start: The lines start
        :type line_start: QgsPoint
        :param line_end: The lines end
        :type line_end: QgsPoint
        :return: The point i, which is the end of the orthogonal line
        :rtype: QgsPoint
        """
        magnitude = line_start.sqrDist(line_end)
        # minimum distance
        u = ((point.x() - line_start.x()) * (line_end.x() - line_start.x()) + (point.y() - line_start.y()) * (line_end.y() - line_start.y()))/(magnitude)
        # intersection point on the line
        ix = line_start.x() + u * (line_end.x() - line_start.x())
        iy = line_start.y() + u * (line_end.y() - line_start.y())
        return QgsPoint(ix,iy)
