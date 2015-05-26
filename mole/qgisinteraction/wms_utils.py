from PyQt4.QtGui import QMessageBox
from qgis.core import QgsProject

import qgis
import os
import time

from mole.qgisinteraction import raster_layer_interaction
from mole.qgisinteraction import layer_interaction


def save_wms_extent_as_image(wms_layer_name, max_res = 2064, geo_reference_output = True):

    export_wms_layer = layer_interaction.find_layer_by_name(wms_layer_name)
    iface = qgis.utils.iface
    canvas = iface.mapCanvas()

    current_crs = canvas.mapSettings().destinationCrs()
    current_extent = canvas.extent()
    export_extent = raster_layer_interaction.transform_wms_geo_data(export_wms_layer, current_extent, current_crs)

    info_text = 'The current extent will now be clipped. This may take some time.'
    QMessageBox.information(iface.mainWindow(), 'Info', info_text)

    path_to_file = os.path.normpath(QgsProject.instance().readPath('./'))
    filename = layer_interaction.save_layer_as_image(export_wms_layer, export_extent, path_to_file, max_res)

    if geo_reference_output:
        # wait until the file exists to add geo-references
        no_timeout = 30
        while not os.path.exists(filename) and no_timeout:
            time.sleep(0.1)
            no_timeout -= 1

        dest_filename = os.path.splitext(filename)[0] + '_geo.tif'
        referencing = raster_layer_interaction.gdal_translate_layerfile(filename, dest_filename, current_crs.authid(), current_extent)

        if referencing != 0:
            print 'Error number {} occured, while referencing the output .tif'.format(referencing)
        else:
            os.remove(filename)
            filename = dest_filename

    return filename