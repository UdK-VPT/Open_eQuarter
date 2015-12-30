# -*- coding: utf-8 -*-

from qgis.core import NULL
from mole.project import config

def calculation(self=None, parameters={}):
    from qgis.core import QgsVectorLayer
    from qgis.utils import iface
    from mole.project import config
    from mole import oeq_global
    from mole.qgisinteraction import plugin_interaction,layer_interaction
    #self.load_wms()
    #run point sampling tool
    #psti = plugin_interaction.PstInteraction(iface, config.pst_plugin_name)
    #psti.set_input_layer(config.pst_input_layer_name)
    #abbreviations = psti.select_and_rename_files_for_sampling()
    #pst_output_layer = psti.start_sampling(oeq_global.OeQ_project_path(), config.pst_output_layer_name)
    #vlayer = QgsVectorLayer(pst_output_layer, config.pst_output_layer_name,"ogr")
    #layer_interaction.add_layer_to_registry(vlayer)
    from mole import oeq_global
    result = self.decode_color(parameters['FLRS_R'],
                             parameters['FLRS_G'],
                             parameters['FLRS_B'],
                             parameters['FLRS_a'],
                             ['FLOORS'],
                             mode='average')
    #print result['FLOORS']['value']
    if oeq_global.isnull(result['FLOORS']['value']):
        result['FLOORS']['value'] = 3.5
    return result



import os
from mole.extensions import OeQExtension

extension = OeQExtension(
    extension_id=__name__,
    category='Import',
    subcategory='WMS',
    extension_name='Floors (ALK, WMS)',
    field_id='FLRS',   #used for point sampling tool
    par_in=['FLRS_R','FLRS_G','FLRS_B','FLRS_a'],
    source_type='wms',
    layer_name='Floors (WMS Capture)',
    layer_in=config.pst_output_layer_name,
    layer_out=config.data_layer_name,
    active=True,
    description=u'',
    source='crs=EPSG:4326&dpiMode=7&format=image/png&layers=2&styles=&url=http://fbinter.stadt-berlin.de/fb/wms/senstadt/alk_gebaeude',
    source_crs='EPSG:4326',
    extension_filepath=os.path.join(__file__),
    colortable = os.path.join(os.path.splitext(__file__)[0] + '.qml'),
    evaluation_method=calculation)

extension.registerExtension(default=True)
