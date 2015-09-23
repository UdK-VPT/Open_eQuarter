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
    dataset = {'YOC': NULL,'BS_UC':NULL}
    dataset.update(parameters)

    if not oeq_global.isnull(dataset['YOC']):
        print str(dataset['YOC'])
        print type(dataset['YOC'])
        #try:
        dataset['BS_UC']=contemporary_base_uvalue_by_building_age_lookup.get(dataset['YOC'])
        #except:
        #    pass
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='evaluation',
    extension_name='Base Quality (U_Value, Contemporary)',
    layer_name= 'Base Quality',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='BAS_UC',
    source_type='none',
    par_in=['YOC'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['BS_UC'],
    description=u"Calculate the U-Value of the Building's baseplate",
    evaluation_method=calculation)

extension.registerExtension(default=True)
