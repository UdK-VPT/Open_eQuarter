# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import building_usage_by_alk_usage_id

def calculation(self=None, parameters={},feature = None):
    from qgis.PyQt.QtCore import QVariant


    return {'GKN_ALK':{'type': QVariant.String,
                        'value': parameters['GKN_ALK']}}

extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='General',
    extension_name='Building GKN',
    layer_name= 'Building GKN',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    #field_id= "BUI_USAGE",
    source_type='none',
    par_in= ['GKN_ALK'],
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    #show_results=[],
    description="Building GKN",
    evaluation_method=calculation)

extension.registerExtension(default=True)
