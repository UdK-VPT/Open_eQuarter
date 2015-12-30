# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    if not oeq_global.isnull([parameters['AREA'] , parameters['HEIGHT']]):
        volume  =  float(parameters['AREA']) * float(parameters['HEIGHT'])
    else:
        volume=NULL
    return{'VOLUME':{'type': QVariant.Double,
                        'value': volume}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Geometry',
    extension_name='Building Volume',
    layer_name= 'Building Volume',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='VOLUME',
    source_type='layer',
    par_in=['AREA','HEIGHT'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['VOLUME'],
    description=u"Calculate the Volume of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
