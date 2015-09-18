from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsVectorFileWriter
from qgis.core import QgsMapLayerRegistry, QgsMapLayer, QgsMapRenderer, QgsProject, QgsField
from qgis.analysis import QgsOverlayAnalyzer
from PyQt4.QtCore import QSettings, QSize, QVariant
from PyQt4.QtGui import QPainter, QColor, QImage, QProgressDialog, QLabel
import os
import time
from string import find
from mole.project import config
from mole import oeq_global

def create_temporary_layer(layer_name, layer_type, crs_name=''):
    """
    Create and add a new Vectorlayer, with name and type as specified in layer_name, layer_tpye and crs_name
    :param layer_name: The name of the new vectorlayer
    :type layer_name: str
    :param layer_type: The type of the new vectorlayer
    :type layer_type: str
    :param crs_name: The name of the new crs, if empty, the user will be prompted for the crs
    :tpye crs_name: str
    :return The created layer:
    :rtype QgsVectorLayer:
    """
    if layer_name and not layer_name.isspace() and layer_type and not layer_type.isspace():

        crs = ''

        if crs_name and not crs_name.isspace() and QgsCoordinateReferenceSystem().createFromUserInput(crs_name):
            # surpress crs-choice dialog
            old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
            QSettings().setValue('/Projections/defaultBehaviour', 'useProject')
            crs += '?crs=' + crs_name
        else:
            old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
            QSettings().setValue('/Projections/defaultBehaviour', 'prompt')

        # create a new shape-file called layer_name, of the type layer_type, with system encoding and crs according to crs_name
        shape_layer = QgsVectorLayer(layer_type + crs, layer_name, 'memory')
        shape_layer.setProviderEncoding('System')

        # reset appearance of crs-choice dialog to previous settings
        QSettings().setValue('/Projections/defaultBehaviour', old_validation)
        # QgsMapLayerRegistry.instance().addMapLayer(shape_layer,True)
        return shape_layer

    else:
        return None


def write_temporary_vector_layer_to_disk(vlayer, style=None, replace_in_legend=True):
    import os
    from qgis.utils import iface
    from mole import oeq_global
    if oeq_global.OeQ_project_name() == '':
        iface.actionSaveProjectAs().trigger()
    layer_name = vlayer.name()
    layer_crs = vlayer.crs()
    path = os.path.join(oeq_global.OeQ_project_path(), layer_name + '.shp')
    error = QgsVectorFileWriter.writeAsVectorFormat(vlayer, path, "System", layer_crs, 'ESRI Shapefile')
    if error == QgsVectorFileWriter.NoError:
        if replace_in_legend:
            QgsMapLayerRegistry.instance().removeMapLayer(vlayer.id())
            rewritten_layer = iface.addVectorLayer(path, layer_name, "ogr")
            if not rewritten_layer.isValid():
                oeq_global.OeQ_init_warning(title='Write Error!', message='path')
                return vlayer
            if style != None:
                add_style_to_layer(style, rewritten_layer)
                rewritten_layer.startEditing()
                time.sleep(0.2)
                rewritten_layer.commitChanges()
            return rewritten_layer
        else:
            oeq_global.OeQ_init_warning(title='Write Error!', message='path')
            return vlayer

#remove a layer including all files
def fullRemove(layer_name=None, layer_id=None):
    if layer_id is None:
        thelayer = find_layer_by_name(layer_name)
    else:
        thelayer = find_layer_by_id(layer_id)
    if thelayer is not None:
        layer_name = thelayer.name()
        QgsMapLayerRegistry.instance().removeMapLayer(thelayer.id())
        delete_layer_files(layer_name)
    oeq_global.OeQ_unlockQgis()

def delete_layer_files(layer):
    if (type(layer) == type('')) | (type(layer) == type(u'')):
        layer = find_layer_by_name(layer)
    if layer == None:
        return None
    source = layer.source()
    path = os.path.dirname(source)
    filenameroot = os.path.basename(source).split('.')
    if len(filenameroot) < 2:
        return []
    filenameroot = ''.join(filenameroot[:-1])+ '.'
    if path.exists(path):
                files = os.listdir(path)
                for file in files:
                    if files.startswith(filenameroot):
                        os.remove(os.path.join(path, file))

def load_layer_from_disk(path_to_layer, name):
    """
    Load a layer from disk
    :param path_to_layer: Location of the .shp-file
    :type path_to_layer: str
    :param name: Display-name of the loaded layer
    :type name: str
    :return:
    :rtype:
    """
    if os.path.exists(path_to_layer):
        disk_layer = QgsVectorLayer(path_to_layer, name, 'ogr')
        # QgsMapLayerRegistry.instance().addMapLayer(disk_layer,False)
        return disk_layer
    else:
        return None


def add_style_to_layer(path_to_style, layer):
    """
    Set the style of the layer to the given style
    :param path_to_style:
    :type path_to_style:
    :param layer:
    :type layer:
    :return:
    :rtype:
    """
    if layer and path_to_style and os.path.exists(path_to_style):
        layer.loadNamedStyle(path_to_style)


def add_layer_to_registry(layer):
    """
    Add the given layer to the MapLayerRegistry
    :param layer:
    :type layer:
    :return:
    :rtype:
    """
    if layer:
        # add the layer to the layer-legend
        QgsMapLayerRegistry.instance().addMapLayer(layer)


def find_layer_by_name(layer_name):
    """
    Iterate over all layers and return the layer with the name layer_name, if found
    :param layer_name: Name of the layer that shall be looked for
    :type layer_name: str
    :return:
    :rtype:
    """
    if layer_name and not layer_name.isspace():

        found_layers = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)
        if found_layers != [] and found_layers[0].name() == layer_name:
            return found_layers[0]
        else:
            return None


def find_layer_by_id(layer_id):
    """
    Iterate over all layers and return the layer with the id layer_id, if found
    :param layer_name: Name of the layer that shall be looked for
    :type layer_name: str
    :return:
    :rtype:
    """
    try:
        found_layer = QgsMapLayerRegistry.instance().mapLayers()[layer_id]
    except:
        return None
    return found_layer


def unhide_or_remove_layer(layer_name, mode='hide', iface = None):
    """
    Hide or remove the given layer from the MapLayerRegistry, depending on the mode.
    :param layer_name: Name of the layer to remove/hide
    :type layer_name: str
    :param mode: What to do with the layer; valid arguments are 'hide' or 'remove'
    :type mode: str
    :return:
    :rtype:
    """
    layer = find_layer_by_name(layer_name)
    if layer and mode == 'remove':
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())

    if layer and mode == 'hide' and iface:
        iface.legendInterface().setLayerVisible(layer, False)

    if layer and mode == 'unhide' and iface:
        iface.legendInterface().setLayerVisible(layer, True)


#ToDo Try to use the currently recommended way to save the layer
def write_vector_layer_to_disk(vlayer, full_path):
    """
    Write the given vector layer to disk.
    :param vlayer: The vector layer that shall be written to disk
    :type vlayer: QgsVectorLayer
    :param full_path: The path and filename the layer shall be written to
    :type full_path: str
    :return:
    :rtype:
    """
    out_path, out_name = os.path.split(full_path)

    if out_name.upper().endswith('.SHP'):
        out_name = out_name[:-4]
    if vlayer is not None and vlayer.isValid() and os.path.exists(out_path):

        if os.path.exists(os.path.join(out_path, out_name + '.shp')):
            new_name = out_name
            suffix = 0

            while os.path.exists(os.path.join(out_path, new_name + '.shp')):
                suffix += 1
                new_name = out_name + str(suffix)

            out_name = new_name

        full_path = os.path.join(out_path, out_name + '.shp')

        provider = vlayer.dataProvider()
        encoding = provider.encoding()
        crs = provider.crs()

        write_error = QgsVectorFileWriter.writeAsVectorFormat(vlayer, full_path, encoding, crs, 'ESRI Shapefile')
        #QgsVectorFileWriter()
        if write_error == QgsVectorFileWriter.WriterError:
            raise IOError('Can\'t create the file: {0}'.format(full_path))
            return None
        else:

            # wait until the layer was created
            timeout = 30
            while not os.path.exists(full_path) and timeout:
                time.sleep(0.1)
                timeout -= 1
                # disk_layer = QgsVectorLayer(full_path, out_name, 'ogr')

                # if disk_layer.isValid():
                #    old_features = provider.getFeatures()
                #    new_provider = disk_layer.dataProvider()
                #    feature_list = []
                #    for feature in old_features:
                #        feature_list.append(feature)

                #    new_provider.addFeatures(feature_list)
                #    return disk_layer
                # else:
                #    return None
    else:
        return None


def trigger_edit_mode(iface, layer_name, trigger='on'):
    """
    Iterate over all layers and activate the Layer called layer_name. Then toggle the edit mode of that layer.
    :param iface: The Qgis-interface that will be accessed
    :type iface: QgisInterface
    :param layer_name: Name of the layer, that shall be switched to edit_mode
    :type layer_name: str
    :return:
    :rtype:
    """
    if layer_name and not layer_name.isspace():

        edit_layer = find_layer_by_name(layer_name)

        # if the layer was found, it is activated and the editing and the adding of features will be triggered
        if edit_layer is not None:

            if trigger == 'on':
                edit_layer.startEditing()
                iface.actionAddFeature().trigger()
            elif trigger == 'off':
                iface.actionAddFeature().trigger()
                edit_layer.commitChanges()


def get_raster_layer_list(iface, visibility='all'):
    """
    Iterate over all layers and return a list of the currently visible WMS-files.
    :param iface: The Qgis-interface that will be accessed
    :type iface: QgisInterface
    :return: A list containing raster layers with the given visibility-value
    :rtype: list
    """
    active_raster_layers = []
    layer_list = QgsMapLayerRegistry.instance().mapLayers()
    interface = iface.legendInterface()

    if visibility == 'visible':
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and interface.isLayerVisible(layer):
                active_raster_layers.append(layer)

        return active_raster_layers

    elif visibility == 'invisible':
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and not interface.isLayerVisible(layer):
                active_raster_layers.append(layer)

        return active_raster_layers

    else:
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer:
                active_raster_layers.append(layer)

        return active_raster_layers


def open_wms_as_raster(iface, wms_url_with_parameters, layer_name):
    """
    Connect to a given wms-server and create a new wms-layer from the url.
    :param iface:
    :type iface:
    :param wms_url_with_parameters: The url to the raster-layer in the form '{parameter=value&}*{url=http://url_to.wms/}'
    :type wms_url_with_parameters: str
    :param layer_name: Name of the new wms raster-layer
    :type layer_name: str
    :return:
    :rtype:
    """
    if iface is not None and wms_url_with_parameters and layer_name and not wms_url_with_parameters.isspace() and not layer_name.isspace():

        rlayer = QgsRasterLayer(wms_url_with_parameters, layer_name, 'wms')

        if not rlayer.isValid():
            return None
        else:
            return rlayer


def zoom_to_layer(iface, layer_name):
    """
    Trigger the iface's zoom-to-layer-action on the layer given by its name.
    :param iface: Reference to Qgis interface
    :type iface: QgisInterface
    :param layer_name: Name of the layer to zoom to
    :type layer_name: str
    :return:
    :rtype:
    """
    if layer_name and not layer_name.isspace():

        zoom_layer = find_layer_by_name(layer_name)

        # if the shapefile was found set the layer active
        if zoom_layer is not None:
            iface.setActiveLayer(zoom_layer)
            iface.actionZoomToLayer().trigger()


def biuniquify_layer_name(layer_name):
    """
    Check the layer-registry if a layer with the same name exists and if so, append a number to make the name unique.
    :param layer_name: Name which will be checked for uniqueness
    :type layer_name: str
    :return: The (now) unique name
    :rtype: str
    """
    biunique_name = ''
    if layer_name and not layer_name.isspace():

        biunique_name = layer_name
        suffix = 0

        while(find_layer_by_name(biunique_name) is not None):
            biunique_name = layer_name + str(suffix)
            suffix += 1

    return biunique_name


def move_layer_to_position(iface, layer_name, position):
    """
    Move the layer with the name 'layer_name' to the given position in the iface's Table of Layers
    :param iface: Qgis Interface
    :type iface: QgisInterface
    :param layer_name: Name of the layer
    :type layer_name: str
    :param position: Postion from 0 to max (if position is larger than the number of layers, the layer is always added to the bottom)
    :type position: int
    :return:
    :rtype:
    """
    root = QgsProject.instance().layerTreeRoot()
    layers = root.children()
    for layer_node in layers:
        if layer_node.layerName() == layer_name:
            clone = layer_node.clone()
            root.insertChildNode(position,clone)
            root.removeChildNode(layer_node)
            iface.setActiveLayer(clone.layer())
            break


def save_layer_as_image(layer, extent, path_to_file, max_resolution='1024', image_type = 'tif'):
    """
    Select and save the currently visible extent to a .tif file
    :param width: image width
    :type width: int
    :param height: image height
    :type height: int
    :param name: name of the created file
    :type name: str
    :return:
    :rtype:
    """
    # calculate the extents width and height
    width = extent.width()
    height = extent.height()
    # calculate the missing value (width or height) of the output file, based on the extent
    if width >= height:
        height_as_dec = max_resolution / width * height
        width = max_resolution
        height = int(height_as_dec)
    else:
        width_as_dec = max_resolution / height * width
        width = int(width_as_dec)
        height = max_resolution

    # append the resolution to the filename and call the save method

    filename=layer.name()
    if filename.startswith("WMS_"):
       filename=filename.replace("WMS_","")
    else:
       resolution_prefix = '{}_{}-'.format(width, height)
       filename = resolution_prefix + layer.name()
    img = QImage(QSize(width, height), QImage.Format_ARGB32_Premultiplied)
    color = QColor(187, 187, 187, 0)
    img.fill(color.rgba())

    leonardo = QPainter()
    leonardo.begin(img)
    leonardo.setRenderHint(QPainter.Antialiasing)

    renderer = QgsMapRenderer()
    lst = [layer.id()]

    renderer.setLayerSet(lst)
    renderer.setExtent(extent)
    renderer.setOutputSize(img.size(), img.logicalDpiX())
    renderer.render(leonardo)
    leonardo.end()

    filename += '.{}'.format(image_type)
    out_path = os.path.join(path_to_file, filename)
    if img.save(out_path, image_type):
        return out_path


def intersect_shapefiles(shape1, shape2, output_path):
    """
    Intersect two shapefiles and wirte the result to disk
    :param shape1: First shapefile
    :type shape1: QgsVectorLayer
    :param shape2: Second shapefile
    :type shape2: QgsVectorLayer
    :param output_path: The place where the intersection shall be stored
    :type output_path: str
    :return: If the layers were intersected successfully
    :rtype: bool
    """
    try:
        if shape1.isValid() and shape2.isValid():
            analyser = QgsOverlayAnalyzer()
            #progress = QProgressDialog()
            #info = QLabel('Intersecting floor plan with investigation layer.\nThis may take up to 30 seconds.')
            #progress.setLabel(info)
            #progress.setMinimum(0)
            #progress.setMaximum(100)
            return analyser.intersection(shape1, shape2, output_path) #p=progress)
    except AttributeError, Error:
        print(Error)
        return False



def edit_housing_layer_attributes(housing_layer):
    """
    Add a PERIMETER, AREA, and BLD_ID field to the layer's attribute table and populate them with appropiate values.
    Delete duplicate features and finally remove the FID-field
    :param housing_layer: The layer whose attribute-table shall be edited
    :type housing_layer: QgsVectorLayer
    :return: If the changes were commited
    :rtype: bool
    """
    try:
        provider = housing_layer.dataProvider()
        housing_layer.startEditing()

        attributes = [QgsField('AREA', QVariant.Double),
                      QgsField('PERIMETER', QVariant.Double),
                      QgsField('BLD_ID', QVariant.String)]
        provider.addAttributes(attributes)
        name_to_index = provider.fieldNameMap()
        area_index = name_to_index['AREA']
        perimeter_index = name_to_index['PERIMETER']
        building_index = name_to_index['BLD_ID']
        try:
            fid_index = name_to_index['FID']
        except:
            pass

        building_id = 0

        for feature in provider.getFeatures():
            # if oeq_global.isnull(feature.attribute('FID')):
            # if feature.attribute('BLD_ID') == 0:
            geometry = feature.geometry()
            values = {area_index: geometry.area(), perimeter_index: geometry.length(),
                      building_index: '{}'.format(building_id)}
            provider.changeAttributeValues({feature.id(): values})
            building_id += 1
            # else:
            # These features are most likely to be duplicates of those that have an FID-entry
            #    provider.deleteFeatures([feature.id()])

        #provider.deleteAttributes([fid_index])
        return housing_layer.commitChanges()
    except AttributeError, Error:
        print(__name__, Error)
        return False


def add_parameter_info_to_layer(color_dict, field_name, layer):
    """
    Adds the color-legend to the given layers corresponding field
    :param color_dict: Dictionary containing the color-value map
    :type color_dict: dict
    :param field_name: The fields name-prefix to which the information belongs
    :type field_name: str
    :param layer: The layer which holds the fields
    :type layer: QgsVectorLayer
    :return:
    :rtype:
    """

    import mole.extensions as extensions
    extension = extensions.by_layername(layer.name(), 'import')
    if extension != []:
        extension = extension[0]
        try:
            provider = layer.dataProvider()
        except AttributeError, NoneTypeError:
            print(__name__, NoneTypeError)
            return

        for color_key in color_dict.keys():
            color_quadriple = color_key[5:-1].split(',')
            color_quadriple = map(int, color_quadriple)

            for feat in provider.getFeatures():
                if colors_match_feature(color_quadriple, feat, field_name):
                    result = {extension.field_id + '_P': {'type': QVariant.String,
                                                          'value': color_dict[color_key][0]},
                               extension.par_in[0]: {'type': QVariant.Double,
                                                    'value': color_dict[color_key][1]},
                               extension.par_in[1]: {'type': QVariant.Double,
                                                    'value': color_dict[color_key][2]}}

                    result.update(extension.evaluate({extension.par_in[0]: color_dict[color_key][1],
                                                      extension.par_in[1]: color_dict[color_key][2]}))
                    attributes = []
                    attributevalues = {}
                    for i in result.keys():
                        attributes.append(QgsField(i, result[i]['type']))
                        attributevalues.update(provider.fieldNameIndex(i), result[i]['value'])

                    add_attributes_if_not_exists(layer, attributes)
                    provider.changeAttributeValues({feat.id(): attributevalues})


def colors_match_feature(color_quadriple, feature, field_name):
    """
    Check if the given color quadriple contains the same color-values as the feature at the given field_name.
    :param color_quadriple: A color-quadriple in the form [R, G, B, a]
    :type color_quadriple: list
    :param feature: The feater which will be checked against
    :type feature: QgsFeature
    :param field_name: The field name, which needs to be prepended with the appropriate color-suffix
    :type field_name: str
    :return: If the quadriple matches
    :rtype: bool
    """
    match = (((color_quadriple[0]-config.color_match_tolerance) < feature.attribute(field_name + '_R') < (color_quadriple[0]+config.color_match_tolerance)) \
            and ((color_quadriple[1]-config.color_match_tolerance) < feature.attribute(field_name + '_G') < (color_quadriple[1]+config.color_match_tolerance))
            and ((color_quadriple[2]-config.color_match_tolerance) < feature.attribute(field_name + '_B') < (color_quadriple[2]+config.color_match_tolerance))
            and ((color_quadriple[3]-config.color_match_tolerance) < feature.attribute(field_name + '_a') < (color_quadriple[3]+config.color_match_tolerance))
            )

    return match


def add_attributes_if_not_exists(layer, attribute):
    """
    Adds given attributes to a layer's data layer
    if there is no attribute with the same name already.
    :param layer: The layer
    :type layer: QgsVectorLayer
    :param attribute: List with the attributes that shall be appended
    :type attribute: list
    :return:
    :rtype:
    """
    layer.startEditing()
    provider = layer.dataProvider()
    name_map = provider.fieldNameMap()
    for att in attribute:
        if att.name() not in name_map:
            provider.addAttributes([att])
    layer.updateFields()
    layer.commitChanges()
