from qgis.core import QgsMapLayerRegistry, QgsCoordinateReferenceSystem
from qgis.utils import plugins
from os import path
import sys


def get_plugin_ifexists(plugin_name):
    """
    Check if a plugin with the given name exists.

    :param plugin_name: Name of the plugin to check existence of.
    :type plugin_name: str

    :return plugin: Return the plugin if it was found or None otherwise
    :rtype: plugin instance
    """
    try:
        plugin = plugins[plugin_name]
        return plugin
    except KeyError:
        print "No plugin with the given name '" + plugin_name + "' found. Please check the plugin settings."
        return None

class PstInteraction(object):

    def __init__(self, iface, plugin_name='pointsamplingtool'):
        self.plugin_folder = path.dirname(sys.modules[plugin_name].__file__)

        # if the pst is not part of the path, add it to the path, so the modules can be imported
        if self.plugin_folder not in sys.path:
            sys.path.insert(0, self.plugin_folder)

        from doPointSamplingTool import Dialog

        self.pst_dialog = Dialog(iface)
        self.path_to_output_layer = ''

    def set_input_layer(self, layer_name):

        if layer_name is not None and not layer_name.isspace():

            layer_available = False
            layer_dict = QgsMapLayerRegistry.instance().mapLayers()
            for layer_key in layer_dict:
                layer = layer_dict[layer_key]

                if layer.name() == layer_name:
                    layer_available = True

            if layer_available:
                index = 0
                # drop down menu, listing all available layers
                in_layer = self.pst_dialog.inSample
                in_layer.setCurrentIndex(index)

                # while the given layer is not active, iterate over the menu
                while in_layer.currentText() != layer_name:
                    index += 1
                    in_layer.setCurrentIndex(index)

    # def set_output_layer(self, path_to_layer, encoding, crs_name):
    #
    #     if path_to_layer is not None and not path_to_layer.isspace() and not path.exists(path_to_layer):
    #
    #         if (encoding is not None and not encoding.isspace()) and \
    #                 (crs_name is not None and QgsCoordinateReferenceSystem().createFromUserInput(crs_name)):
    #
    #             out_path, out_name = path.split(path_to_layer)
    #             if out_name.upper().endswith('.SHP'):
    #                 out_name = out_name[:-4]
    #
    #             full_path = path.join(out_path, out_name + '.shp')
    #
    #             vlayer = QgsVectorLayer('Point?crs=EPSG:4326', 'pas_out2', 'memory', False)
    #             return_code = QgsVectorFileWriter.writeAsVectorFormat(vlayer, full_path, encoding, QgsCoordinateReferenceSystem(crs_name), 'ogr')
    #
    #             if return_code == QgsVectorFileWriter.NoError:
    #                 QgsMapLayerRegistry.instance().addMapLayer(vlayer)
    #                 self.path_to_output_layer = full_path

    def select_files_for_sampling(self):

        sample_list = self.pst_dialog.inData
        fields_table = self.pst_dialog.fieldsTable
        number_of_samples = len(sample_list)

        # ToDo change the range to full select and eliminate duplicates
        #for i in range(0, number_of_samples):
        for i in range(number_of_samples):
            print sample_list.item(i).text()
            sample_list.setItemSelected(sample_list.item(i), True)



    def start_sampling(self, path_to_layer, layer_name):
        if path_to_layer and not path_to_layer.isspace() and \
                layer_name and not layer_name.isspace():

            if path.exists(path_to_layer):

                if layer_name.upper().endswith('.SHP'):
                    layer_name = layer_name[:-4]

                if path.exists(path.join(path_to_layer, layer_name + '.shp')):
                    new_name = layer_name
                    suffix = 0

                    while path.exists(path.join(path_to_layer, new_name + '.shp')):
                        suffix += 1
                        new_name = layer_name + str(suffix)

                    layer_name = new_name

                full_path = path.join(path_to_layer,layer_name + '.shp')
                self.pst_dialog.sampling(full_path)

                return full_path

        else:
            return ''


class OlInteraction(object):


    def __init__(self, plugin_name = 'openlayers_plugin'):

        self.plugin = None

        try:
            plugin = plugins[plugin_name]
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
            self.plugin.setMapCrs(QgsCoordinateReferenceSystem(crs_string))