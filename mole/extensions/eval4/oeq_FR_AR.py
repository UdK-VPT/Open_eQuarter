# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule


    if not oeq_global.isnull([parameters['YOC'] , parameters['HEIGHT'],parameters['AREA']]):

        if parameters['HEIGHT'] < 8:
            fr1=0
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

        flatroofratio = 0.5 * (fr1 + fr2)


        return {'FR_RT': {'type': QVariant.Double,
                               'value': flatroofratio},
                'FR_AR': {'type': QVariant.Double,
                               'value': flatroofratio * parameters['AREA']}}

    return {'FR_RT': {'type': QVariant.Double,
                    'value': NULL},
            'FR_AR': {'type': QVariant.Double,
                    'value': NULL}}


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
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['FR_RT'],
    description=u"Calculate the flat area of the roof of the Building",
    evaluation_method=calculation)

extension.registerExtension(default=True)
