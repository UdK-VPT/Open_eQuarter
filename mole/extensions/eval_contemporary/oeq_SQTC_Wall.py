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
    from PyQt4.QtCore import QVariant
    wl_sqtp = NULL
    if not oeq_global.isnull([parameters['WL_UC'],parameters['HHRS']]):
        wl_sqtp= float(parameters['WL_UC'])*float(parameters['HHRS'])/1000
    return {'WL_SQTC': {'type': QVariant.Double, 'value': wl_sqtp}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Spec. Transm. Heat Loss',
    extension_name='Wall SpecTransm (SQT, Contemporary)',
    layer_name= 'SQT Wall Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_SQTC',
    source_type='none',
    par_in=['WL_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_SQTC'],
    description=u"Calculate the contemporary Transmission Heat Loss of the Building's baseplate per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
