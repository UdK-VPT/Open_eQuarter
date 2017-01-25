# -*- coding: utf-8 -*-


def load(self=None):
    self.createCoordinateLayer()
    return True



def evaluation(self=None, parameters={},feature=None):
    from qgis.core import NULL
    from PyQt4.QtCore import QVariant
    if bool(feature):
        geometry = feature.geometry()

        x = geometry.asPoint().x()
        y = geometry.asPoint().y()

        return {'LON': {'type': QVariant.Double,
                       'value': x},
                'LAT': {'type': QVariant.Double,
                       'value': y},
                config.building_id_key : {'type': QVariant.String,
                       'value': parameters[config.building_id_key]}
                }
    return {'LON': {'type': QVariant.Double,
                       'value': NULL},
                'LAT': {'type': QVariant.Double,
                       'value': NULL},
                config.building_id_key: {'type': QVariant.String,
                       'value': NULL}
               }


import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category= None,
    subcategory= None,
    extension_name='Building Coordinates (Calculated)',
    extension_type='information',
    field_id='',   #used for point sampling tool
    par_in= [config.building_id_key],
    #par_out=[config.building_id_key,'AREA','PERIMETER'],
    source_type='calc',
    layer_name=config.building_coordinate_layer_name,
    sourcelayer_name=config.building_coordinate_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    description=u'',
    source= None,
    source_crs= None,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method= load,
    preflight_method = None,
    evaluation_method= evaluation,
    postflight_method = None)

extension.registerExtension(default=True)
