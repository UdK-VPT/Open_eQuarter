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
    dataset = {'RF_QTC': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['RF_AR'],dataset['RF_UC'],dataset['HHRS']]):
        dataset['RF_QTC']=float(dataset['RF_AR']) * float(dataset['RF_UC'])*float(dataset['HHRS'])/1000

    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Contemp. Transm. Heat Loss',
    extension_name='Roof Quality (QT, Contemporary)',
    layer_name= 'QT Roof Contemporary',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_QTC',
    source_type='none',
    par_in=['RF_AR','RF_UC','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_QTC'],
    description=u"Calculate the Contemporary Transmission Heat Loss of the Building's roof",
    evaluation_method=calculation)

extension.registerExtension(default=True)
