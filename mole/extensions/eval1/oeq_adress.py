# -*- coding: utf-8 -*-

import os,math
from qgis.core import NULL
from mole import oeq_global
from mole.project import config
from mole.extensions import OeQExtension
from mole.stat_corr import contemporary_base_uvalue_by_building_age_lookup

def calculation(self=None, parameters={}):
    from PyQt4.QtCore import QVariant
    result = {}
    for i in ['BLD_LON1','BLD_LAT1','BLD_LON2','BLD_LAT2']:
        result.update({i: {'type': QVariant.Double,
                           'value': parameters[i]}})
    for i in ['BLD_NUM','BLD_STR','BLD_COD','BLD_CTY','BLD_CTR']:
        result.update({i: {'type': QVariant.String,
                           'value': parameters[i]}})
    result.update({'BLD_CRS': {'type': QVariant.Int,
                       'value': parameters['BLD_CRS']}})
    return result

extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Building Adress',
    layer_name= 'Building Adress',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    field_id='ADRESS',
    source_type='none',
    par_in=['BLD_LON1','BLD_LAT1','BLD_LON2','BLD_LAT2','BLD_CRS','BLD_NUM','BLD_STR','BLD_COD','BLD_CTY','BLD_CTR'],
    layer_in=config.pst_output_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    show_results=None,
    description=u"Building Adress",
    evaluation_method=calculation)

extension.registerExtension(default=True)
