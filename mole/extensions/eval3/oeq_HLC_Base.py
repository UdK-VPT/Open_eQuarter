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
    dataset = {'BS_QTC': NULL}
    dataset.update(parameters)

    print dataset['BS_AR']
    print dataset['BS_UC']
    print dataset['HHRS']

    dataset['BS_QTC']=float(dataset['BS_AR']) * float(dataset['BS_UC'])*0.6*float(dataset['HHRS'])/1000

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Base',
    extension_name='Base Quality (QT, Contemporary)',
    layer_name= 'QT Base Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='BS_QTC',
    source_type='none',
    par_in=['BS_AR','BS_UC','HHRS'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['BS_QTC'],
    description=u"Calculate the contemporary Transmission Heat Loss of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
