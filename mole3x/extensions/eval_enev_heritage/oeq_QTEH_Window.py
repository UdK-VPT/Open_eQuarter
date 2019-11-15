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

    wn_qteh = NULL
    if not oeq_global.isnull([parameters['WN_AR'],parameters['WN_UEH'],parameters['HHRS']]):
        wn_qteh=float(parameters['WN_AR']) * float(parameters['WN_UEH'])*float(parameters['HHRS'])/1000
    return {'WN_QTEH': {'type': QVariant.Double, 'value': wn_qteh}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Transm. Heat Loss',
    extension_name='Window Quality (QT, EnEV Heritage)',
    layer_name= 'QT Window EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_QTEH',
    source_type='none',
    par_in=['WN_AR','WN_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_QTEH'],
    description="Calculate the EnEV Heritage Transmission Heat Loss of the Building's Windows",
    evaluation_method=calculation)

extension.registerExtension(default=True)
