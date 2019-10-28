# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    hte = NULL
    if not oeq_global.isnull([parameters['BS_UE'] , parameters['BS_AR'] , parameters['RF_UE'] , parameters['RF_AR'] , parameters['WL_UE'] , parameters['WL_AR'] , parameters['WN_UE'] , parameters['WN_AR']]):
        qte_total = float(parameters['BS_UE'] * parameters['BS_AR'] *0.35 ) + float(parameters['RF_UE'] * parameters['RF_AR']) + float(parameters['WL_UE'] * parameters['WL_AR'] ) + float(parameters['WN_UE'] * parameters['WN_AR'])
        env_area =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        hte=qte_total/env_area
    return {'HTE': {'type': QVariant.Double,'value': hte}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, EnEV)',
    layer_name= 'SHT Envelope EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTE',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UE','RF_UE','WL_UE','WN_UE'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTE'],
    description=u"Calculate the EnEV Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
