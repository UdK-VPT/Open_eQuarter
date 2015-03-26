# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SaveSelectionWithPyramid
                                 A QGIS plugin
 The plugin saves the current view into a new file and creates the pyramids
                              -------------------
        begin                : 2014-08-14
        copyright            : (C) 2014 by Kim Gülle / UdK Berlin
        email                : kimbim@lim.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Import additional packages
import os
import time

# Import self-written packages
from mole.qgisinteraction import layer_interaction, raster_layer_interaction


class ExportWMSasTif:

    def __init__(self, iface):
        """
        Do a basic setup and connect the program to the QGIS-ui

        :param iface: The QGIS user interface
        :type iface: qgis.core.iface

        :return:
        :rtype: None
        """

        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = None

        # Information to find the file on disk
        self.export_name = 'Investigation Area'
        self.path_to_file = ''

        # max width of output file
        self.max_res = 2064

        # pyramid configuration
        self.number_of_pyramids = 4
        self.res_algorithm = 'gauss'

        return

    #ToDo Deal with bug resulting from different crs - at some point the investigation area is not extracted properly (after export, the IA is displayed approx. 1000m away from the source IA)
    def export(self, clipped_raster_name = 'Investigation Area'):
        """
        Put the steps necessary for the export together in one procedure
        :return:
        :rtype:
        """
        if clipped_raster_name:
            self.export_name = clipped_raster_name

        export_layer = layer_interaction.find_layer_by_name(self.export_name)
        self.canvas = self.iface.mapCanvas()

        if not isinstance(export_layer, QgsRasterLayer):
            error_message = 'The selected layer is not a raster layer and can not be clipped! \n Make sure to select a raster layer for clipping.'
            QMessageBox.information(self.iface.mainWindow(), 'Error', error_message)
            return None

        else:
            # Get the geo-values from url, hence they need to be added to the clipped layer at the end of the process
            raster_url = raster_layer_interaction.get_wms_url(export_layer)

            if not raster_url:
                #ToDo
                QMessageBox.information(self.iface.mainWindow(), 'Error', 'Url of raster "{}" is missing.'.format(clipped_raster_name))
                return None

            crs = raster_layer_interaction.get_wms_crs(export_layer)

            #ToDo replace with proper check
            if not QgsCoordinateReferenceSystem(crs).toProj4():
                #ToDo
                QMessageBox.information(self.iface.mainWindow(), 'Error', 'Crs of raster "{}" is missing.'.format(clipped_raster_name))
                return None

            current_crs = self.canvas.mapSettings().destinationCrs()
            current_extent = self.canvas.extent()
            export_extent = raster_layer_interaction.transform_wms_geo_data(export_layer, current_extent, current_crs)

            info_text = 'The current extent will now be clipped. This may take some time.'
            QMessageBox.information(self.iface.mainWindow(), 'Info',info_text)

            create_geo_reference = True
            # Start calculating export files
            layer_name = self.create_multiple_rasters(export_layer, export_extent, create_geo_reference, 6)

            return layer_name

    def create_multiple_rasters(self, layer, extent, geo_ref=False, pyramids=0):
        """
        Calculate the amount and the resolution of the pyramids based on the number of pyramids requested
        :param extent: The canvas-extent from which the layer will be clipped
        :type extent: QgsRectangle
        :param geo_ref: If the exportet .tif shall be geo-referenced afterwards or not
        :type geo_ref: bool
        :param pyramids: number of pyramids, that will be created
        :type pyramids: int
        :return:
        :rtype: none
        """

        # calculate the extents width and height
        extent_width = extent.width()
        extent_height = extent.height()
        crs = raster_layer_interaction.get_wms_crs(layer)

        # calculate the missing value (width or height) of the output file, based on the extent
        resolution = dict()
        if extent_width >= extent_height:
            height_as_dec = self.max_res / extent_width * extent_height
            resolution['width'] = self.max_res
            resolution['height'] = int(height_as_dec)
        else:
            width_as_dec = self.max_res / extent_height * extent_width
            resolution['width'] = int(width_as_dec)
            resolution['height'] = self.max_res

        # append the resolution to the filename and call the save method
        resolution_postfix = '-{}_{}'.format(resolution['width'], resolution['height'])
        export_name = self.export_name + resolution_postfix
        path_to_file = os.path.normpath(QgsProject.instance().readPath('./'))
        filename = os.path.join(path_to_file, export_name)
        filename = layer_interaction.save_layer_as_image(layer, extent, filename, self.max_res)

        # check if the image was saved to disk
        if not filename or filename.isspace():
            #ToDo
            QMessageBox.information(self.iface.mainWindow(), 'Error', 'Could not save image.')
            return

        else:
            # the image was created and shall get geo-referenced
            if geo_ref:
                # wait until the file exists to add geo-references
                no_timeout = 50
                while not os.path.exists(filename) and no_timeout:
                    time.sleep(0.1)
                    no_timeout -= 1

                dest_filename = os.path.splitext(filename)[0] + '_geo.tif'
                referencing = raster_layer_interaction.gdal_translate_layerfile(filename, dest_filename, crs, extent)

                # remove the formerly created, non-georeferenced .tif-file
                os.remove(filename)

                if referencing != 0:
                    print 'Error number {} occured, while referencing the output .tif'.format(referencing)

                if pyramids > 0:
                    # wait until the geo-referenced file was created before building pyramids
                    no_timeout = 30
                    while not os.path.exists(dest_filename) and no_timeout:
                        time.sleep(0.1)
                        no_timeout -= 1
                    building_pyramids = raster_layer_interaction.gdal_addo_layerfile(dest_filename, self.res_algorithm, pyramids)

                    if building_pyramids != 0:
                        print 'Error number {} occured, while building pyramids.'.format(building_pyramids)

            # once the layer was created, open in QGIS
            recent_file = os.path.splitext(filename)[0]
            recent_file_name = recent_file + '_geo.tif'
            recent_file_desc_name = recent_file.split(os.path.sep)[-1]

            no_timeout = 50
            while not os.path.exists(recent_file_name) and no_timeout:
                time.sleep(0.1)
                no_timeout -= 1

            #ToDo Replace with proper check
            if not QgsCoordinateReferenceSystem(crs).toProj4():
                # crs is not valid
                # save current settings and set Qgis to prompt for CRS
                old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'prompt'))
                QSettings().setValue('/Projections/defaultBehaviour', 'prompt')

            else:
                # crs is a valid crs
                # surpress prompt to chose crs and use project-crs
                old_validation = str(QSettings().value('/Projections/defaultBehaviour', 'useProject'))
                QSettings().setValue('/Projections/defaultBehaviour', 'useProject')

            rlayer = QgsRasterLayer(recent_file_name, recent_file_desc_name)
            if not rlayer.isValid():
                print 'Layer failed to load!'

            rlayer.setCrs(QgsCoordinateReferenceSystem(crs))
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
            self.canvas.refresh()
            # restore former settings
            QSettings().setValue('/Projections/defaultBehaviour', old_validation)

            return recent_file_desc_name