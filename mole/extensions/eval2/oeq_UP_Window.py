# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import present_window_uvalue_AVG_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'YOC': NULL,'WN_UP':NULL}
    dataset.update(parameters)

    if not oeq_global.isnull(dataset['YOC']):
        #print str(dataset['YOC'])
        #print type(dataset['YOC'])
        #try:
        dataset['WN_UP']=present_window_uvalue_AVG_by_building_age_lookup.get(dataset['YOC'])
        #except:
        #    pass
    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='U-Values Present',
    extension_name='Window Quality (U_Value, Present)',
    layer_name= 'U Window Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WN_UP',
    source_type='none',
    par_in=['YOC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WN_UP'],
    description=u"Calculate the present U-Value of the Building's windoes",
    evaluation_method=calculation)

extension.registerExtension(default=True)
