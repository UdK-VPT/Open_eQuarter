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
    from qgis.PyQt.QtCore import QVariant

    htp = NULL
    if not oeq_global.isnull([parameters['BS_UP'] , parameters['BS_AR'] , parameters['RF_UP'] , parameters['RF_AR'] , parameters['WL_UP'] , parameters['WL_AR'] , parameters['WN_UP'] , parameters['WN_AR']]):
        qtp_total = float(parameters['BS_UP'] * parameters['BS_AR'] * 0.35 ) + float(parameters['RF_UP'] * parameters['RF_AR']) + float(parameters['WL_UP'] * parameters['WL_AR'] ) + float(parameters['WN_UP'] * parameters['WN_AR'])
        env_area =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        htp=qtp_total/env_area
    return {'HTP': {'type': QVariant.Double, 'value': htp}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, Present)',
    layer_name= 'SHT Envelope Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTP',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UP','RF_UP','WL_UP','WN_UP'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTP'],
    description="Calculate the present Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
