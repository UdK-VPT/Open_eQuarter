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

    wl_qtc = NULL
    if not oeq_global.isnull([parameters['WL_AR'],parameters['WL_UC'],parameters['HHRS']]):
        wl_qtc =float(parameters['WL_AR']) * float(parameters['WL_UC'])*float(parameters['HHRS'])/1000
    return {'WL_QTC': {'type': QVariant.Double, 'value': wl_qtc}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Transm. Heat Loss',
    extension_name='Wall Quality (QT, Contemporary)',
    layer_name= 'QT Wall Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_QTC',
    source_type='none',
    par_in=['WL_AR','WL_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_QTC'],
    description="Calculate the contemporary Transmission Heat Loss through the Building's wall",
    evaluation_method=calculation)

extension.registerExtension(default=True)
