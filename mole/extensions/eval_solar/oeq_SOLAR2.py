# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import rb_contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={},feature = None):
    return {}


extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='Solarthermics',
    extension_name='Solar Heat Earning per Living Area',
    layer_name= 'Solar Heat Earning (per Living Area)',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='SOLHEL',
    source_type='none',
    par_in= [],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['SOLHEL'],
    description=u"Calculation of the Solar Heat Earning",
    evaluation_method=calculation)

extension.registerExtension(default=True)
