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

    rf_qteh = NULL
    if not oeq_global.isnull([parameters['RF_AR'],parameters['RF_UEH'],parameters['HHRS']]):
        rf_qteh=float(parameters['RF_AR']) * float(parameters['RF_UEH'])*float(parameters['HHRS'])/1000
    return {'RF_QTEH': {'type': QVariant.Double, 'value': rf_qteh}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Transm. Heat Loss',
    extension_name='Roof Quality (QT, EnEV Heritage)',
    layer_name= 'QT Roof EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_QTEH',
    source_type='none',
    par_in=['RF_AR','RF_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_QTEH'],
    description=u"Calculate the EnEV Heritage Transmission Heat Loss of the Building's Roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
