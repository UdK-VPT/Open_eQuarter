from qgis.core import QgsMapLayerRegistry


class QgisTestInterface(object):

    def __init__(self):
        self.layer_visibilty = {}

    def layers(self):
        # simulate iface.legendInterface().layers()
        return QgsMapLayerRegistry.instance().mapLayers().values()

    def legendInterface(self):
        return self

    def setLayerVisible(self, layer, visible):
        self.layer_visibilty[layer.name()] = visible

    def isLayerVisible(self, layer):
        return self.layer_visibilty[layer.name()]