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

    hlaph = NULL
    if not oeq_global.isnull([parameters['AREA'] , parameters['FLOORS'] , parameters['BS_QTPH'] , parameters['RF_QTPH'] , parameters['WL_QTPH'] , parameters['WN_QTPH']]):
        living_area = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
        qtph_total = float(parameters['BS_QTPH']) + float(parameters['RF_QTPH']) + float(parameters['WL_QTPH']) + float(parameters['WN_QTPH'])*1.2
        hlaph=qtph_total/living_area
    return {'HLAPH': {'type': QVariant.Double,'value': hlaph}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Living Area, Present Heritage)',
    layer_name= 'QT Building per Living Area Present Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='HLAPH',
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTPH','RF_QTPH','WL_QTPH','WN_QTPH'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAPH'],
    description=u"Calculate the present heritage Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
