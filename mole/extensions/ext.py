
# -*- coding: utf-8 -*-

import os,time,datetime
import pickle
from mole import oeq_global
from mole.project import config
from mole.qgisinteraction import legend
from qgis.core import QgsVectorJoinInfo




def average(self=None, parameters={}):
    """

    :param self:  (Default value = None)
    :param parameters:  (Default value = {})

    """
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
    """
    The class OeQExtension is used to describe data information sources and accociated workflows.
    It tells Open eQuarter where to get the information from, how to load, how optimize it, defines feature specific evaluations and calculations etc.
    The class is able to track and check inter-extension dependencies as well.
    """
    def __init__(self, category=None,
                 subcategory = None,
                 field_id=None,
                 extension_id=None,
                 extension_name=None,
                 extension_type = None,
                 extension_filepath = None,
                 layer_name = None,
                 #layer_id=None,
                 description='Extention Details',
                 source_type=None,
                 active=False,
                 source=None,
                 source_crs=None,
                 bbox_crs='EPSG:4326',
                 par_in=[],
                 sourcelayer_name=None,
                 #par_out=None,
                 targetlayer_name=None,
                 #field_rename=None,
                 colortable=None,
                 show_results=[],
                 load_method=None,
                 preflight_method = None,
                 sample_mathod = None,
                 evaluation_method=average,
                 postflight_method=None,
                 last_calculation=oeq_global.first_of_all_calculation_times):
        """
        Constructor for class OeQExtension

        :param category: Category in the QGIS legend where the layer (after load) shall reside (Default value = None)
        :param subcategory: Subcategory in the QGIS legend where the target layer (after load) shall reside  (Default value = None)
        :param field_id:  (Default value = None)
        :param extension_id:  Unique ID for the extension (Default value = None)
        :param extension_name:  Name of the extension (Default value = None)
        :param extension_type:  Type of the extension (might be 'basic','information' or 'calculation') (Default value = None)
        :param extension_filepath: path to the extension (Default value = None)
        :param layer_name: name of the layer (after load)  (Default value = None)
        :param layer_id:  Expired!
        :param description:  Description of the extension's spirit and purpose (Default value = 'Extention Details')
        :param source_type:  Type of information source (Default value = None)
        :param active:  Flag, defining wether the extension shall be used or not (Default value = None)
        :param source:  Information source, might be a URL or a path (Default value = None)
        :param source_crs:  Coordinatesystem of the information source (Default value = None)
        :param bbox_crs:  Coordinatesystem of the bounding box of wfs (Default value = 'EPSG:4326')
        :param par_in:  Mandatory parameters for evaluation (Default value = None)
        :param sourcelayer_name: Source Layer for evaluation (Default value = None)
        :param par_out:  Expired!
        :param targetlayer_name: Target Layer for evaluation  (Default value = None -> )
        :param field_rename:  Expired !
        :param show_results:  Flag, defining wether the result shall be shown as a new layer (Default value = None)
        :param colortable:  Path to the colortable (Default value = None)
        :param load_method: Pointing to a method describing the load process (Default value = None)
        :param preflight_method: Pointing to a method called after the load process (Default value = None)
        :param sample_method: Pointing to a method describing the sample process (Default value = None)
        :param evaluation_method: Pointing to a method describing the evaluation process (Default value = None)
        :param postflight_method: Pointing to a method called after the evaluation process (Default value = None)
        :param last_calculation: Timestamp, set after each evalution(Default value = None)

        """

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
        self.extension_type = extension_type
        self.extension_filepath = extension_filepath
        self.category = category
        self.subcategory = subcategory
        #self.layer_id = layer_id
        self.description = description
        self.type = type
        self.source = source     
        self.source_crs = source_crs
        self.bbox_crs = bbox_crs
        self.active = active
        self.show_results = show_results
        self.load_method = load_method
        self.preflight_method = preflight_method
        self.sample_method = evaluation_method
        self.evaluation_method = evaluation_method
        self.postflight_method = postflight_method

        #if par_in == None:
        #    self.par_in = [field_id + '_L', field_id + '_H']
        #else:
        self.par_in = par_in
        if sourcelayer_name == None:
            self.sourcelayer_name = config.data_layer_name#config.building_coordinate_layer_name #config.sample_layer_name
        else:
            self.sourcelayer_name = sourcelayer_name
       # if par_out == None:
        #    self.par_out = self.get_par_out()
        #else:
        #    self.par_out = par_out
        if targetlayer_name == None:
            self.targetlayer_name = config.data_layer_name
        else:
            self.targetlayer_name = targetlayer_name
        #self.field_rename = field_rename

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
               extension_type=None,
               extension_filepath=None,
               layer_name=None,
               #layer_id=None,
               description='Extention Details',
               source_type=None,
               active=None,
               source=None,
               source_crs=None,
               bbox_crs=None,
               par_in=None,
               sourcelayer_name=None,
               #par_out=None,
               targetlayer_name=None,
               field_rename=None,
               show_results=None,
               colortable=None,
               load_method = None,
               preflight_method = None,
               sample_method=None,
               evaluation_method = None,
               postflight_method = None,
               last_calculation=None):
        """
        Update an OeQExtension

        :param category: Category in the QGIS legend where the layer (after load) shall reside (Default value = None)
        :param subcategory: Subcategory in the QGIS legend where the target layer (after load) shall reside  (Default value = None)
        :param field_id:  (Default value = None)
        :param extension_id:  Unique ID for the extension (Default value = None)
        :param extension_name:  Name of the extension (Default value = None)
        :param extension_type:  Type of the extension (might be 'basic','information' or 'calculation') (Default value = None)
        :param extension_filepath: path to the extension (Default value = None)
        :param layer_name: name of the layer (after load)  (Default value = None)
        :param layer_id:  Expired!
        :param description:  Description of the extension's spirit and purpose (Default value = 'Extention Details')
        :param source_type:  Type of information source (Default value = None)
        :param active:  Flag, defining wether the extension shall be used or not (Default value = None)
        :param source:  Information source, might be a URL or a path (Default value = None)
        :param source_crs:  Coordinatesystem of the information source (Default value = None)
        :param bbox_crs:  Coordinatesystem of the bounding box of wfs (Default value = 'EPSG:4326')
        :param par_in:  Mandatory parameters for evaluation (Default value = None)
        :param sourcelayer_name: Source Layer for evaluation (Default value = None)
        :param par_out:  Expired!
        :param targetlayer_name: Target Layer for evaluation  (Default value = None -> )
        :param field_rename:  Expired !
        :param show_results:  Flag, defining wether the result shall be shown as a new layer (Default value = None)
        :param colortable:  Path to the colortable (Default value = None)
        :param load_method: Pointing to a method describing the load process (Default value = None)
        :param preflight_method: Pointing to a method called after the load process (Default value = None)
        :param sample_method: Pointing to a method describing the sample process (Default value = None)
        :param evaluation_method: Pointing to a method describing the evaluation process (Default value = None)
        :param postflight_method: Pointing to a method called after the evaluation process (Default value = None)
        :param last_calculation: Timestamp, set after each evalution(Default value = None)

        """

        if category != None: self.category = category
        if subcategory != None: self.subcategory = subcategory
        if field_id != None: self.field_id = field_id
        if extension_id != None: self.extension_id = extension_id
        if extension_name != None: self.extension_name = extension_name
        if extension_type != None: self.extension_type = extension_type
        if extension_filepath != None: self.extension_filepath = extension_filepath
        if layer_name != None: self.layer_name = layer_name
        #if layer_id != None: self.layer_id = layer_id
        if description != None: self.description = description
        if source_type != None: self.source_type = source_type
        if active != None: self.active = active
        if source != None: self.source = source
        if source_crs != None: self.source_crs = source_crs
        if bbox_crs != None: self.bbox_crs = bbox_crs
        if par_in != None: self.par_in = par_in
        if sourcelayer_name != None: self.sourcelayer_name = sourcelayer_name
        #if par_out != None: self.par_out = par_out
        if field_rename != None: self.field_rename = field_rename
        if targetlayer_name != None: self.targetlayer_name = targetlayer_name
        if colortable != None: self.colortable = colortable
        if show_results != None: self.show_results = show_results
        if load_method != None: self.load_method = load_method
        if preflight_method != None: self.preflight_method = preflight_method
        if sample_method != None: self.sample_method = sample_method
        if evaluation_method != None: self.evaluation_method = evaluation_method
        if postflight_method != None: self.postflight_method = postflight_method
        if last_calculation != None: self.last_calculation = last_calculation

    def load(self, force=False):
        from mole.qgisinteraction import legend
        """
        Method call for the load method
        """
        if force:
            self.reset_calculation_state()
            if legend.nodeExists(self.layer_name):
                legend.nodeRemove(self.layer_name, physical=True)

            else:
                return None

        baritem = oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":',
                                           'Loading Layer')
        result = None
        if self.load_method != None:
            result = self.load_method(self)
            if result: self.sortAndShelve()
        oeq_global.OeQ_pop_info(baritem)
        return result

    def preflight(self):
        """
        Method call for the preflight method
        """
        baritem = oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":',
                                           'Running Preflight Script')
        result = None
        if self.preflight_method != None:
            result = self.preflight_method(self)
        oeq_global.OeQ_pop_info(baritem)
        return result


    def evaluate(self, parameter={},feature = None):
        """
        Method call for the evaluation method

        :param parameter:  List of fieldnames that are used for the evaluation process (Default value = {})
        :param feature:  Pointer to the current feature (Default value = None)

        """
        result = None
        if self.evaluation_method != None:
            result = self.evaluation_method(self, parameter , feature )
        return result

    def evaluateAll(self, parameter={},feature = None):
        from mole.qgisinteraction import legend
        from mole.qgisinteraction import layer_interaction
        from qgis.core import QgsMessageLog
        baritem = oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":',
                                       'Running Evaluation Script')

        if not legend.nodeExists(self.sourcelayer_name):
            oeq_global.OeQ_pop_info(baritem)
            oeq_global.OeQ_push_warning(str(self.extension_id) + ':',
                                        'Sourcelayer "' + self.sourcelayer_name + '" not found in evaluateAll()')
            return False

        if not legend.nodeExists(self.targetlayer_name):
            oeq_global.OeQ_pop_info(baritem)
            oeq_global.OeQ_push_warning(str(self.extension_id) + ':',
                                        'Targetlayer "' + self.targetlayer_name + '" not found in evaluateAll()')
            return False

       # save visibility states and st them to 'visible'
        legend.nodeStoreVisibility(self.sourcelayer_name)
        legend.nodeShow(self.sourcelayer_name)
        legend.nodeStoreVisibility(self.targetlayer_name)
        legend.nodeShow(self.targetlayer_name)

        # get source and target layers
        source_layer = legend.nodeByName(self.sourcelayer_name)[0].layer()
        target_layer = legend.nodeByName(self.targetlayer_name)[0].layer()
        # time.sleep(0.5)

        # get target data provider
        target_provider = target_layer.dataProvider()
        par_out = self.get_par_out()
        if bool(par_out):
            # add missing attributes to target
            layer_interaction.add_attributes_if_not_exists(target_layer, self.par_out_as_attributes())

        # init progressbar
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                      u'Updating layer "' + self.targetlayer_name + '" from "' + self.sourcelayer_name + '"!',
                                                      maxcount=source_layer.featureCount())
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        source_fields = [a.name() for a in source_layer.fields()]
        #print 'Sourcefields'
        #print source_fields
        #print self.par_in

        # check whether input parameter exists in source attributes
        if not all([par in source_fields for par in self.par_in]):
            oeq_global.OeQ_pop_progressbar(progressbar)
            oeq_global.OeQ_push_warning('Extension "' + self.extension_name + '":',
                                        'Source Layer "' + self.sourcelayer_name + '" does not contain all Input Attributes!')
            target_layer.commitChanges()
            return False

        # set target to edit mode
        target_layer.startEditing()

        # do calculation feature by feature
        for srcFeat in source_layer.getFeatures():
            #print "current key"
            #print srcFeat[config.building_id_key]

            if target_layer == source_layer:
                tgtFeat = srcFeat
            else:
                tgtFeat = filter(lambda x: x[config.building_id_key] == srcFeat[config.building_id_key],target_layer.getFeatures())

                if tgtFeat == []:
                    #print tgtFeat
                    #print type(tgtFeat)
                    QgsMessageLog.logMessage(str(self.extension_id) + "Building ID's not in layer " + self.targetlayer_name,
                                             'Warning in Extensions' + ':', QgsMessageLog.CRITICAL)
                    oeq_global.OeQ_pop_progressbar(progressbar)
                    oeq_global.OeQ_pop_info(baritem)
                    target_layer.commitChanges()
                    return False

                if (len(tgtFeat) >1):
                    #print tgtFeat
                    #print type(tgtFeat)
                    QgsMessageLog.logMessage(str(self.extension_id) + "Multiple Building ID's in layer "+ self.layer_name, 'Warning in Extensions' + ':', QgsMessageLog.CRITICAL)

                tgtFeat = tgtFeat[0]

            par_in_data = {}

            # set all source parameters
            for par in self.par_in:
                par_in_data.update({par: srcFeat[par]})


            # execute the extension specific evaluations
            result = self.evaluate(par_in_data, feature=srcFeat)

            # get the target feature of the same building id as the source feature
            #print srcFeat[config.building_id_key]

            # if multiple take the first an send logmessage
            #print tgtFeat
            #print type(tgtFeat)
            #if no target features found



            for par in par_out:
                tgtFeat[par] = result[par]['value']
            target_layer.updateFeature(tgtFeat)
            # trigger pogressbar
            progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        target_layer.commitChanges()

        # restore visibility states
        legend.nodeRestoreVisibility(self.sourcelayer_name)
        legend.nodeRestoreVisibility(self.targetlayer_name)

        oeq_global.OeQ_pop_progressbar(progressbar)
        oeq_global.OeQ_pop_info(baritem)
        return True



    def sample(self, parameter={},feature = None):
        """
        Method call for the evaluation method

        :param parameter:  List of fieldnames that are used for the sample process (Default value = {})
        :param feature:  Pointer to the current feature (Default value = None)

        """
        result = None
        if self.sample_method != None:
            result = self.sample_method(self, parameter , feature )
        return result


    def postflight(self):
        """
        Method call for the postflight method
        """

        baritem = oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":',
                                           'Running Postflight Script')
        result = None
        if self.postflight_method != None:
            result = self.postflight_method(self)
        oeq_global.OeQ_pop_info(baritem)
        return result


    def activate(self):
        """
        Activate an OeQExtension
        """
        self.active = True

    def deactivate(self):
        """
        Deactivate an OeQExtension
        """
        self.active = False

    def registerExtension(self, default=False):
        """
        Add an OeQExtension to one of the ExtensionRegistries
        :param default:  if False the extension is added to the projectspecific ExtensionRegistry,
                         if True it is inscribed into the global ExtensionRegistry (Default value = False)

        """
        from mole.oeq_global import OeQ_ExtensionRegistry, OeQ_ExtensionDefaultRegistry

        if default:
            OeQ_ExtensionDefaultRegistry.append(self)
        else:
            OeQ_ExtensionRegistry.append(self)



    def dummy_par(self):
        """ """
        return dict(zip(self.par_in, [1 for i in self.par_in]))

    def get_par_out(self):
        """
        Get the names of the output parameters of an extension, important for the dpendency checks.
        To make it work, each evaluation method of the extension always has to return
        the complete set of output parameters even if "feature" is None.
        """
        #print self.extension_filepath
        result = self.evaluate(parameter=dict(zip(self.par_in, [1 for i in self.par_in])),feature=None)
        if result == None: return {}
        return result.keys()


    def get_par_out_not_in(self):
        """
        The same as get_par_out() except that only output parameters will be given back that are not input parameters as well
        """
        return filter(lambda par: not (par in self.par_in), self.get_par_out())

    def par_out_as_attributes(self):
        """
        The same as get_par_out() except that the output parameters are given back as QGIS field attributes
        """
        from qgis.core import QgsField
        eval_out = self.evaluate(parameter=dict(zip(self.par_in, [1 for i in self.par_in])),feature=None)
        return [QgsField(i, eval_out[i]['type']) for i in eval_out.keys()]

    def get_default_colortable(self):
        """
        get the colortable information from the OeQDefaultExtensionRegistry
        """
        defcolortable = by_extension_id(self.extension_id, registry=oeq_global.OeQ_ExtensionDefaultRegistry)
        if defcolortable:
            return defcolortable[0].colortable
        return None

    def copy_default_colortable_to_project(self, overwrite=False):
        """
        copy the default colortable information from the OeQDefaultExtensionRegistry to project's OeQExtensionRegistry
        :param overwrite:  (Default value = False)

        """
        #print "0"
        from shutil import copyfile
        #print "1"
        ct_default = self.get_default_colortable()
        #print "2"
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



    def treelayer(self,which = 'own'):
        """
        Get the QgsLayerTreeLayer object (as used in the QGIS Legend model) of the extension's layer, the source_layer or the target_layer

        :param which:  'own','source','target'

        """
        thename = self.layer_name
        if which == 'source':
            thename = self.sourcelayer_name
        elif which == 'target':
            thename = self.targetlayer_name
        thelayer = legend.nodeByName(thename)
        if bool(thelayer):
            return thelayer[0]
        return None

    def layer(self,which = 'own'):
        """
        Get the QgsMapLayer object of the extension's layer, the source_layer or the target_layer

        :param which:  'own','source','target' (Default value = 'own')

        """
        treelayer = self.treelayer(which)
        if treelayer != None:
            return treelayer.layer()
        return None

    def provider(self,which = 'own'):
        """
        Get the data provider object of the extension's layer, the source_layer or the target_layer

        :param which:  'own','source','target' (Default value = 'own')

        """
        treelayer = self.treelayer(which)
        if treelayer != None:
            return treelayer.layer().dataProvider()
        return None

    def features(self,name = None,which ='own'):
        """
        Get the features object of the extension's layer, the source_layer or the target_layer

        :param which:  'own','source','target' (Default value = 'own')

        """
        treelayer = self.treelayer(which)
        if treelayer != None:
            return treelayer.layer().getFeatures()
        return None

    def sortAndShelve(self, collapse=True, hide=False):
        '''
        Sort and shelve the extension layer to category and subcategory. Building outline layer and building coordinate layer are only moved to position 1 resp. 2 of the legend root.
        :param collapse: shall category and subcategory collapse (Default is 'True')
        :type: boolean
        :param hide: shall category and subcategory change to 'invisible'  (Default is 'False')
        :type: boolean
        :return: the legend node of the moved extension layer
        '''
        # if extension layer exists
        from mole.qgisinteraction import legend
        mynode = None
        if legend.nodeExists(self.layer_name):
            # if it is the building outline layer
            if self.layer_name == config.building_outline_layer_name:
                return legend.nodeMove(self.layer_name, 1)

            # if it is the building coordinate layer
            if self.layer_name == config.building_coordinate_layer_name:
                return legend.nodeMove(self.layer_name, 2)

            # if category defined
            if bool(self.category):
                if not legend.nodeExists(self.category):
                    # create category node
                    cat = legend.nodeCreateGroup(self.category)
                else:
                    # get category node
                    cat = legend.nodeByName(self.category)[0]
                # if subcategory defined
                if bool(self.subcategory):
                    if not legend.nodeExists(self.subcategory):
                        # create category node
                        subcat = legend.nodeCreateGroup(self.subcategory, 'bottom', cat)
                    else:
                        # get category node
                        subcat = legend.nodeByName(self.subcategory)[0]
                    mynode = legend.nodeMove(self.layer_name, 'bottom', subcat)
                    if collapse: legend.nodeCollapse(subcat)
                    if hide: legend.nodeHide(subcat)
                else:
                    mynode = legend.nodeMove(self.layer_name, 'bottom', cat)
                    if collapse: legend.nodeCollapse(cat)
                    if hide: legend.nodeHide(cat)
            return mynode

    def load_wms(self,capture=True,forceload=False):
        """

        :param capture:  (Default value = True)

        """
        from qgis.core import QgsRasterLayer,QgsMapLayerRegistry
        from mole.oeq_global import OeQ_wait_for_renderer
        from mole.qgisinteraction.wms_utils import save_wms_extent_as_image,getWmsLegendUrl
        from mole.qgisinteraction import layer_interaction

        #zoom to a canvas covering the whole investigation area
        legend.nodeZoomTo(config.investigation_shape_layer_name)

        # remove old files if requested

        if legend.nodeExists(self.layer_name):
            if forceload:
                legend.nodeRemove(self.layer_name, physical=True)
                self.reset_calculation_state()
            else:
                return None

        if not legend.nodeExists(self.layer_name):
            #init progressbar
            progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                                  u'Loading WMS-Map "' + self.layer_name + '"!',
                                                                  maxcount=3)
            progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

            #setting the layer and filename for the temp raw load
            wmslayer='WMS_'+self.layer_name+'_RAW'

            oeq_global.OeQ_wait(1)

            #create and register the temp raw layer
            rlayer = QgsRasterLayer(self.source, wmslayer, self.source_type)
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)

            #load wms map
            if not OeQ_wait_for_renderer(60000):
                oeq_global.OeQ_push_warning(self.extension_id + ':','Loading Data timed out!')
                return None

            #oeq_global.OeQ_wait(3)

            legendURL = getWmsLegendUrl(rlayer)

            #push progressbar
            progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

            # save wms visible in canvas as image
            path = save_wms_extent_as_image(wmslayer)
            try:
                legend.nodeRemove(wmslayer, physical=True)
            except:
                pass

            #push progressbar
            progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

            oeq_global.OeQ_wait(1)

            # load clipped wms map
            rlayer = QgsRasterLayer(path, self.layer_name)
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            #print legendURL
            oeq_global.OeQ_wait(0.1)
            rlayer.setLegendUrl(legendURL)

            if not OeQ_wait_for_renderer(60000):
                oeq_global.OeQ_push_warning(self.extension_id + ':','Reloading WMS-Capture timed out!')
                return None

            # close progressbar
            oeq_global.OeQ_pop_progressbar(progressbar)

        return self.sortAndShelve()



    def load_wfs(self,extent=None,forceload = False):
        """

        :param extent:  (Default value = None)

        """
        import os
        from mole.project import config
        from mole import oeq_global
        from mole.qgisinteraction import legend,layer_interaction
        from qgis.core import QgsVectorLayer,QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsCoordinateTransform,QgsVectorFileWriter
        from qgis.utils import iface
        #check whether extent is defined, if not use investigationarea extent
        if not extent:
            extent= legend.nodeGetExtent(config.investigation_shape_layer_name)
        else:
            return None #legend.nodeByName(self.layer_name)[0]

        #init progressbar
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                              u'Be patient! Loading WFS-Map "' + self.layer_name + '" may take long!',
                                                              maxcount=3)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        #get crs objects
        print ('Defaulft CRS:',config.default_extent_crs)
        crsSrc=QgsCoordinateReferenceSystem(int(config.default_extent_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        crsDest=QgsCoordinateReferenceSystem(int(self.source_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        print ('Source CRS:',self.source_crs)
        crsBox=QgsCoordinateReferenceSystem(int(self.bbox_crs.split(':')[-1]), QgsCoordinateReferenceSystem.EpsgCrsId)
        print ('Box CRS:',self.bbox_crs)
        #transform extent
        #print ("Original Extent",config.default_extent_crs)
        #print (str(extent.yMinimum())+','+str(extent.xMinimum())+','+str(extent.yMaximum())+','+str(extent.xMaximum()))
        coord_transformer = QgsCoordinateTransform(crsSrc, crsBox)
        boxextent = coord_transformer.transform(extent)
        #print ("Box Extent",self.bbox_crs)
        #print (str(boxextent.yMinimum())+','+str(boxextent.xMinimum())+','+str(boxextent.yMaximum())+','+str(boxextent.xMaximum()))
        coord_transformer = QgsCoordinateTransform(crsSrc, crsDest)
         # windows might throw a warning while loading , as is does not adopt the CRS from the WFS source
        # so we the current messagebar item
        current_msgb= iface.messageBar().currentItem()
        #load wfs
        url = self.source
        if self.bbox_crs.split(':')[-1] == '4326':
            print ('WGS84:',)
            url = url+ '&BBOX='+str(boxextent.yMinimum())+','+str(boxextent.xMinimum())+','+str(boxextent.yMaximum())+','+str(boxextent.xMaximum())+ ',urn:ogc:def:crs:EPSG:6.9:' + self.bbox_crs.split(':')[-1]
        else:
            print ('Other:',)
            url = url+ '&BBOX='+str(boxextent.xMinimum())+','+str(boxextent.yMinimum())+','+str(boxextent.xMaximum())+','+str(boxextent.yMaximum())+ ',urn:ogc:def:crs:EPSG:6.9:' + self.bbox_crs.split(':')[-1]
        
        
        print (url)
        #wfsLayer=QgsVectorLayer(self.source + '&BBOX='+str(extent.xMinimum())+','+str(extent.yMinimum())+','+str(extent.xMaximum())+','+str(extent.yMaximum()),self.layer_name,'ogr')
        try:
            wfsLayer=QgsVectorLayer(url,self.layer_name,'ogr')
        except:
            pass
        
        #    oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":',
        #                              u'WFS load error! "' + self.source + '"!')
        # windows might throw a warning here, as is does not adopt the CRS from the WFS source
        # so the current baritem gets  immediately removed if is not the the one before loading
        if iface.messageBar().currentItem() != current_msgb:
            iface.messageBar().popWidget()
        # push progressbar
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        if not wfsLayer.isValid():
            oeq_global.OeQ_push_error(u'Extension "' + self.extension_name + '":',
                                      u'Could not load WFS-Map "' + self.source + '"!')
            return None
        wfsLayer.setCrs(crsDest)


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
        baritem=oeq_global.OeQ_push_info("Clipping Building Outlines:", "'"+self.layer_name+"'")
        wfsnode=legend.nodeClipByShapenode(wfsnode,config.investigation_shape_layer_name)
        oeq_global.OeQ_pop_info(baritem)

        #self.process()

        return self.sortAndShelve()
        #return wfsnode



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
    """

    :param 'Floors (WMS Capture: 

    """
        from qgis import utils
        from qgis.core import NULL
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant

        result = {config.building_id_key: {'type': QVariant.String,'value': NULL},
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
        """

        :param red:  (Default value = 0)
        :param green:  (Default value = 0)
        :param blue:  (Default value = 0)
        :param alpha:  (Default value = 0)
        :param resultkeys:  (Default value = [])
        :param mode:  (Default value = 'range')

        """
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
        """ """
        from qgis import utils
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant
        from mole.qgisinteraction.layer_interaction import add_attributes_if_not_exists, \
            colors_match_feature
        oeqMain = utils.plugins['mole']
        source_layer = legend.nodeByName(self.sourcelayer_name)
        if not source_layer:
            print "layer not found in decode color table"
            print source_layer
            return
        source_layer = source_layer[0]
        legend.nodeStoreVisibility(source_layer)
        legend.nodeShow(source_layer)
        #time.sleep(0.5)
        source_layer = self.layer('source')
        source_provider = self.provider('source')
        if self.source_type == 'wms':
            if self.colortable != None:
                oeqMain.color_picker_dlg.color_entry_manager.read_color_map_from_qml(self.colortable)
                color_dict = oeqMain.color_picker_dlg.color_entry_manager.layer_values_map[self.layer_name]

                progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                              u'Decoding colors in "' + self.sourcelayer_name + '"!',
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
        legend.nodeRestoreVisibility(self.sourcelayer_name)
        #time.sleep(0.5)


    def databaseInsane(self):
        from mole.qgisinteraction import legend
        import mole.extensions as ext
        if not legend.nodeExists(config.data_layer_name):
            ext.by_layername(config.building_outline_layer_name)[0].reset_calculation_state()
            return True
        return False




    def required(self):
        """ """
        from qgis.core import QgsMessageLog
        from mole import extensions as ext
        req=[]
        all_suppliers=filter(lambda ext: ext != self, by_state(True))

        self.databaseInsane()
        #req.insert(0, ext.by_layername(config.building_outline_layer_name)[0])
        #print "layer: ", self.layer_name
        #print "source: ", self.sourcelayer_name
        #print "target: ", self.targetlayer_name

        if (self.sourcelayer_name != self.layer_name): #(self.sourcelayer_name != config.data_layer_name) &
            sourcelayer_supplier = filter(lambda ext: (self.sourcelayer_name == ext.layer_name) & bool(self.sourcelayer_name), all_suppliers)
            #print "Sourcelayer supplier"
            #print sourcelayer_supplier
            if sourcelayer_supplier != []:
                if not (sourcelayer_supplier[0] in req):
                    req.insert(0, sourcelayer_supplier[0])
            else:
                QgsMessageLog.logMessage(str(self.extension_id) + 'Can not find a supplier for sourcelayer "' + str(self.sourcelayer_name) + '"',
                                         'Warning in Extensions' + ':', QgsMessageLog.CRITICAL)

        if (self.targetlayer_name != self.layer_name): #(self.targetlayer_name != config.data_layer_name) &
            targetlayer_supplier = filter(lambda ext: (self.targetlayer_name == ext.layer_name) & bool(self.targetlayer_name), all_suppliers)
            #print "Targetlayer supplier"
            #print targetlayer_supplier
            if targetlayer_supplier != []:
                if not (targetlayer_supplier[0] in req):
                    req.insert(0, targetlayer_supplier[0])
            else:
                QgsMessageLog.logMessage(str(self.extension_id) + 'Can not find a supplier for targetlayer "' + str(self.sourcelayer_name) + '"',
                'Warning in Extensions' + ':', QgsMessageLog.CRITICAL)
            # oeq_global.OeQ_push_warning(str(self.extension_id) + ':','can not find a supplier found for "'+str(ipar)+'"')

        if bool(self.par_in):
            for ipar in self.par_in:
                parameter_supplier = filter(lambda ext: ipar in ext.get_par_out(), all_suppliers)
                if parameter_supplier != []:
                    if not (parameter_supplier[0] in req):
                        #print supplier[0].extension_id
                        req.insert(0, parameter_supplier[0])
                else:
                    QgsMessageLog.logMessage(str(self.extension_id)+'Can not find a supplier found for "'+str(ipar)+'"','Warning in Extensions' + ':', QgsMessageLog.CRITICAL)
                    #oeq_global.OeQ_push_warning(str(self.extension_id) + ':','can not find a supplier found for "'+str(ipar)+'"')
        #print self.extension_id + ' needs:'
        #print [e.extension_id for e in req]
        #oeq_global.OeQ_wait(0.5)
        #print "Caller ", self.layer_name
        #for i in req:
        #    print "Extension ",i.layer_name
        #    print "Last update",i.last_calculation
        #oeq_global.OeQ_wait(0.1)
        return req

    def needs_evaluation(self,required=None):
        """

        sourcelayer_suppliers = filter(lambda ext: self.sourcelayer_name == ext.layer_name, all_suppliers)

        :param required:  (Default value = None)

        """
        from mole.qgisinteraction import legend
        if not required:
            required = self.required()
        #print self.extension_filepath

        if not all([(self.last_calculation > ext.last_calculation) for ext in required]):
            #print [str( self.last_calculation) + '  '  +str(ext.last_calculation) + ' : ' + str(self.last_calculation > ext.last_calculation)+ ' -> ' +  str(ext.extension_filepath)  for ext in required]
            #print "predessors outdated"
            self.reset_calculation_state()
            return True
        if bool(self.show_results) & (not legend.nodeExists(self.layer_name)):
            #print self.show_results
            #print self.layer_name
            #print legend.nodeExists(self.layer_name)
            #print str(self.extension_filepath)
            #print "node does not exist"
            self.reset_calculation_state()
            return True
        if bool(self.sourcelayer_name) & (not legend.nodeExists(self.sourcelayer_name)):
            #print "source node does not exist"
            self.reset_calculation_state()
            return True
        if bool(self.targetlayer_name) & (not legend.nodeExists(self.targetlayer_name)):
            #print "target node does not exist"
            self.reset_calculation_state()
            return True
        targetlayer=legend.nodeByName(self.targetlayer_name)[0].layer()
        target_fields = [a.name() for a in targetlayer.fields()]
        par_out = self.get_par_out()
        if not all([par in target_fields for par in par_out]):
            print "some fields do not exist"
            self.reset_calculation_state()
            return True
        return False

    '''
    def needs_needle_request(self,required=None):
        """

        :param required:  (Default value = None)

        """
        if not required:
            required = self.required()
        if not self.last_calculation:
            return True
        for ext in required:
            if ext.last_calculation:
                if self.last_calculation < ext.last_calculation:
                    return True
        return False
    '''
    def reset_calculation_state(self):
        """ """
        from mole.oeq_global import first_of_all_calculation_times
        self.last_calculation=first_of_all_calculation_times


    # extensions.by_category('Import')[1].process()
    def process(self, forcedload=False, forcedeval=False):
        """

        :param forcedload:  (Default value = False)
        :param forcedeval:  (Default value = False)

        """
        from qgis import utils
        from qgis.core import QgsField
        from PyQt4.QtCore import QVariant
        from mole.qgisinteraction.layer_interaction import find_layer_by_name, add_attributes_if_not_exists

        # remove existing layer if forcedload is True
        if forcedload:
            self.reset_calculation_state()
            if legend.nodeExists(self.layer_name):
                legend.nodeRemove(self.layer_name, physical=True)


        # search for mandatory predecessors
        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                      'Processing',maxcount=7)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        #baritem = oeq_global.OeQ_push_info(u'Extension "' + self.extension_name + '":','Updating mandatory predecessors')
        # find required predecessors
        required = self.required()

        # process every predecessor
        for ext in required:
            if ext.needs_evaluation(): ext.process()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter
        # check wether one of them was updated
        if not self.needs_evaluation():
            #oeq_global.OeQ_pop_info(baritem)
            oeq_global.OeQ_pop_progressbar(progressbar)
            return False

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        # check wether a load function is defined and run it
        if self.load_method != None:
            self.load()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        # check wether a preflight function is defined and run it
        if self.preflight_method != None:
            self.preflight()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        if self.evaluation_method != None:
                self.evaluateAll()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        # check wether a postflight function is defined and run it
        if self.postflight_method != None:
            self.postflight()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        # if any result shall be visualized
        if bool(self.show_results) & (type(self.show_results) == list):
           self.work_out_results()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print progress_counter

        self.last_calculation = datetime.datetime.now()
        # time.sleep(0.5)
        oeq_global.OeQ_pop_progressbar(progressbar)
        return True
        #return False



    def getValueFromDatabase(self,fieldname,building_id):
        layer = legend.nodeByName(config.data_layer_name)[0].layer()
        feature = filter(lambda x: x[config.building_id_key] in building_id ,layer.getFeatures().toList())
        return feature[0][fieldname]

    def getAttributeFromDatabase(self,fieldname):
        layer = legend.nodeByName(config.data_layer_name)[0].layer()
        field = filter(lambda x: x.name() == fieldname ,layer.dataProvider().fields())
        return field

    def work_out_results(self):
        """ """
        from mole.qgisinteraction.layer_interaction import fullRemove
        from mole.qgisinteraction import legend
        from mole.qgisinteraction.layer_interaction import find_layer_by_name, add_attributes_if_not_exists

        progressbar = oeq_global.OeQ_push_progressbar(u'Extension "' + self.extension_name + '":',
                                                      'Working out Results!',maxcount=8)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, 0)

        fullRemove(self.layer_name)

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        self.copy_default_colortable_to_project()

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        #create category group in legend
        if not legend.nodeExists(self.category):
            cat=legend.nodeCreateGroup(self.category,2)
        else:
            cat=legend.nodeByName(self.category)[0]

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print 'Create Group'

        #create subcategory group in legend
        if not legend.nodeExists(self.subcategory):
            subcat=legend.nodeCreateGroup(self.subcategory,'bottom',cat)
        else:
            subcat=legend.nodeByName(self.subcategory)[0]

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        #use the housing layer as a template for the resultlayer

        resultnode=legend.nodeDuplicate(config.building_outline_layer_name, self.layer_name, None, subcat)

        legend.nodeDeleteAllAttributes(resultnode,config.building_id_key)

         #oeq_global.OeQ_wait(0.5)
        #print 'Copy Colortable'
        #self.copy_default_colortable_to_project()
        #oeq_global.OeQ_unlockQgis()
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)

        #copy the required attributes of the datalayer to the resultlayer
        #return
        database = legend.nodeByName(config.data_layer_name)[0].layer()
        target_layer=resultnode.layer()
        target_layer.dataProvider().addAttributes(self.getAttributeFromDatabase(self.show_results[0]))
        target_layer.updateFields()
        #add_attributes_if_not_exists(target_layer, self.show_results)
        target_layer.startEditing()

        # set target to edit mode

        result = dict(zip([x[config.building_id_key] for x in database.getFeatures()],[x[self.show_results[0]] for x in database.getFeatures()]))

        target_layer.startEditing()
        # do calculation feature by feature
        for tgtFeat in target_layer.getFeatures():
            tgtFeat[self.show_results[0]] = result[tgtFeat[config.building_id_key]]
            target_layer.updateFeature(tgtFeat)
        target_layer.commitChanges()

        #legend.nodeCopyAttributes(config.data_layer_name,resultnode,self.show_results)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #return
        #add the colortable as style
        resultnode.layer().loadNamedStyle( self.colortable)

        #resultnode=legend.nodeConvertCRS(resultnode,config.default_extent_crs)
        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        #print 'Add Node Entry 1'
        #add node entry to the radiogroup of the category
        legend.nodeRadioAdd(resultnode,self.category)
        legend.nodeShow(resultnode)
        ##oeq_global.OeQ_wait(0.1)
        #print 'Add Node Entry 2'

        legend.nodeCollapse(resultnode)
        ##oeq_global.OeQ_wait(0.1)
        #print 'Add Node Entry 3'

        legend.nodeCollapse(subcat)
        ##oeq_global.OeQ_wait(0.1)
        #print 'Add Node Entry 4'

        legend.nodeCollapse(cat)

        progress_counter = oeq_global.OeQ_update_progressbar(progressbar, progress_counter)
        oeq_global.OeQ_pop_progressbar(progressbar)

        #legend.nodeZoomTo(config.investigation_shape_layer_name)

    def sampleColor(self,feature, rasterlayer_name = '', fieldname='',feature_crs = None, blur=3):
        from mole.qgisinteraction import layer_interaction
        if rasterlayer_name == '':
            rasterlayer_name = self.layer_name
        fieldnames = ['R','G','B','a']
        if fieldname != '':
            fieldnames = [fieldname + '_' + c for c in fieldnames]
        return layer_interaction.sampleColorFromRasterLayerByFeature(feature, rasterlayer_name, fieldnames, feature_crs, blur)

    def sampleData(self, feature, datalayer_name = '', field_list=[], feature_crs = None):
        if datalayer_name == '': datalayer_name = self.layer_name
        from mole.qgisinteraction import layer_interaction
        return layer_interaction.sampleDataFromVectorLayerByFeature(feature, datalayer_name, field_list, feature_crs)

    def sampleold(self,source_layer=None,target_layers=None,result_layer=None):
        """

        :param source_layer:  (Default value = None)
        :param target_layers:  (Default value = None)
        :param result_layer:  (Default value = None)

        """
        from mole.qgisinteraction import layer_interaction, plugin_interaction, legend
        from qgis.utils import iface
        if source_layer == None:
            source_layer = self.sourcelayer_name().name()
        if result_layer == None:
            result_layer = self.targetlayer_name().name()

        layerstoshow = [source_layer, source_layer]
        layerstoshow += (target_layers)
        legend.nodesShow(layerstoshow)

        if  legend.nodeExists(result_layer):
            legend.nodeRemove(result_layer, physical=True)

        # run point sampling tool
        psti = plugin_interaction.PstInteraction(iface, config.pst_plugin_name)
        psti.set_input_layer(source_layer)
        abbreviations = psti.select_and_rename_files_for_sampling()
        pst_output_layer = psti.start_sampling(oeq_global.OeQ_project_path(), result_layer)
        # oeq_global.OeQ_wait_for_file(pst_output_layer)
        vlayer = iface.addVectorLayer(pst_output_layer, result_layer, "ogr")
        oeq_global.OeQ_wait_for_renderer()

    def needle_request(self):
        """ """
        from mole.qgisinteraction import layer_interaction,plugin_interaction,legend
        from mole.project import config
        from mole import extensions
        from qgis.core import QgsVectorLayer
        from qgis.utils import iface
        # create data node
        if not legend.nodeExists(config.building_coordinate_layer_name):
            rci = plugin_interaction.RealCentroidInteraction(config.real_centroid_plugin_name)
            polygon = config.building_outline_layer_name
            output = os.path.join(oeq_global.OeQ_project_path(), config.building_coordinate_layer_name + '.shp')
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
        layerstoshow = [config.investigation_shape_layer_name, config.building_coordinate_layer_name]
        layerstoshow += ([i.layer_name for i in extensions.by_category('Import',extensions.by_state(True))])
        legend.nodesShow(layerstoshow)

        #remove point sampling layer
        legend.nodeRemove(config.sample_layer_name, physical=True)

        #run point sampling tool
        psti = plugin_interaction.PstInteraction(iface, config.pst_plugin_name)
        psti.set_input_layer(config.building_coordinate_layer_name)
        #abbreviations = psti.select_and_rename_files_for_sampling()
        pst_output_layer = psti.start_sampling(oeq_global.OeQ_project_path(), config.sample_layer_name)
        #oeq_global.OeQ_wait_for_file(pst_output_layer)
        vlayer = iface.addVectorLayer(pst_output_layer, config.sample_layer_name, "ogr")
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

    #wrappers
    def createDatabase(self):
        from mole import extensions
        return extensions.createDatabase(self.extension_name)

    def createSampleLayer(self):
        from mole import extensions
        return extensions.createSampleLayer(self.extension_name)


    def createCoordinateLayer(self):
        from mole import extensions
        return extensions.createCoordinateLayer(self.extension_name)



def by_category(category=None, registry=None):
    """

    :param category:  (Default value = None)
    :param registry:  (Default value = None)

    """
    if registry == None:
        registry = oeq_global.OeQ_ExtensionRegistry
    if category == None:
        return registry
    return filter(lambda ext: ext.category == category, registry)

def by_subcategory(subcategory=None, registry=None):
    """

    :param subcategory:  (Default value = None)
    :param registry:  (Default value = None)

    """
    if registry == None:
        registry = oeq_global.OeQ_ExtensionRegistry
    if subcategory == None:
        return registry
    return filter(lambda ext: ext.subcategory == subcategory, registry)

def by_state(active=None, category=None, registry=None):
    """

    :param active:  (Default value = None)
    :param category:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_category(category, registry)
    if active == None:
        return registry
    return filter(lambda ext: ext.active == active, registry)


def by_name(name=None, category=None, active=None, registry=None):
    """

    :param name:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if name == None:
        return registry
    return filter(lambda ext: ext.extension_name == name, registry)


def by_layername(name=None, category=None, active=None, registry=None):
    """

    :param name:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if name == None:
        return registry
    return filter(lambda ext: ext.layer_name == name, registry)


def by_type(type=None, category=None, active=None, registry=None):
    """

    :param type:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if type == None:
        return registry
    return filter(lambda ext: ext.source_type == type, registry)


def by_field_id(field_id=None, category=None, active=None, registry=None):
    """

    :param field_id:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if field_id == None:
        return registry
    return filter(lambda ext: ext.field_id == field_id, registry)


def by_layerid(layer_id=None, category=None, active=None, registry=None):
    """

    :param layer_id:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if layer_id == None:
        return registry
    return filter(lambda ext: ext.layer_id == layer_id, registry)

def by_targetlayer_name(targetlayer_name=None, category=None, active=None, registry=None):
    """

    :param targetlayer_name:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if targetlayer_name == None:
        return registry
    return filter(lambda ext: ext.targetlayer_name == targetlayer_name, registry)

def by_sourcelayer_name(sourcelayer_name=None, category=None, active=None, registry=None):
    """

    :param sourcelayer_name:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if sourcelayer_name == None:
        return registry
    return filter(lambda ext: ext.sourcelayer_name == sourcelayer_name, registry)


def by_extension_id(extension_id=None, category=None, active=None, registry=None):
    """

    :param extension_id:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if extension_id == None:
        return registry
    return filter(lambda ext: ext.extension_id == extension_id, registry)

def by_extension_type(extension_type=None, category=None, active=None, registry=None):
    """

    :param extension_type:  (Default value = None)
    :param category:  (Default value = None)
    :param active:  (Default value = None)
    :param registry:  (Default value = None)

    """
    registry = by_state(active, category, registry)
    if extension_type == None:
        return registry
    return filter(lambda ext: ext.extension_type == extension_type, registry)

#load extensions to project and update colortables
def copy_extensions_to_project():
    """ """
    import copy
    oeq_global.OeQ_ExtensionRegistry = copy.deepcopy(oeq_global.OeQ_ExtensionDefaultRegistry)
    for ext in oeq_global.OeQ_ExtensionRegistry:
        ext.copy_default_colortable_to_project(True)
    oeq_global.OeQ_ExtensionsLoaded = True

'''
def load_extensions_from_project(): #mi
    project_path = oeq_global.OeQ_project_path()
    project_name = oeq_global.OeQ_project_name()
    registry_file = os.path.join(project_path, project_name + '.xreg')
    if os.path.isfile(registry_file):
    """ """
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
    """ """
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


def createDatabase(caller = 'Unknown'):
    """ """
    from mole import extensions
    from mole.qgisinteraction import legend
    result = False
    baritem = oeq_global.OeQ_push_info('Extension "' + caller + '":', 'Creating Database!')
    if not legend.nodeExists(config.data_layer_name):
        result = bool(legend.nodeCreateDatabase(config.building_outline_layer_name, config.data_layer_name,
                                                config.project_crs, True, "Data"))
    oeq_global.OeQ_pop_info(baritem)
    return result


def createSampleLayer(caller = 'Unknown'):
    """ """
    from mole import extensions
    from mole.qgisinteraction import legend
    result = False
    baritem = oeq_global.OeQ_push_info('Extension "' + caller + '":', 'Creating Database!')
    if not legend.nodeExists(config.sample_layer_name):
        result = bool(legend.nodeCreateSampleLayer(config.building_coordinate_layer_name, config.sample_layer_name,
                                                   config.project_crs, True, "Data"))
    oeq_global.OeQ_pop_info(baritem)
    return result

def createCoordinateLayer(caller='Unknown',forced = True):
    """ """
    from mole.qgisinteraction import legend,layer_interaction
    baritem = oeq_global.OeQ_push_info('Extension "' + caller + '":', 'Creating Centroids!')
    result = bool(layer_interaction.createCentroidLayer(config.building_outline_layer_name,config.building_coordinate_layer_name,forced))
    oeq_global.OeQ_pop_info(baritem)
    return result



def run_active_extensions(category=None):
    """

    :param category:  (Default value = None)

    """
    for extension in by_state(True, category):
       # if extension.source_type == 'wms':
       #     extension.decode_color_table()
        extension.process()


def export():
    """ """
    pass

def update_all_colortables(overwrite=True):
    """

    :param overwrite:  (Default value = True)

    """
    for ext in by_state(overwrite):
        ext.copy_default_colortable_to_project()

def get_tree(show=False):
    """

    :param show:  (Default value = False)

    """
    categories=sorted(list(set([i.category for i in by_category()])))
    ext_tree=[]
    for i in categories:
        subcategories = sorted(list(set([cat.subcategory for cat in by_category(i)])))
        branch=[]
        for j in subcategories:
            branch.append(by_subcategory(j))
        ext_tree.append(branch)
    if show:
        for i in ext_tree:
            print i[0][0].category
            for j in i:
                print " > " + j[0].subcategory
                for k in j:
                    print " > " + " > " + k.extension_name
    return ext_tree
