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
    hteh = NULL
    if not oeq_global.isnull([parameters['BS_UEH'] , parameters['BS_AR'] , parameters['RF_UEH'] , parameters['RF_AR'] , parameters['WL_UEH'] , parameters['WL_AR'] , parameters['WN_UEH'] , parameters['WN_AR']]):
        qteh_total = float(parameters['BS_UEH'] * parameters['BS_AR'] *0.35 ) + float(parameters['RF_UEH'] * parameters['RF_AR']) + float(parameters['WL_UEH'] * parameters['WL_AR'] ) + float(parameters['WN_UEH'] * parameters['WN_AR'])
        env_area =  float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        hteh=qteh_total/env_area
    return {'HTEH': {'type': QVariant.Double,'value': hteh}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, EnEV Heritage)',
    layer_name= 'SHT Envelope EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTEH',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UEH','RF_UEH','WL_UEH','WN_UEH'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTEH'],
    description=u"Calculate the EnEV Heritage Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
