# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule

    hlae= NULL

    if not oeq_global.isnull([parameters['AREA'] , parameters['FLOORS'] , parameters['BS_QTE'] , parameters['RF_QTE'] , parameters['WL_QTE'] , parameters['WN_QTE']]):
        living_area = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
        qtp_total = float(parameters['BS_QTE']) + float(parameters['RF_QTE']) + float(parameters['WL_QTE']) + float(parameters['WN_QTE']) #*1.2
        hlae=qtp_total/living_area

    return {'HLAE': {'type': QVariant.Double,'value': hlae}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Livig Area, EnEV)',
    layer_name= 'QT Building per Livig Area EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id= None,
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTE','RF_QTE','WL_QTE','WN_QTE'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAE'],
    description=u"Calculate the EnEV Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
