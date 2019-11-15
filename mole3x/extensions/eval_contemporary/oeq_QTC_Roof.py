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
    rf_qtc = NULL
    if not oeq_global.isnull([parameters['RF_AR'],parameters['RF_UC'],parameters['HHRS']]):
        rf_qtc=float(parameters['RF_AR']) * float(parameters['RF_UC'])*float(parameters['HHRS'])/1000
    return {'RF_QTC': {'type': QVariant.Double, 'value': rf_qtc}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Transm. Heat Loss',
    extension_name='Roof Quality (QT, Contemporary)',
    layer_name= 'QT Roof Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_QTC',
    source_type='none',
    par_in=['RF_AR','RF_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_QTC'],
    description="Calculate the Contemporary Transmission Heat Loss of the Building's roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
