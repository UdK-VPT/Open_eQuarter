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

    rf_sqtp = NULL
    if not oeq_global.isnull([parameters['RF_UP'],parameters['HHRS']]):
        rf_sqtp= float(parameters['RF_UP'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'RF_SQTP': {'type': QVariant.Double, 'value': rf_sqtp}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Spec. Transm. Heat Loss',
    extension_name='Roof SpecTransm (SQT, Present)',
    layer_name= 'SQT Roof Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_SQTP',
    source_type='none',
    par_in=['RF_UP','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_SQTP'],
    description="Calculate the present Transmission Heat Loss of the Building's Roof per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
