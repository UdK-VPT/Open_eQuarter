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
    htc = NULL
    if not oeq_global.isnull([parameters['BS_UC'] , parameters['BS_AR'] , parameters['RF_UC'] , parameters['RF_AR'] , parameters['WL_UC'] , parameters['WL_AR'] , parameters['WN_UC'] , parameters['WN_AR']]):
        qtp_total = float(parameters['BS_UC'] * parameters['BS_AR'] *0.35 ) + float(parameters['RF_UC'] * parameters['RF_AR']) + float(parameters['WL_UC'] * parameters['WL_AR'] ) + float(parameters['WN_UC'] * parameters['WN_AR'])
        env_area =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        htc=qtp_total/env_area
    return {'HTC': {'type': QVariant.Double,'value': htc}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, Contemporary)',
    layer_name= 'SHT Envelope Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTC',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UC','RF_UC','WL_UC','WN_UC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTC'],
    description="Calculate the contemporary Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
