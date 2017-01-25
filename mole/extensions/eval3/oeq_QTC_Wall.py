# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    # factor for golden rule
    dataset = {'WL_QTC': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['WL_AR'],dataset['WL_UC'],dataset['HHRS']]):
        dataset['WL_QTC']=float(dataset['WL_AR']) * float(dataset['WL_UC'])*float(dataset['HHRS'])/1000

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


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
    description=u"Calculate the contemporary Transmission Heat Loss through the Building's wall",
    evaluation_method=calculation)

extension.registerExtension(default=True)
