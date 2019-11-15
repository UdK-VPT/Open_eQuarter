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
    bs_qtc = NULL
    if not oeq_global.isnull([parameters['BS_AR'],parameters['BS_UC'],parameters['HHRS']]):
        bs_qtc=float(parameters['BS_AR']) * float(parameters['BS_UC'])*float(parameters['HHRS'])/1000*0.35 #correction factor
    return {'BS_QTC': {'type': QVariant.Double, 'value': bs_qtc}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Transm. Heat Loss',
    extension_name='Base Quality (QT, Contemporary)',
    layer_name= 'QT Base Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='BS_QTC',
    source_type='none',
    par_in=['BS_AR','BS_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BS_QTC'],
    description="Calculate the contemporary Transmission Heat Loss of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
