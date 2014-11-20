__author__ = 'VPTtutor'
from Qgis.core import *


class DummyInterface(object):

    def __getattr__(self, *args, **kwargs):
        def dummy(*args, **kwargs):
            return self

        return dummy

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

    def layers(self):
        # simulate iface.legendInterface().layers()
        return QgsMapLayerRegistry.instance().mapLayers().values()