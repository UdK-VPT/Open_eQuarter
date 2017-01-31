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

    achl = NULL
    if not oeq_global.isnull([parameters['LIV_AR']]):
        achl= 40 * parameters['LIV_AR'] #kWh/a
    return {'ACHL': {'type': QVariant.Double, 'value': achl}}


extension = OeQExtension(
    extension_id=__name__,

    category='Evaluation',
    subcategory='Building',
    extension_name='Air change heat loss',
    layer_name= 'Air change heat loss',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='ACHL',
    source_type='none',
    par_in=['LIV_AR'],
    sourcelayer_name=config.data_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    show_results=['ACHL'],
    description=u"Calculate Air Change Heat loss",
    evaluation_method=calculation)

extension.registerExtension(default=True)
