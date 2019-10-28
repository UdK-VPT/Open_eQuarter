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

    htph = NULL
    if not oeq_global.isnull([parameters['BS_UPH'] , parameters['BS_AR'] , parameters['RF_UPH'] , parameters['RF_AR'] , parameters['WL_UPH'] , parameters['WL_AR'] , parameters['WN_UPH'] , parameters['WN_AR']]):
        qtph_total = float(parameters['BS_UPH'] * parameters['BS_AR'] * 0.35 ) + float(parameters['RF_UPH'] * parameters['RF_AR']) + float(parameters['WL_UPH'] * parameters['WL_AR'] ) + float(parameters['WN_UPH'] * parameters['WN_AR'])
        env_area = float(parameters['BS_AR']) + float(parameters['RF_AR']) + float(parameters['WL_AR']) + float(parameters['WN_AR'])
        htph=qtph_total/env_area
    return {'HTPH': {'type': QVariant.Double, 'value': htph}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Envelope Quality (SHT, Present Heritage)',
    layer_name= 'SHT Envelope Present Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HTPH',
    source_type='none',
    par_in=['BS_AR','RF_AR','WL_AR','WN_AR','BS_UPH','RF_UPH','WL_UPH','WN_UPH'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HTPH'],
    description=u"Calculate the present heritage Transmission Heat Coefficient of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
