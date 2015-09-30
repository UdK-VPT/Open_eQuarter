# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension

def calculation(self=None, parameters={}):
    return {}


extension = OeQExtension(
    #extension_id=__name__,
    category='Evaluation',
    subcategory='Dimensions',
    extension_name='Building Height',
    layer_name= 'Building Height',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='HEIGHT',
    source_type='none',
    par_in=['HEIGHT'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['HEIGHT'],
    description=u"Height of Buildings",
    evaluation_method=calculation)

extension.registerExtension(default=True)
