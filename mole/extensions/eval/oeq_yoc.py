# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    return {}


extension = OeQExtension(
    #extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Year of Construction',
    layer_name= 'Year of Construction',
    #extension_filepath=os.path.join(__file__),
    #colortable = os.path.join(__file__[:-3] + '.qml'),
    field_id='YOC',
    source_type='none',
    par_in=['YOC'],
    layer_in=config.data_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=['YOC'],
    description=u"Year of Construction",
    evaluation_method=calculation)

extension.registerExtension(default=True)
