# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_wall_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'YOC': NULL,'WL_UC':NULL}
    dataset.update(parameters)

    if not oeq_global.isnull(dataset['YOC']):
        #print str(dataset['YOC'])
        #print type(dataset['YOC'])
        #try:
        dataset['WL_UC']=contemporary_wall_uvalue_by_building_age_lookup.get(dataset['YOC'])
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
    subcategory='U-Values Contemporary',
    extension_name='Wall Quality (U_Value, Contemporary)',
    layer_name= 'U Wall (Contemporary)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='WL_UC',
    source_type='none',
    par_in=['YOC'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['WL_UC'],
    description=u"Calculate the contemporary U-Value of the Building's walls",
    evaluation_method=calculation)

extension.registerExtension(default=True)
