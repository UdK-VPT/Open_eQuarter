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
        if layer_name is not None and not layer_name.isspace():
            layer_registry = QgsMapLayerRegistry.instance()
            layer_available = layer_registry.mapLayersByName(layer_name)

            if layer_available:
                # drop down menu, listing all available layers
                in_layer = self.pst_dialog.inSample
                index = in_layer.findText(layer_name)
                in_layer.setCurrentIndex(index)

    def select_and_rename_files_for_sampling(self):
        """
        Select all available layers for the point sampling and rename multiple occurrences of the same name.
        Prepend an index, to separate the layers and append the information, which color value is displayed.
        :return plugin: Return the plugin if it was found or None otherwise
        :rtype: plugin instance
        """
        sample_list = self.pst_dialog.inData
        table = self.pst_dialog.fieldsTable
        number_of_samples = len(sample_list)

        RGBa_appendix = ['R', 'G', 'B', 'a']
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
            layer_name = table.item(i, 0).text().split(' : ')[0]
            if last_name != layer_name:
                last_name = layer_name
                prefix += 1
                RGBa_index = 0

            # Truncate the name to a maximum of 6 characters, since QGIS limits the length of a feature's name to 10
            # prepend prefix (with leading zero), truncated name and RGBa RGBa_appendix
            rgba = RGBa_appendix[RGBa_index]
            RGBa_index += 1
            export_name = '{:02d}{}_{}'.format(prefix, layer_name[0:6], rgba)

            replacement_map[layer_name] = export_name[:-2]
            # Change the text in the table, so the pst can manage its model accordingly/appropriately
            table.item(i, 1).setText(export_name)

        return replacement_map

    def start_sampling(self, path_to_layer, layer_name):

        if not path_to_layer or path_to_layer.isspace() or not layer_name or layer_name.isspace():
            return ''

        else:
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

                full_path = path.join(path_to_layer, layer_name + '.shp')
                self.pst_dialog.sampling(full_path)

                return full_path



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