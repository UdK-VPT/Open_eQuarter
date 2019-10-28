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

    wl_qtph = NULL
    if not oeq_global.isnull([parameters['WL_AR'],parameters['WL_UPH'],parameters['HHRS']]):
        wl_qtph=float(parameters['WL_AR']) * float(parameters['WL_UPH'])*float(parameters['HHRS'])/1000
    return {'WL_QTPH': {'type': QVariant.Double, 'value': wl_qtph}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Heritage Transm. Heat Loss',
    extension_name='Wall Quality (QT, Present Heritage)',
    layer_name= 'QT Wall Present Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_QTPH',
    source_type='none',
    par_in=['WL_AR','WL_UPH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_QTPH'],
    description=u"Calculate the present heritage Transmission Heat Loss of the Building's Walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
