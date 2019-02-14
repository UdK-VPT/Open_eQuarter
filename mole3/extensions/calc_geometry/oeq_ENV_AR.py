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
    if not oeq_global.isnull([parameters['BS_AR'] , parameters['RF_AR'] , parameters['WL_AR'] , parameters['WN_AR']]):
        env_ar =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
    else:
        env_ar = NULL
    return {'ENV_AR':{'type': QVariant.Double,
                        'value': env_ar}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Geometry',
    extension_name='Envelope Area',
    layer_name= 'Envelope Area',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='ENV_AR',
    source_type='layer',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['ENV_AR'],
    description="Calculate the Envelope Area of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
