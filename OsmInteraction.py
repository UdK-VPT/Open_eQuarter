from PyQt4.QtCore import *
from qgis.utils import iface, plugins
from qgis.core import QgsMapLayerRegistry

def get_open_layers_plugin_ifexists(plugin_name):
    """
    Check if a plugin with the given name exists.

    :param plugin_name: Name of the plugin to check existence of.
    :type plugin_name: str

    :return plugin: Return the plugin if it was found
    :rtype: OpenlayersPlugin instance

    :return False: Return False if the plugin was not found and the lookup resulted in an exception.
    :rtype: bool
    """

    if not plugin_name or plugin_name.isspace():
        return None

    plugin_dict = plugins
    plugin = None

    try:
        plugin = plugin_dict[plugin_name]
        return plugin
    except KeyError:
        print "No plugin with the given name '" + plugin_name + "' found. Please check the plugin settings."
        return None


def open_osm_layer(layer_type_id):

    plugin = get_open_layers_plugin_ifexists('openlayers_plugin')

    if plugin == None or layer_type_id < 0:
        return None

    open_layer = plugin._olLayerTypeRegistry.getById(layer_type_id)

    number_of_layers = len(QgsMapLayerRegistry.instance().mapLayers())
    plugin.addLayer(open_layer)

    return (number_of_layers+1) == len(QgsMapLayerRegistry.instance().mapLayers())