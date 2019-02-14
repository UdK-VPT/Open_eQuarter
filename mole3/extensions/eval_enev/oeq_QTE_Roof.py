# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole3 import oeq_global
from mole3.project import config
from mole3.extensions import OeQExtension
from mole3.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from qgis.PyQt.QtCore import QVariant

    rf_qte = NULL
    if not oeq_global.isnull([parameters['RF_AR'],parameters['RF_UE'],parameters['HHRS']]):
        rf_qte=float(parameters['RF_AR']) * float(parameters['RF_UE'])*float(parameters['HHRS'])/1000
    return {'RF_QTE': {'type': QVariant.Double, 'value': rf_qte}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Transm. Heat Loss',
    extension_name='Roof Quality (QT, EnEV)',
    layer_name= 'QT Roof EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_QTE',
    source_type='none',
    par_in=['RF_AR','RF_UE','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_QTE'],
    description="Calculate the EnEV Transmission Heat Loss of the Building's Roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
