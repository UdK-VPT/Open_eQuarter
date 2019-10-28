# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension

def calculation(self=None, parameters={},feature = None):
    return {}


extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='Dimensions',
    extension_name='Building Height',
    extension_type='display',
    layer_name= 'Building Height',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id= None,
    source_type='none',
    par_in=[],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['HEIGHT'],
    description=u"Height of Buildings",
    evaluation_method=calculation)

extension.registerExtension(default=True)
