# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from mole.oeq_global import OeQ_get_bld_id, isnull


def load(self=None):
    from mole.extensions import by_layername
    if bool(by_layername(config.building_outline_layer_name)[0].createDatabase()):
        return True
    return False


def preflight(self=None):
    from mole.project import config
    from qgis.PyQt.QtCore import QVariant
    from qgis.core import QgsField
    from mole.qgisinteraction.layer_interaction import add_attributes_if_not_exists
    from mole.oeq_global import OeQ_get_bld_id
    layer = self.layer()
    provider = layer.dataProvider()
    #fields = filter(lambda f: f.name() not in [config.building_id_key,u'AREA',u'PERIMETER'], provider.fields())
    fields = [f for f in provider.fields() if f.name() != config.building_id_key]
    fieldnames =[field.name() for field in fields]
    to_remove = []
    count = 0
    for field in provider.fields():
        if field.name() in fieldnames:
            to_remove.append(count)
        count += 1
    provider.deleteAttributes(to_remove)
    layer.updateFields()
    return True

def evaluation(self=None, parameters={},feature=None):
    return []

def postflight(self=None):
    return True



import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='',
    subcategory='',
    extension_name='Database Creator',
    extension_type='basic',
    field_id='',   #used for point sampling tool
    par_in= [], #[config.building_id_key,'AREA','PERIMETER'],
    #par_out=[config.building_id_key,'AREA','PERIMETER'],
    source_type='',
    layer_name=config.data_layer_name,
    sourcelayer_name=config.building_outline_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    description='',
    source= None,
    source_crs='',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method= load,
    preflight_method = preflight,
    evaluation_method= None,
    postflight_method = None)

extension.registerExtension(default=True)
