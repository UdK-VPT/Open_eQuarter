# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    ar = NULL
    perim = NULL
    if bool(parameters['AREA_ALK']):
        ar = parameters['AREA_ALK']
    if bool(parameters['PERI_ALK']):
        perim = parameters['PERI_ALK']
    return {'AREA': {'type': QVariant.Double,
                           'value': ar},
            'PERIMETER': {'type': QVariant.Double,
                     'value': perim},
            }



extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Geometry',
    extension_name='Area_Perimeter',
    layer_name= 'Area and Perimeter',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='',
    source_type='layer',
    par_in=['AREA_ALK','PERI_ALK'],
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=[],
    description=u"Write the building's area and perimeter to database",
    evaluation_method=calculation)

extension.registerExtension(default=True)
