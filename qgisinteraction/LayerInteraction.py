import subprocess
from os import path
from platform import system
import time

from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsVectorFileWriter, QgsMapLayerRegistry, QgsMapLayer, QgsApplication
from PyQt4.QtCore import QSettings
import GdalUtils

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
        shape_layer = QgsVectorLayer(layer_type + crs, layer_name, 'memory', False)
        shape_layer.setProviderEncoding('System')

        # reset appearance of crs-choice dialog to previous settings
        QSettings().setValue('/Projections/defaultBehaviour', old_validation)

        return shape_layer

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
    if layer and path_to_style and path.exists(path_to_style):
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


def hide_or_remove_layer(layer_name, mode='hide', iface = None):
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
    out_path, out_name = path.split(full_path)

    if out_name.upper().endswith('.SHP'):
        out_name = out_name[:-4]

    if vlayer is not None and vlayer.isValid() and path.exists(out_path):

        if path.exists(path.join(out_path, out_name + '.shp')):
            new_name = out_name
            suffix = 0

            while path.exists(path.join(out_path, new_name + '.shp')):
                suffix += 1
                new_name = out_name + str(suffix)

            out_name = new_name

        full_path = path.join(out_path, out_name + '.shp')

        provider = vlayer.dataProvider()
        return_code = QgsVectorFileWriter.writeAsVectorFormat(vlayer, full_path, provider.encoding(), provider.crs(), 'ESRI Shapefile')

        if return_code == QgsVectorFileWriter.NoError:
            vlayer = QgsVectorLayer(full_path, unicode(out_name), "ogr")

            return vlayer

        else:
            return None

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

def get_wms_layer_list(iface, visibility='all'):
    """
    Iterate over all layers and return a list of the currently visible WMS-files.
    :param iface: The Qgis-interface that will be accessed
    :type iface: QgisInterface
    :return: A list containing raster layers with the given visibility-value
    :rtype: list
    """
    active_wms_layers = []
    layer_list = QgsMapLayerRegistry.instance().mapLayers()
    interface = iface.legendInterface()

    if visibility == 'visible':
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and interface.isLayerVisible(layer):
                active_wms_layers.append(layer)

        return active_wms_layers

    elif visibility == 'invisible':
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer and not interface.isLayerVisible(layer):
                active_wms_layers.append(layer)

        return active_wms_layers

    else:
        for key, layer in layer_list.iteritems():
            if layer.type() == QgsMapLayer.RasterLayer:
                active_wms_layers.append(layer)

        return active_wms_layers

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

    if layer_name and not layer_name.isspace():

        zoom_layer = find_layer_by_name(layer_name)

        # if the shapefile was found set the layer active
        if zoom_layer is not None:
            iface.setActiveLayer(zoom_layer)
            iface.actionZoomToLayer().trigger()

def biuniquify_layer_name(layer_name):

    biunique_name = ''
    if layer_name and not layer_name.isspace():

        biunique_name = layer_name
        suffix = 0

        while(find_layer_by_name(biunique_name) is not None):
            biunique_name = layer_name + str(suffix)
            suffix += 1

    return biunique_name

def change_crs_of_layers(layer_list, dest_crs):

    for layer_name in layer_list:
        layer = find_layer_by_name(layer_name)

        if layer and layer.isValid():
            layer.setCrs(dest_crs)

def gdal_warp_layer_list(layer, target_crs):

    try:
        source_crs = layer.crs().toProj4()
        input_path = layer.publicSource()
        input_path = path.normpath(input_path)
        out_path = path.dirname(input_path)
        out_path = path.normpath(out_path)
        out_path = path.join(out_path, layer.name() + '_transformed.tif')

        # setup the MacOSX path to both GDAL executables and python modules
        if system() == 'Darwin':
            GdalUtils.setMacOSXDefaultEnvironment()

        environment = GdalUtils.setProcessEnvironment()

        if system() == 'Windows':
            # The gdal-processing executables are located at <QGIS Installation folder>\bin
            # The gcs.csv-file (required as a GDAL_DATA env-var) is stored in <QGIS Installation folder>\share\gdal
            # The projection files (required as a PROJ_LIB env-var) are stored in <QGIS Installation folder>\share\proj
            # prefixPath() returns <QGIS Installation folder>\apps\qgis
            gdal_location = path.join(QgsApplication.prefixPath(), '..', '..', 'bin')
            gdal_data = path.join(QgsApplication.prefixPath(), '..', '..', 'share', 'gdal')
            gdal_python_tools = path.join(QgsApplication.prefixPath(), 'python', 'plugins', 'GdalTools')
            gdal_projection = path.join(QgsApplication.prefixPath(), '..', '..', 'share', 'proj')
            environment['PATH'] = str(path.abspath(gdal_location))
            environment['PYTHONPATH'] = str(path.abspath(gdal_python_tools))
            environment['GDAL_DATA'] = str(path.abspath(gdal_data))
            environment['PROJ_LIB'] = str(path.abspath(gdal_projection))

        # wait until the file exists to add geo-references
        while not path.exists(input_path):
            time.sleep(0.1)

        cmd = ['gdalwarp', '-s_srs', str(source_crs),'-t_srs', str(target_crs), input_path, out_path]

        gdalwarp = subprocess.Popen(cmd, env=environment)

        #ToDo Add timeout function
        return gdalwarp.wait()
    except AttributeError as Att_Error:
        print(Att_Error.message)





