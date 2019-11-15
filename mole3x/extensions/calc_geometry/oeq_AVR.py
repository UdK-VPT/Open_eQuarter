# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole3 import oeq_global
from mole3.project import config
from mole3.extensions import OeQExtension
from mole3.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant
    # factor for golden rule

    if not oeq_global.isnull([parameters['VOLUME'] , parameters['ENV_AR']]):
         avr=float(parameters['ENV_AR'])/float(parameters['VOLUME'])
    else:
        avr = NULL
    return {'AVR': {'type': QVariant.Double,
                           'value': avr}}



extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Geometry',
    extension_name='AV Ratio',
    layer_name= 'AV Ratio',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='AVR',
    source_type='layer',
    par_in=['VOLUME','ENV_AR'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['AVR'],
    description="Calculate the present Transmission Heat Koefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
