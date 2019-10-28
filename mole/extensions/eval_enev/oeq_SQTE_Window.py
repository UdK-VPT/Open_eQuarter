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

    wn_sqte = NULL
    if not oeq_global.isnull([parameters['WN_UE'],parameters['HHRS']]):
        wn_sqte= float(parameters['WN_UE'])*float(parameters['HHRS'])/1000
    return {'WN_SQTE': {'type': QVariant.Double, 'value': wn_sqte}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='EnEV Spec. Transm. Heat Loss',
    extension_name='Window SpecTransm (SQT, EnEV)',
    layer_name= 'SQT Window EnEV',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_SQTE',
    source_type='none',
    par_in=['WN_UE','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_SQTE'],
    description=u"Calculate the EnEV Transmission Heat Loss of the Building's Windows per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
