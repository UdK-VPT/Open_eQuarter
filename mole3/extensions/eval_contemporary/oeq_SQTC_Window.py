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

    wn_sqtp = NULL
    if not oeq_global.isnull([parameters['WN_UC'],parameters['HHRS']]):
        wn_sqtp= float(parameters['WN_UC'])*float(parameters['HHRS'])/1000
    return {'WN_SQTC': {'type': QVariant.Double, 'value': wn_sqtp}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Spec. Transm. Heat Loss',
    extension_name='Window SpecTransm (SQT, Contemporary)',
    layer_name= 'SQT Window Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_SQTC',
    source_type='none',
    par_in=['WN_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_SQTC'],
    description="Calculate the contemporary Transmission Heat Loss of the Building's Windows per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
