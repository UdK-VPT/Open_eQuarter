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

    bs_qteh = NULL
    if not oeq_global.isnull([parameters['BS_AR'],parameters['BS_UEH'],parameters['HHRS']]):
        bs_qteh=float(parameters['BS_AR']) * float(parameters['BS_UEH'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'BS_QTEH': {'type': QVariant.Double, 'value': bs_qteh}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Transm. Heat Loss',
    extension_name='Base Quality (QT, EnEV Heritage)',
    layer_name= 'QT Base EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_QTEH',
    source_type='none',
    par_in=['BS_AR','BS_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_QTEH'],
    description="Calculate the EnEV Heritage Transmission Heat Loss of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
