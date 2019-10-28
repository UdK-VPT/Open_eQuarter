# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from mole.oeq_global import OeQ_get_bld_id, isnull


def load(self=None):
    return True


def preflight(self=None):
    return True

def evaluation(self=None, parameters={},feature=None):
    from PyQt4.QtCore import QVariant
    if bool(feature) & bool(parameters[u'FLRS_ALK']):
        return {self.field_id: {'type': QVariant.Double,'value': parameters[u'FLRS_ALK']}}
    else:
        return {self.field_id: {'type': QVariant.Double, 'value': config.default_number_of_floors}}

def postflight(self=None):
    return True
    #return self.createDatabase()



import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='Evaluation',
    subcategory='General',
    extension_name='Floors (ALK, WFS)',
    extension_type='basic',
    field_id='FLOORS',   #used for point sampling tool
    par_in= [u'FLRS_ALK'], #[config.building_id_key,'AREA','PERIMETER'],
    #par_out=[config.building_id_key,'AREA','PERIMETER'],
    source_type='none',
    layer_name='Floors (ALK Capture)',
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.data_layer_name,#config.data_layer_name,
    active=True,
    description=u'',
    source=None,
    source_crs=None,
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    show_results=None,
    load_method= None,
    preflight_method = None,
    evaluation_method= evaluation,
    postflight_method = None)

extension.registerExtension(default=True)
