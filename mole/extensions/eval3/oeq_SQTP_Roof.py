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
    dataset = {'RF_SQTP': NULL}
    dataset.update(parameters)

    if not oeq_global.isnull([dataset['RF_UP'],dataset['HHRS']]):
        dataset['RF_SQTP']= float(dataset['RF_UP'])*float(dataset['HHRS'])/1000 *0.35 #correction factor


    result = {}
    for i in dataset.keys():
        result.update({i: {'type': QVariant.Double,
                           'value': dataset[i]}})
    return result

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Present Spec. Transm. Heat Loss',
    extension_name='Roof SpecTransm (SQT, Present)',
    layer_name= 'SQT Roof Present',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='RF_SQTP',
    source_type='none',
    par_in=['RF_UP','HHRS'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['RF_SQTP'],
    description=u"Calculate the present Transmission Heat Loss of the Building's Roof per m2",
    evaluation_method=calculation)

extension.registerExtension(default=True)
