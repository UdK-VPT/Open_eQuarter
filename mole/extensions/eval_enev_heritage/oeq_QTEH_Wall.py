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

    wl_qteh = NULL
    if not oeq_global.isnull([parameters['WL_AR'],parameters['WL_UEH'],parameters['HHRS']]):
        wl_qteh=float(parameters['WL_AR']) * float(parameters['WL_UEH'])*float(parameters['HHRS'])/1000
    return {'WL_QTEH': {'type': QVariant.Double, 'value': wl_qteh}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Heritage Transm. Heat Loss',
    extension_name='Wall Quality (QT, EnEV Heritage)',
    layer_name= 'QT Wall EnEV Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_QTEH',
    source_type='none',
    par_in=['WL_AR','WL_UEH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_QTEH'],
    description=u"Calculate the EnEV Heritage Transmission Heat Loss of the Building's Walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
