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
    # factor for golden rule

    hlac= NULL

    if not oeq_global.isnull([parameters['AREA'] , parameters['FLOORS'] , parameters['BS_QTC'] , parameters['RF_QTC'] , parameters['WL_QTC'] , parameters['WN_QTC']]):
        living_area = float(parameters['AREA']) * float(parameters['FLOORS']) * 0.8
        qtp_total = float(parameters['BS_QTC']) + float(parameters['RF_QTC']) + float(parameters['WL_QTC']) + float(parameters['WN_QTC']) #*1.2
        hlac=qtp_total/living_area

    return {'HLAC': {'type': QVariant.Double,'value': hlac}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Building Quality (QT per Livig Area, Contemporary)',
    layer_name= 'QT Building per Livig Area Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id= None,
    source_type='none',
    par_in=['AREA','FLOORS','BS_QTC','RF_QTC','WL_QTC','WN_QTC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HLAC'],
    description="Calculate the contemporary Transmission Heat Loss per Living Area",
    evaluation_method=calculation)

extension.registerExtension(default=True)
