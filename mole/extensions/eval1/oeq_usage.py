# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import building_usage_type_by_alk_usage_id

def calculation(self=None, parameters={},feature = None):
    from scipy.constants import golden
    from math import floor, ceil
    from PyQt4.QtCore import QVariant
    bu_bt = NULL
    falk=str(int(parameters['FUNC_ALK']))

    if not oeq_global.isnull(falk):
        bu_bt=building_usage_type_by_alk_usage_id.get(falk)
        #print('falk:' falk)
    return bu_bt

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='General',
    extension_name='Building Usage',
    layer_name= 'Building Usage',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    #field_id= "BUI_USAGE",
    source_type='none',
    par_in= ['FUNC_ALK'],
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['BLD_USAGE'],
    description=u"Building Usage",
    evaluation_method=calculation)

extension.registerExtension(default=True)
