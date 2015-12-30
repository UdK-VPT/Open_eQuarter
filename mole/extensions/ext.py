# -*- coding: utf-8 -*-

import os,time,datetime
import pickle
from mole import oeq_global
from mole.project import config
from mole.qgisinteraction import legend
from qgis.core import QgsVectorJoinInfo

def average(self=None, parameters={}):
 #   print parameters
    from PyQt4.QtCore import QVariant
    from qgis.core import NULL
    result = {self.field_id + '_P': {'type': QVariant.String,
                                     'value': self.layer_name},
              self.field_id + '_M': {'type': QVariant.Double,
                                     'value': NULL}}
    if parameters != {}:
        # print sum(float(parameters.values()))/len(parameters)
        try:
            result[self.field_id + '_M']['value'] = sum([float(i) for i in parameters.values()]) / len(parameters)
        except:
            pass

    return result




class OeQExtension:
    def __init__(self, category=None,
                 subcategory = None,
                 field_id=None,
                 extension_id=None,
                 extension_name=None,
                 extension_filepath = None,
                 layer_name = None,
                 layer_id=None,
                 description='Extention Details',
                 source_type=None,
                 active=False,
                 source=None,
                 source_crs=None,
                 par_in=None,
                 layer_in=None,
                 par_out=None,
                 layer_out=None,
                 colortable=None,
                 show_results=False,
                 evaluation_method=average,
                 last_calculation=None):
        self.field_id = field_id
        self.source_type = source_type
        if extension_id == None:
            self.extension_id = 'userdefined_' + str(OeQExtension.generic_id_cnt)
            OeQExtension.generic_id_cnt += 1
        else:
            self.extension_id = extension_id
        if layer_name == None:
            self.layer_name = extension_id
        else:
            self.layer_name = layer_name
        if extension_name == None:
            if self.source_type == None:
                self.extension_name = layer_name + ' (Unknown)'
            else:
                self.extension_name = layer_name + ' (' + source_type.upper() + ')'
        else:
            self.extension_name = extension_name
        self.extension_filepath = extension_filepath
        self.category = category
        self.subcategory = subcategory
        self.layer_id = layer_id
        self.description = description
        self.type = type
        self.source = source
        self.source_crs = source_crs
        self.active = active
        self.show_results = show_results
        self.evaluator = evaluation_method
        if par_in == None:
            self.par_in = [field_id + '_L', field_id + '_H']
        else:
            self.par_in = par_in
        if layer_in == None:
            self.layer_in = config.pst_output_layer_name
        else:
            self.layer_in = layer_in
        if par_out == None:
            self.par_out = self.get_par_out()
        else:
            self.par_out = par_out
        if layer_out == None:
            self.layer_out = config.data_layer_name
        else:
            self.layer_out = layer_out
        #if colortable != None:
        #     if not os.path.exists(colortable):
        #        colortable = None
        #     elif not os.path.isfile(colortable):
        #        colortable = None
        self.colortable = colortable
        self.last_calculation = last_calculation


    def update(self, category=None,
               subcategory = None,
               field_id=None,
               extension_id=None,
               extension_name=None,
               extension_filepath=None,
               layer_name=None,
               layer_id=None,
               description='Extention Details',
               source_type=None,
               active=None,
               source=None,
               source_crs=None,
               par_in=None,
               layer_in=None,
               par_out=None,
               layer_out=None,
               show_results=None,
               colortable=None,
               evaluation_method=None,
               last_calculation=None):
        if category != None: self.category = category
        if subcategory != None: self.subcategory = subcategory
        if field_id != None: self.field_id = field_id
        if extension_id != None: self.extension_id = extension_id
        if extension_name != None: self.extension_name = extension_name
        if extension_filepath != None: self.extension_filepath = extension_filepath
        if layer_name != None: self.layer_name = layer_name
        if layer_id != None: self.layer_id = layer_id
        if description != None: self.description = description
        if source_type != None: self.source_type = source_type
        if active != None: self.active = active
        if source != None: self.source = source
        if source_crs != None: self.source_crs = source_crs
        if par_in != None: self.par_in = par_in
        if layer_in != None: self.layer_in = layer_in
        if par_out != None: self.par_out = par_out
        if layer_out != None: self.layer_out = layer_out
        if colortable != None: self.colortable = colortable
        if show_results != None: self.show_results = show_results
        if evaluation_method != None: self.evaluator = evaluation_method
        if last_calculation != None: self.last_calculation = last_calculation

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def registerExtension(self, default=False):
        from mole.oeq_global import OeQ_ExtensionRegistry, OeQ_ExtensionDefaultRegistry
        # if self.category == 'Import':
        #    OeQ_ImportExtensionRegistry.append(self)
        # elif self.category == 'export':
        #      OeQ_ExportExtensionRegistry.append(self)
        # elif self.category == 'evaluation':

        if default:
            OeQ_ExtensionDefaultRegistry.append(self)
        else:
            OeQ_ExtensionRegistry.append(self)


    def evaluate(self, parameter):
        if self.evaluator == None:
            return {}
        return self.evaluator(self, parameter)


    def dummy_par(self):
        return dict(zip(self.par_in, [1 for i in self.par_in]))

    def get_par_out(self):
        if self.par_in == None:
            return {}
        return self.evaluate(dict(zip(self.par_in, [1 for i in self.par_in]))).keys()

    def get_par_out_not_in(self):
        return filter(lambda par: not (par in self.par_in), self.get_par_out())

    def par_out_as_attributes(self):
        from qgis.core import QgsField
        eval_out = self.evaluate(dict(zip(self.par_in, [1 for i in self.par_in])))
        attributes = []
        for i in eval_out.keys():
            attributes.append(QgsField(i, eval_out[i]['type']))
        return attributes

    def default_colortable(self):
        defcolortable = by_extension_id(self.extension_id, registry=oeq_global.OeQ_ExtensionDefaultRegistry)
      #  print defcolortable
        if defcolortable:
            #print defcolortable[0].colortable
            return defcolortable[0].colortable
        return None

    def update_colortable(self, overwrite=False):
        from shutil import copyfile
        ct_default = self.default_colortable()
        if (not ct_default):
            self.colortable = None
        elif not oeq_global.OeQ_project_saved():
            self.colortable = ct_default
        else:
            ct_default = os.path.join(ct_default)
            ct_project = os.path.join(oeq_global.OeQ_project_path(), self.layer_name+'.qml')
         #   print "Copy from"
         #   print ct_default
         #   print "To"
         #   print ct_project
            if overwrite:
                try:
                    os.remove(ct_project)
                except:
                    pass
            #try:
            if os.path.exists(ct_default):
                copyfile(ct_default, ct_project)
            #except:
            #        pass
            if os.path.exists(ct_project):
                self.colortable = ct_project
            else:
                self.colortable = None
        return self.colortable


    def inspect(self):
        attrs = ['extension_name', 'extension_id', 'description', 'layer_name', 'layer_id', 'category', 'source',
                 'source_type', 'colortable', 'field_id', 'par_in', 'par_out', 'layer_out', 'layer_in', 'active']
        for i in attrs:
            j = getattr(self, i)
            if type(j) == type(u''):
                j = 'unicode ' + j.encode('utf-8')



    def load_wms(self,capture=True):
        from qgis.core import QgsRasterLayer,QgsMapLayerRegistry
        from mole.oeq_global import OeQ_wait_for_renderer
        from mole.qgisinteraction.wms_utils import save_wms_extent_as_image
        from mole.qgisinteraction import layer_interaction
        #init progressbar
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                              u'Loading WMS-Map "' + self.layer_name + '"!',
                                                              maxcount=3)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        wmslayer='WMS_'+self.layer_name+'_RAW'
        rlayer = QgsRasterLayer(self.source, wmslayer, self.source_type)
        QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        if not OeQ_wait_for_renderer(60000):
            oeq_global.OeQ_push_warning(self.extension_id + ':','Loading Data timed out!')
            return False
        #push progressbar
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        path = save_wms_extent_as_image(wmslayer)
        try:
            layer_interaction.remove_layer(rlayer,physical=True)
        except:
            pass

        #push progressbar
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        rlayer = QgsRasterLayer(path, self.layer_name)
        QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        #close progressbar
        if not OeQ_wait_for_renderer(60000):
            oeq_global.OeQ_push_warning(self.extension_id + ':','Reloading WMS-Capture timed out!')
            return False
        oeq_global.OeQ_pop_progressbar(progressbar)
        wmsnode=legend.nodeByLayer(rlayer)[0]
        #oeq_global.OeQ_wait(1)

        if self.category:
            if not legend.nodeExists(self.category):
                cat=legend.nodeCreateGroup(self.category)
            else:
                cat=legend.nodeByName(self.category)[0]
            legend.nodeHide(cat)
            #oeq_global.OeQ_wait(0.2)
            #create subcategory group in legend
            if self.subcategory:
                if not legend.nodeExists(self.subcategory):
                    subcat=legend.nodeCreateGroup(self.subcategory,'bottom',cat)
                else:
                    subcat=legend.nodeByName(self.subcategory)[0]
                legend.nodeHide(subcat)
                #oeq_global.OeQ_wait(0.2)
                wmsnode=legend.nodeMove(wmsnode,'bottom',subcat)
                #oeq_global.OeQ_wait(0.2)
                legend.nodeCollapse(subcat)
            else:
                wmsnode=legend.nodeMove(wmsnode,'bottom',cat)
                #.OeQ_wait(0.2)
                legend.nodeCollapse(cat)
        return wmsnode.layer()



    def load_wfs(self,extent=None):
        import os
        from mole.project import config
        from mole import oeq_global
        from mole.qgisinteraction import legend,layer_interaction
        from qgis.core import QgsVectorLayer,QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsVectorFileWriter
        from qgis.utils import iface
        #check whether extent is defined, if not use investigationarea extent
        if not extent:
            extent= legend.nodeGetExtent(config.investigation_shape_layer_name)

        #init progressbar
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                              u'Loading WFS-Map "' + self.layer_name + '"!',
                                                              maxcount=3)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        #get crs objects
        crsSrc=QgsCoordinateReferenceSystem(int(config.default_extent_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        crsDest=QgsCoordinateReferenceSystem(int(self.source_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        #transform extent
        coord_transformer = QgsCoordinateTransform(crsSrc, crsDest)
        extent = coord_transformer.transform(extent)
        #load wfs
        wfsLayer=QgsVectorLayer(self.source + '&BBOX='+str(extent.xMinimum())+','+str(extent.yMinimum())+','+str(extent.xMaximum())+','+str(extent.yMaximum()),self.layer_name,'ogr')

        #push progressbar
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        if not wfsLayer.isValid():
            oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":', u'Could not load WFS-Map "' + self.source + '"!')
            return None

        wfsfilepath = os.path.join(oeq_global.OeQ_project_path(),self.layer_name+'.shp')
        QgsVectorFileWriter.writeAsVectorFormat( wfsLayer,wfsfilepath,'System',wfsLayer.crs(),'ESRI Shapefile')
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #oeq_global.OeQ_wait_for_file(wfsfilepath)
        wfsLayer = iface.addVectorLayer(wfsfilepath,self.layer_name, 'ogr')
        if not oeq_global.OeQ_wait_for_renderer(60000):
            oeq_global.OeQ_push_warning(self.extension_id + ':','Loading Data timed out!')
            return False
        if not wfsLayer.isValid():
            oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":', u'Could not add WFS-Map "' + self.layer_name + ' to Legend"!')
            return None
        wfsnode=legend.nodeByLayer(wfsLayer)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        if not wfsnode:
            oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":', u'Could not find WFS-Map "' + self.layer_name + ' in Legend"!')
            return None
        wfsnode=wfsnode[0]
        wfsnode=legend.nodeConvertCRS(wfsnode,config.default_extent_crs)
        if not wfsnode:
            oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":', u'Could not convert CRS of WFS-Map "' + self.layer_name + '"!')
            return None

        oeq_global.OeQ_pop_progressbar(progressbar)
        if self.category:
            if not legend.nodeExists(self.category):
                cat=legend.nodeCreateGroup(self.category)
            else:
                cat=legend.nodeByName(self.category)[0]
            #legend.nodeHide(cat)
            #create subcategory group in legend
            if self.subcategory:
                if not legend.nodeExists(self.subcategory):
                    subcat=legend.nodeCreateGroup(self.subcategory,'bottom',cat)
                else:
                    subcat=legend.nodeByName(self.subcategory)[0]
                #legend.nodeHide(subcat)
                wfsnode=legend.nodeMove(wfsnode,'bottom',subcat)
                legend.nodeCollapse(subcat)
            else:
                wfsnode=legend.nodeMove(wfsnode,'bottom',cat)
                legend.nodeCollapse(cat)
                legend.nodeHide(cat)
        return wfsnode.layer()



    '''

def convert_crs
import processing
input = legend.nodeByName('Floors (WMS Capture)')[0].layer().source()
mask= legend.nodeByName('Investigation Area')[0].layer().source()
output=input.split('.')[0]+'_tmp.'+ input.split('.')[1]
processing.runalg('gdalogr:cliprasterbymasklayer', input, mask, 'none', False, False, '', output)
processing.load(output)



import mole.extensions as ext
ext.by_type('wms')[0].load_wms()




layer = iface.activeLayer()

extent = layer.extent()
width, height = layer.width(), layer.height()
renderer = layer.renderer()
provider=layer.dataProvider()
crs = layer.crs().toWkt()

pipe = QgsRasterPipe()
pipe.set(provider.clone())
pipe.set(renderer.clone())

file_writer = QgsRasterFileWriter('/Users/wk/Tresors/VPT/Open eQuarter/QGIS/output2.tif')

file_writer.writeRaster(pipe,
                        width,
                        height,
                        extent,
                        layer.crs())
    '''






    '''
    #generate_building id and get area and perimeters
    def complete_outlines(self):
        from qgis import utils
        from qgis.core import NULL
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant

        result = {'BLD_ID': {'type': QVariant.String,'value': NULL},
                'AREA': {'type': QVariant.Double,'value': NULL},
                'PERIMETER']: {'type': QVariant.Double,'value': NULL}}

        #read colormap
        try:
            oeqMain = utils.plugins['mole']
        except:
            print self.extension_id + ".decode_color(): Could not connect to Colormanager"
            return result

        color_dict = oeqMain.color_picker_dlg.color_entry_manager.read_color_map_from_qml(self.colortable)
        #check every color for match
        for color_key in color_dict.keys():
            #extract color map entry
            color_quadriple = color_key[5:-1].split(',')
            color_quadriple = map(int, color_quadriple)

            #check if color matches
            match = (((color_quadriple[0]-config.color_match_tolerance) < red < (color_quadriple[0]+config.color_match_tolerance))
                    and ((color_quadriple[1]-config.color_match_tolerance) < green < (color_quadriple[1]+config.color_match_tolerance))
                    and ((color_quadriple[2]-config.color_match_tolerance) < blue < (color_quadriple[2]+config.color_match_tolerance))
                    and ((color_quadriple[3]-config.color_match_tolerance) < alpha < (color_quadriple[3]+config.color_match_tolerance)))

            #set generic result to mapped values and return
            if match:
                if mode == 'average':
                    result[resultkeys[0]]['value'] = (float(color_dict[color_key][1]) + float(color_dict[color_key][2])) / 2
                else:
                    result[resultkeys[0]]['value'] = color_dict[color_key][0]
                    result[resultkeys[1]]['value'] = color_dict[color_key][1]
                    result[resultkeys[2]]['value'] = color_dict[color_key][2]
                return result

        #return generic result
        return result
    '''

    #decode RGBa color by the colormap
    def decode_color(self, red = 0 ,green = 0 ,blue = 0 ,alpha = 0 ,resultkeys = [], mode = 'range'):
        from qgis import utils
        from qgis.core import NULL
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant

        #define generic result
        if mode == 'average':
            if not resultkeys: resultkey = ['AvgVal']
            result = {resultkeys[0] + '': {'type': QVariant.Double,'value': NULL}}

        else:
            if not resultkeys: resultkey = ['Name','MinVal','MaxVal']
            result = {resultkeys[0]: {'type': QVariant.String,'value': NULL},
                      resultkeys[1]: {'type': QVariant.Double,'value': NULL},
                      resultkeys[2]: {'type': QVariant.Double,'value': NULL}}

        #read colormap
        try:
            oeqMain = utils.plugins['mole']
        except:
            print self.extension_id + ".decode_color(): Could not connect to Colormanager"
            return result

        color_dict = oeqMain.color_picker_dlg.color_entry_manager.read_color_map_from_qml(self.colortable)
        #check every color for match
        for color_key in color_dict.keys():
            #extract color map entry
            color_quadriple = color_key[5:-1].split(',')
            color_quadriple = map(int, color_quadriple)

            #check if color matches
            match = (((color_quadriple[0]-config.color_match_tolerance) < red < (color_quadriple[0]+config.color_match_tolerance))
                    and ((color_quadriple[1]-config.color_match_tolerance) < green < (color_quadriple[1]+config.color_match_tolerance))
                    and ((color_quadriple[2]-config.color_match_tolerance) < blue < (color_quadriple[2]+config.color_match_tolerance))
                    and ((color_quadriple[3]-config.color_match_tolerance) < alpha < (color_quadriple[3]+config.color_match_tolerance)))

            #set generic result to mapped values and return
            if match:
                if mode == 'average':
                    result[resultkeys[0]]['value'] = (float(color_dict[color_key][1]) + float(color_dict[color_key][2])) / 2
                else:
                    result[resultkeys[0]]['value'] = color_dict[color_key][0]
                    result[resultkeys[1]]['value'] = color_dict[color_key][1]
                    result[resultkeys[2]]['value'] = color_dict[color_key][2]
                return result

        #return generic result
        return result



    # extensions.by_category('Import')[1].decode_color_table()
    def decode_color_table(self):
        from qgis import utils
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant
        from mole.qgisinteraction.layer_interaction import add_attributes_if_not_exists, \
            colors_match_feature
        oeqMain = utils.plugins['mole']
        source_layer = legend.nodeByName(self.layer_in)
        if not source_layer:
            print "layer not found in decode color table"
            print source_layer
            return
        source_layer = source_layer[0]
        legend.nodeStoreVisibility(source_layer)
        legend.nodeShow(source_layer)
        #time.sleep(0.5)
        source_layer = source_layer.layer()
        source_provider = source_layer.dataProvider()
        if self.source_type == 'wms':
            if self.colortable != None:
                oeqMain.color_picker_dlg.color_entry_manager.read_color_map_from_qml(self.colortable)
                color_dict = oeqMain.color_picker_dlg.color_entry_manager.layer_values_map[self.layer_name]

                progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                              u'Decoding colors in "' + self.layer_in + '"!',
                                                              maxcount=len(color_dict) * source_layer.featureCount())
                progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)
            #    print color_dict
                for color_key in color_dict.keys():
                    color_quadriple = color_key[5:-1].split(',')
                    color_quadriple = map(int, color_quadriple)

                    attributes = [QgsField(self.field_id + '_P', QVariant.String),
                                  QgsField(self.par_in[0], QVariant.Double),
                                  QgsField(self.par_in[1], QVariant.Double)]

                    add_attributes_if_not_exists(source_layer, attributes)

                    for feat in source_provider.getFeatures():
                        # progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
                        if colors_match_feature(color_quadriple, feat, self.field_id):
                            result = {self.field_id + '_P': {'type': QVariant.String,
                                                             'value': color_dict[color_key][0]},
                                      self.par_in[0]: {'type': QVariant.Double,
                                                       'value': color_dict[color_key][1]},
                                      self.par_in[1]: {'type': QVariant.Double,
                                                       'value': color_dict[color_key][2]}}

                            attributevalues = {}
                            for i in result.keys():
                                attributevalues.update({source_provider.fieldNameIndex(i): result[i]['value']})

                            source_provider.changeAttributeValues({feat.id(): attributevalues})
                        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
                oeq_global.OeQ_pop_progressbar(progressbar)
        legend.nodeRestoreVisibility(self.layer_in)
        #time.sleep(0.5)


    def required(self):
        from qgis.core import QgsMessageLog
        req=[]
        all_suppliers=filter(lambda ext: ext != self, by_state(True))
        #if self.category != 'Import':
        if True:
            for ipar in self.par_in:
                supplier = filter(lambda ext: ipar in ext.get_par_out_not_in(), all_suppliers)
                if supplier:
                    if not (supplier[0] in req):
                        #print supplier[0].extension_id
                        req.insert(0, supplier[0])
                else:
                    QgsMessageLog.logMessage('Can not find a supplier found for "'+str(ipar)+'"','Warning in '+str(self.extension_id) + ':', QgsMessageLog.CRITICAL)
                    #oeq_global.OeQ_push_warning(str(self.extension_id) + ':','can not find a supplier found for "'+str(ipar)+'"')
        #print self.extension_id + ' needs:'
        #print [e.extension_id for e in req]
        return req

    def needs_evaluation(self,required=None):
        from mole.qgisinteraction import legend
        if not required:
            required = self.required()
        if not self.last_calculation:
            self.last_calculation=None
            return True
        if (self.show_results!=None) & (not legend.nodeExists(self.layer_name)):
            self.last_calculation=None
            return True

        outnode=legend.nodeByName(self.layer_out)
        if outnode:
            outlayer=outnode[0].layer()
            for par in self.get_par_out():
                if outlayer.fieldNameIndex(par)<0:
                    self.last_calculation=None
                    return True
        for ext in required:
            if ext.last_calculation:
                if self.last_calculation < ext.last_calculation:
                    self.last_calculation=None
                    return True
        return False


    def needs_needle_request(self,required=None):
        if not required:
            required = self.required()
        if not self.last_calculation:
            return True
        for ext in required:
            if ext.last_calculation:
                if self.last_calculation < ext.last_calculation:
                    return True
        return False

    def reset_calculation_state(self):
        self.last_calculation=None

    # extensions.by_category('Import')[1].calculate()
    def calculate(self):
        from qgis import utils
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant
        from mole.qgisinteraction.layer_interaction import find_layer_by_name, \
            add_attributes_if_not_exists

        #check wether a evaluation function is defined
        if self.evaluator == None: return
        #self.calculate_required()
        baritem=oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":','Searching for mandatory predecessors')
        required = self.required()
        for ext in required:
            ext.calculate()
        oeq_global.OeQ_pop_info(baritem)
        if not self.needs_evaluation(required):
            return

        #get source and target nodes
        source_layer = legend.nodeByName(self.layer_in)
        target_layer = legend.nodeByName(self.layer_out)
        if (not source_layer) | (not target_layer):
            oeq_global.OeQ_push_warning(str(self.extension_id) + ':','Sourcelayer "'+self.layer_in+'" not found in calculate()')
        source_layer =source_layer[0]
        target_layer = target_layer[0]

        #save visibility states and st them to 'visible'
        legend.nodeStoreVisibility(source_layer)
        legend.nodeShow(source_layer)
        legend.nodeStoreVisibility(target_layer)
        legend.nodeShow(target_layer)

        #get source and target layers
        source_layer = source_layer.layer()
        target_layer = target_layer.layer()
        #time.sleep(0.5)

        #get target data provider
        target_provider = target_layer.dataProvider()

        if self.get_par_out():
            #add missing attributes to target
            add_attributes_if_not_exists(target_layer, self.par_out_as_attributes())

        #init progressbar
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                      u'Updating layer "' + self.layer_out + '" from "' + self.layer_in + '"!',
                                                      maxcount=source_layer.featureCount())
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        #do calculation feature by feature
        for srcFeat in source_layer.getFeatures():
            #define empty input parameter dict
            par_in_data = {}

            #get input parameters from source
            for par in self.par_in:
                #check whether anptut parameter exists in source attributes
                if source_layer.fieldNameIndex(par) < 0:
                    oeq_global.OeQ_push_warning('Extension "' + self.extension_name + '":',
                                                'Layer "' + self.layer_in + '" has no attribute "' + par + '"!')
                    return None

                #get the corresponding value
                value = srcFeat.attributes()[source_layer.fieldNameIndex(par)]

                #add it to the input parameter dict
                par_in_data.update({par: value})

            #execute the extension specific evaluations
            result = self.evaluate(par_in_data)

            #define empty output parameter dict
            attributevalues = {}

            #add values to the output parameter dict
            #print "RESULTKEYS"
            #print result.keys()
            for i in result.keys():
                attributevalues.update({target_layer.fieldNameIndex(i): result[i]['value']})

            #get the target feature of the same building id as the source feature
            tgtFeat = filter(lambda x: x.attribute('BLD_ID') == srcFeat.attribute('BLD_ID'),
                             target_layer.getFeatures())
            #if it does not exist go to next
            if tgtFeat:
                tgtFeat = tgtFeat[0]
            else:
                continue

            #set the attribute values of the target provider to the evaluated output parameters
            target_provider.changeAttributeValues({tgtFeat.id(): attributevalues})

            #trigger pogressbar
            progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        #restore visibility states
        legend.nodeRestoreVisibility(self.layer_in)
        legend.nodeRestoreVisibility(self.layer_out)

        #if any result shall be visualized
        if self.show_results:
            self.work_out_results()
        oeq_global.OeQ_pop_progressbar(progressbar)
        self.last_calculation=datetime.datetime.now()
       #time.sleep(0.5)


    def work_out_results(self):
        from mole.qgisinteraction.layer_interaction import fullRemove
        from mole.qgisinteraction import legend
        fullRemove(self.layer_name)
        self.update_colortable()

        #create category group in legend
        if not legend.nodeExists(self.category):
            cat=legend.nodeCreateGroup(self.category,2)
        else:
            cat=legend.nodeByName(self.category)[0]
        #create subcategory group in legend
        if not legend.nodeExists(self.subcategory):
            subcat=legend.nodeCreateGroup(self.subcategory,'bottom',cat)
        else:
            subcat=legend.nodeByName(self.subcategory)[0]

        #use the housing layer as a template for the resultlayer
        resultnode=legend.nodeDuplicate(config.housing_layer_name,self.layer_name,None,subcat)
        self.update_colortable()

        #copy the required attributes of the datalayer to the resultlayer
        legend.nodeCopyAttributes(config.data_layer_name,resultnode,self.show_results)

        #add the colortable as style
        resultnode.layer().loadNamedStyle( self.colortable)

        #resultnode=legend.nodeConvertCRS(resultnode,config.default_extent_crs)

        #add node entry to the radiogroup of the category
        legend.nodeRadioAdd(resultnode,self.category)
        legend.nodeShow(resultnode)
        time.sleep(0.1)
        legend.nodeCollapse(resultnode)
        time.sleep(0.1)
        legend.nodeCollapse(subcat)
        time.sleep(0.1)
        legend.nodeCollapse(cat)

        #legend.nodeZoomTo(config.investigation_shape_layer_name)


    def needle_request(self):
        from mole.qgisinteraction import layer_interaction,plugin_interaction,legend
        from mole.project import config
        from mole import extensions
        from qgis.core import QgsVectorLayer
        from qgis.utils import iface
        # create data node
        if not legend.nodeExists(config.pst_input_layer_name):
            rci = plugin_interaction.RealCentroidInteraction(config.real_centroid_plugin_name)
            polygon = config.housing_layer_name
            output = os.path.join(oeq_global.OeQ_project_path(), config.pst_input_layer_name + '.shp')
            centroid_layer = rci.create_centroids(polygon, output)

            if centroid_layer.isValid():
                layer_interaction.add_layer_to_registry(centroid_layer)
                polygon = legend.nodeByName(polygon)
                if not polygon: return 0
                polygon = polygon[0].layer()
                rci.calculate_accuracy(polygon, centroid_layer)
                layer_interaction.add_style_to_layer(config.valid_centroids_style, centroid_layer)
                #self.reorder_layers()
               # print centroid_layer.name()
                legend.nodeByName(centroid_layer.name())[0].setExpanded(False)
                #source_section = self.progress_items_model.section_views[1]
                #section_model = source_section.model()
                #project_item = section_model.findItems("Load building coordinates")[0]
                #project_item.setCheckState(2)
                #time.sleep(0.1)
                #self.handle_load_raster_maps()
                return 2
            else:
                return 0
        if not legend.nodeExists('Data'):
            cat=legend.nodeCreateGroup('Data')
        else:
            cat=legend.nodeByName('Data')[0]

        #create_database
        #self.create_database(True,'Data')

        # show import layers
        layerstoshow = [config.investigation_shape_layer_name,config.pst_input_layer_name]
        layerstoshow += ([i.layer_name for i in extensions.by_category('Import',extensions.by_state(True))])
        legend.nodesShow(layerstoshow)

        #remove point sampling layer
        legend.nodeRemove(config.pst_output_layer_name,physical=True)

        #run point sampling tool
        psti = plugin_interaction.PstInteraction(iface, config.pst_plugin_name)
        psti.set_input_layer(config.pst_input_layer_name)
        abbreviations = psti.select_and_rename_files_for_sampling()
        pst_output_layer = psti.start_sampling(oeq_global.OeQ_project_path(), config.pst_output_layer_name)
        #oeq_global.OeQ_wait_for_file(pst_output_layer)
        vlayer = iface.addVectorLayer(pst_output_layer, config.pst_output_layer_name,"ogr")
        oeq_global.OeQ_wait_for_renderer()
        #vlayer = QgsVectorLayer(pst_output_layer, config.pst_output_layer_name,"ogr")
        #layer_interaction.add_layer_to_registry(vlayer)

        #move to data
        legend.nodeMove(vlayer.name(),'bottom','Data')

        #run import extensions

        # collapse and hide
        legend.nodeCollapse('Import')
        legend.nodeHide('Import')

        # unlock
        #oeq_global.OeQ_unlockQgis()
        return 2


OeQExtension.generic_id_cnt = 0



def by_category(category=None, registry=None):
    if registry == None:
        registry = oeq_global.OeQ_ExtensionRegistry
    if category == None:
        return registry
    return filter(lambda ext: ext.category == category, registry)


def by_state(active=None, category=None, registry=None):
    registry = by_category(category, registry)
    if active == None:
        return registry
    return filter(lambda ext: ext.active == active, registry)


def by_name(name=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if name == None:
        return registry
    return filter(lambda ext: ext.extension_name == name, registry)


def by_layername(name=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if name == None:
        return registry
    return filter(lambda ext: ext.layer_name == name, registry)


def by_type(type=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if type == None:
        return registry
    return filter(lambda ext: ext.source_type == type, registry)


def by_field_id(field_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if field_id == None:
        return registry
    return filter(lambda ext: ext.field_id == field_id, registry)


def by_layerid(layer_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if layer_id == None:
        return registry
    return filter(lambda ext: ext.layer_id == layer_id, registry)


def by_extension_id(extension_id=None, category=None, active=None, registry=None):
    registry = by_state(active, category, registry)
    if extension_id == None:
        return registry
    return filter(lambda ext: ext.extension_id == extension_id, registry)




#load extensions to project and update colortables
def copy_extensions_to_project():
    import copy
    oeq_global.OeQ_ExtensionRegistry = copy.deepcopy(oeq_global.OeQ_ExtensionDefaultRegistry)
    for ext in oeq_global.OeQ_ExtensionRegistry:
        ext.update_colortable(True)
    oeq_global.OeQ_ExtensionsLoaded = True

'''
def load_extensions_from_project(): #mi
    project_path = oeq_global.OeQ_project_path()
    project_name = oeq_global.OeQ_project_name()
    registry_file = os.path.join(project_path, project_name + '.xreg')
    if os.path.isfile(registry_file):
        try:
            with open(registry_file, 'rb') as input:
                oeq_global.OeQ_ExtensionRegistry = pickle.load(input)
                oeq_global.OeQ_ExtensionsLoaded = True
        except IOError, FileNotFoundError:
            print(self.__module__, FileNotFoundError)

    else:
        copy_extensions_to_project()
    if oeq_global.OeQ_ExtensionRegistry == []:
        copy_extensions_to_project()
    for ext in oeq_global.OeQ_ExtensionRegistry:
        ext.update_colortable(True)


def XXsave():
    project_path = oeq_global.OeQ_project_path()
    project_name = oeq_global.OeQ_project_name()
    if not oeq_global.OeQ_project_saved():
        copy_extensions_to_project()
    update_all_colortables()
    registry_file = os.path.join(project_path, project_name + '.xreg')
    try:
        with open(registry_file, 'wb') as output:
            pickle.dump(oeq_global.OeQ_ExtensionRegistry, output, pickle.HIGHEST_PROTOCOL)
    except IOError, FileNotFoundError:
        print(self.__module__, FileNotFoundError)
'''

def run_active_extensions(category=None):
    for extension in by_state(True, category):
       # if extension.source_type == 'wms':
       #     extension.decode_color_table()
        extension.calculate()


def export():
    pass

def update_all_colortables(overwrite=True):
    for ext in by_state(overwrite):
        ext.update_colortable()

