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

    rf_qtp = NULL
    if not oeq_global.isnull([parameters['RF_AR'],parameters['RF_UP'],parameters['HHRS']]):
        rf_qtp=float(parameters['RF_AR']) * float(parameters['RF_UP'])*float(parameters['HHRS'])/1000
    return {'RF_QTP': {'type': QVariant.Double, 'value': rf_qtp}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Transm. Heat Loss',
    extension_name='Roof Quality (QT, Present)',
    layer_name= 'QT Roof Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_QTP',
    source_type='none',
    par_in=['RF_AR','RF_UP','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_QTP'],
    description=u"Calculate the present Transmission Heat Loss of the Building's Roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
