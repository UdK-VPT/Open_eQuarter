from PyQt4.QtCore import *
from qgis.utils import iface, plugins


def get_open_layers_plugin_ifexists(plugin_name):
    """
    Check if a plugin with the given name exists.

    :param plugin_name: Name of the plugin to check existence of.
    :type plugin_name: str

    :return plugin_exists: Return the plugin if it was found
    :rtype: OpenlayersPlugin instance

    :return False: Return False if the plugin was not found and the lookup resulted in an exception.
    :rtype: bool
    """

    if not plugin_name or plugin_name.isspace():
        return False

    plugin_dict = plugins
    plugin_exists = False

    try:
        plugin_exists = plugin_dict[plugin_name]
        return plugin_exists
    except KeyError:
        print "No plugin under the given name '" + plugin_name + "' found. Please check the plugins settings."
        return False


def open_osm_layer(layer_type_id):

    plugin = get_open_layers_plugin_ifexists()

    if plugin == None or layer_type_id < 0:
        return False

    open_layer = plugin._olLayerTypeRegistry.getById(layer_type_id)
    return plugin.addLayer(open_layer)