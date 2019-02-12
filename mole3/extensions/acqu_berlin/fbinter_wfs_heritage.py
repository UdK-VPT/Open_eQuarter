# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config
from mole.oeq_global import OeQ_get_bld_id, isnull
from mole.qgisinteraction import legend
from qgis.PyQt import QtGui, QtCore

def load(self=None):
    self.load_wfs()
    return True


def preflight(self=None):
    from mole.project import config
    from qgis.PyQt.QtCore import QVariant
    from qgis.core import QgsField
    from mole.qgisinteraction.layer_interaction import add_attributes_if_not_exists
    from mole.oeq_global import OeQ_get_bld_id
    print("Heritage Preflight")
    layer = self.layer()
    #print layer.name()
    if layer == None:
        return False
    provider = layer.dataProvider()
    #in the Denkmalkarte there are two Features that describe the heritage state of a building. One is ID the other one TYPE
    #ID means the registration number of the building or area in the official heritage register of berlin
    #TYPE gives an information about wether the outline describes a heritage building (Baudenkmal), a heritage building group (Bereich_Ensemble) or a more general heritage area (Bereich_Gesamtanlage)
    #other heritage types will be ignored

    # remove irrelevant heritage features like "Gertendenkmal" or "Bodendenkmal"
    her_states = ['Baudenkmal','Bereich_Ensemble','Bereich_Gesamtanlage']
    to_remove =[]
    for i in layer.getFeatures():
        try:
            if (i['TYP'] not in her_states):
                to_remove.append(i.id())


        except:
            return False
    provider.deleteFeatures(to_remove)

    #add STATE Attribute
    add_attributes_if_not_exists(layer, [QgsField('STATE', QVariant.Int)])
    layer.updateFields()

    # classify the TYP for more international handling with numbers and save it in STATE
    # 1: heritage area
    # 2: heritage building group
    # 3: heritage building

    layer.startEditing()
    for i in layer.getFeatures():
        if (i['TYP'] == 'Baudenkmal'):
            i['STATE'] = 3
        elif (i['TYP'] == 'Bereich_Ensemble'):
            i['STATE'] = 2
        elif (i['TYP'] == 'Bereich_Gesamtanlage'):
            i['STATE'] = 1
        else:
            i['STATE'] = 0
        layer.updateFeature(i)
    layer.commitChanges()
    count=0

    #remove other attributes
    to_remove = []
    for field in provider.fields():
        if field.name() not in ['ID','STATE']:
            to_remove.append(count)
        count += 1

    provider.deleteAttributes(to_remove)
    layer.updateFields()

    return True

def evaluation(self=None, parameters={},feature=None):

    from qgis.PyQt.QtCore import QVariant
    from qgis.core import QgsDistanceArea, QgsCoordinateReferenceSystem
    herid = NULL
    herstate = NULL
    #layer = legend.nodeByName()[0].layer()
    if feature:
        herstate = 0
        herid = ''
        herits = self.sampleData(feature, field_list=['ID', 'STATE'], feature_crs = self.layer().crs())
        if herits != None:
            print(herits);
            for i in herits:
                if i['STATE'] > herstate:
                    herstate = i['STATE']  # necessary to safe dependency check
                    herid = i['ID']

    return {'HERIT_ID': {'type': QVariant.Int,
                           'value': herid},
            'HERIT_STAT': {'type': QVariant.String,
                           'value': herstate}}

def postflight(self=None):
    return True
    #return self.createDatabase()



import os
from mole.extensions import OeQExtension
from mole.project import config
extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WFS',
    extension_name='Building Heritage State (WFS)',
    extension_type='information',
    field_id='STATE',   #used for point sampling tool
    par_in= [],
    source_type='wfs',
    layer_name='Building Heritage State',
    sourcelayer_name=config.building_coordinate_layer_name,
    targetlayer_name=config.data_layer_name,
    active=True,
    description='Building Heritage State (WFS)',
    source='https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/sach_denkmal?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAME=fis:sach_denkmal&SRSNAME=urn:ogc:def:crs:EPSG:6.9:25833',
    source_crs='EPSG:25833',
    bbox_crs='EPSG:25833',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    load_method= load,
    preflight_method = preflight,
    evaluation_method= evaluation,
    postflight_method = None)

extension.registerExtension(default=True)

