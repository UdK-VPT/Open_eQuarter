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

    hlap = NULL
    if not oeq_global.isnull([parameters['AREA'] , parameters['FLOORS'] , parameters['BS_QTP'] , parameters['RF_QTP'] , parameters['WL_QTP'] , parameters['WN_QTP']]):
        living_area = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
        qtp_total = float(parameters['BS_QTP']) + float(parameters['RF_QTP']) + float(parameters['WL_QTP']) + float(parameters['WN_QTP'])*1.2
        hlap=qtp_total/living_area
    return {'HLAP': {'type': QVariant.Double,'value': hlap}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Living Area, Present)',
    layer_name= 'QT Building per Livig Area Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HLAP',
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTP','RF_QTP','WL_QTP','WN_QTP'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAP'],
    description=u"Calculate the present Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
