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

    bs_sqtph= NULL
    if not oeq_global.isnull([parameters['BS_UPH'],parameters['HHRS']]):
        bs_sqtph= float(parameters['BS_UPH'])*float(parameters['HHRS'])/1000 *0.35 #correction factor
    return {'BS_SQTPH': {'type': QVariant.Double, 'value': bs_sqtph}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Heritage Spec. Transm. Heat Loss',
    extension_name='Base SpecTransm (SQT, Present Heritage)',
    layer_name= 'SQT Base Present Heritage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_SQTPH',
    source_type='none',
    par_in=['BS_UPH','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_SQTPH'],
    description="Calculate the present heritage Transmission Heat Loss of the Building's baseplate per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
