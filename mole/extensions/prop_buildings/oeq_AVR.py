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
    print ("AVR")
    avr = NULL
    if not oeq_global.isnull([parameters['AREA'] , parameters['HEIGHT'] , parameters['BS_AR'] , parameters['RF_AR'] , parameters['WL_AR'] , parameters['WN_AR']]):
        volume = float(parameters['AREA']) * float(parameters['HEIGHT'])
        env_area =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        avr=env_area/volume
    return {'AVR': {'type': QVariant.Double, 'value': avr}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='General',
    extension_name='AV Ratio',
    layer_name= 'AV Ratio',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='AVR',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','AREA','HEIGHT'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=False,
    show_results=['AVR'],
    description=u"Calculate the present Transmission Heat Koefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
