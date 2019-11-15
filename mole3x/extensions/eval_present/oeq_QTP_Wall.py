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

    wl_qtp = NULL
    if not oeq_global.isnull([parameters['WL_AR'],parameters['WL_UP'],parameters['HHRS']]):
        wl_qtp=float(parameters['WL_AR']) * float(parameters['WL_UP'])*float(parameters['HHRS'])/1000
    return {'WL_QTP': {'type': QVariant.Double, 'value': wl_qtp}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Transm. Heat Loss',
    extension_name='Wall Quality (QT, Present)',
    layer_name= 'QT Wall Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_QTP',
    source_type='none',
    par_in=['WL_AR','WL_UP','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_QTP'],
    description="Calculate the present Transmission Heat Loss of the Building's Walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
