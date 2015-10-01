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
    dataset = {'WL_SQTC': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['WL_UC'],dataset['HHRS']]):
        dataset['WL_SQTC']= float(dataset['WL_UC'])*float(dataset['HHRS'])/1000

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Wall',
    extension_name='Wall SpecTransm (SQT, Contemporary)',
    layer_name= 'SQT Wall Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='WL_SQTC',
    source_type='none',
    par_in=['WL_UC','HHRS'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['WL_SQTC'],
    description=u"Calculate the contemporary Transmission Heat Loss of the Building's baseplate per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
