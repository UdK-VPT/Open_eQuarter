from PyQt4.QtCore import *
from qgis.core import QgsMapLayerRegistry
from qgis.utils import plugins

def open_osm_layer(layer_type_id, plugin_name = 'openlayers_plugin'):

    try:
        plugin = plugins[plugin_name]
    except KeyError as ke:
        print "The open layers plugin has not been found under the given name " + plugin_name
        return False

    if plugin == None or layer_type_id < 0:
        return False

    open_layer = plugin._olLayerTypeRegistry.getById(layer_type_id)

    number_of_layers = len(QgsMapLayerRegistry.instance().mapLayers())
    plugin.addLayer(open_layer)

    return (number_of_layers+1) == len(QgsMapLayerRegistry.instance().mapLayers())