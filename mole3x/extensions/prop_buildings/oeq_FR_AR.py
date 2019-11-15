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
    # factor for golden rule

    fr_rt = NULL
    fr_ar = NULL
    if not oeq_global.isnull([parameters['YOC'] , parameters['HEIGHT'],parameters['AREA']]):

        if parameters['HEIGHT'] < 5:
            fr1= 1
        elif parameters['HEIGHT'] < 8:
            fr1 = 0
        elif parameters['HEIGHT'] < 33:
            fr1= 0.04 * (parameters['HEIGHT'] - 8)
        else:
            fr1 = 1

        if parameters['YOC'] < 1860:
            fr2=0
        elif parameters['YOC'] < 1960:
            fr2=0.01 * (parameters['YOC'] - 1860)
        else:
            fr2 = 1

        fr_rt = 0.5 * (fr1 + fr2)
        fr_ar = fr_rt * parameters['AREA']

    return {'FR_RT': {'type': QVariant.Double,
                    'value': fr_rt},
            'FR_AR': {'type': QVariant.Double,
                    'value': fr_ar}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='General',
    extension_name='Flat Roof Area',
    layer_name= 'Flat Roof Area',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='FR_RT',
    source_type='none',
    par_in=['HEIGHT','YOC','AREA'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['FR_RT'],
    description="Raw calculation of the flat area of the roof of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
