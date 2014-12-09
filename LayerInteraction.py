from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsVectorFileWriter, QgsMapLayerRegistry
from PyQt4.QtCore import QSettings
from os import path


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

        for layer_key in QgsMapLayerRegistry.instance().mapLayers():

            layer = QgsMapLayerRegistry.instance().mapLayers()[layer_key]
            if layer.name() == layer_name:
                return layer
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

    out_path, out_name = path.split(full_path)

    if out_name.upper().endswith('.SHP'):
        out_name = out_name[:-4]

    if vlayer is not None and path.exists(out_path):

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


def trigger_edit_mode(iface, layer_name, trigger='on'):
    """
    Iterate over all layers and activate the Layer called layer_name. Then toggle the edit mode of that layer.
    :param iface: The Qgis-interface that will be accessed
    :type iface: QgsInterface
    :param layer_name: Name of the layer, that shall be switched to edit_mode
    :type layer_name: str
    :return:
    :rtype:
    """
    if layer_name and not layer_name.isspace():

        edit_layer = find_layer_by_name(layer_name)

        # if the layer was found, it is activated and the editing and the adding of features will be triggered
        if edit_layer is not None:
            iface.setActiveLayer(edit_layer)

            if trigger == 'on':
                iface.actionToggleEditing().trigger()
                iface.actionAddFeature().trigger()
            elif trigger == 'off':
                iface.actionAddFeature().trigger()
                iface.actionToggleEditing().trigger()
