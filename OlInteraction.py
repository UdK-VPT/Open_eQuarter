from PyQt4.QtCore import *
from qgis.core import QgsMapLayerRegistry, QgsCoordinateReferenceSystem
from qgis.utils import plugins


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
