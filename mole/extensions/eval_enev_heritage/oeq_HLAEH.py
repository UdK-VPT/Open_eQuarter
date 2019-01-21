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
    # factor for golden rule

    hlaeh= NULL

    if not oeq_global.isnull([parameters['AREA'] , parameters['FLOORS'] , parameters['BS_QTEH'] , parameters['RF_QTEH'] , parameters['WL_QTEH'] , parameters['WN_QTEH']]):
        living_area = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
        qteh_total = float(parameters['BS_QTEH']) + float(parameters['RF_QTEH']) + float(parameters['WL_QTEH']) + float(parameters['WN_QTEH']) #*1.2
        hlaeh=qteh_total/living_area

    return {'HLAEH': {'type': QVariant.Double,'value': hlaeh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Livig Area, EnEV Heritage)',
    layer_name= 'QT Building per Living Area EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id= None,
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTEH','RF_QTEH','WL_QTEH','WN_QTEH'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAEH'],
    description=u"Calculate the EnEV Heritage Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
