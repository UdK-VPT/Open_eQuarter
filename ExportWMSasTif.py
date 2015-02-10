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
import numpy
import GdalUtils
import os
import subprocess
import platform
import time

# Import self-written packages
import LayerInteraction


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
        self.active_layer = None

        # Information to find the file on disk
        self.export_name = 'Investigation Area'
        self.path_to_file = ''

        # Data needed for geo-referencing
        self.crs = ''
        self.ulx = numpy.float64(0)
        self.uly = numpy.float64(0)
        self.lrx = numpy.float64(0)
        self.lry = numpy.float64(0)
        self.transformed_extent = QgsRectangle()

        # Source url of the wms file
        self.src_url = ''

        # max width of output file
        self.max_res = 2064

        # pyramid configuration
        self.number_of_pyramids = 4
        self.res_algorithm = 'gauss'

        return

    #ToDo Deal with bug resulting from different crs
    def export(self, clipped_raster_name = 'Investigation Area'):
        """
        Put the steps necessary for the export together in one procedure
        :return:
        :rtype:
        """

        if not clipped_raster_name.isspace() and clipped_raster_name != self.export_name:
            self.export_name = clipped_raster_name

        self.active_layer = self.iface.activeLayer()
        self.canvas = self.iface.mapCanvas()

        if not isinstance(self.active_layer, QgsRasterLayer):
            QMessageBox.information(self.iface.mainWindow(), 'Info', 'The selected layer is not a raster layer and can not be clipped! \n Make sure to select a raster layer for clipping.')
            return None

        else:

            if self.active_layer is None or self.canvas is None:
                #ToDo
                QMessageBox.information(self.iface.mainWindow(), 'Info', 'Please select a layer.')
                return None
            else:

                self.path_to_file = QgsProject.instance().readPath('./') + '/'

                # Get the geo-values from url, hence they need to be added to the clipped layer at the end of the process
                self.src_url, self.crs, self.ulx, self.uly, self.lrx, self.lry = self.get_geo_data()

                if not self.src_url or self.src_url.isspace():
                    #ToDo
                    QMessageBox.information(self.iface.mainWindow(), 'Info', 'Url is missing.')
                    return None

                # check if a crs-string was found and if a Qgs-Object can be created from that string
                if not self.crs or self.crs.isspace() or not QgsCoordinateReferenceSystem().createFromUserInput(self.crs):
                    #ToDo
                    QMessageBox.information(self.iface.mainWindow(), 'Info', 'Crs is missing.')
                    return None

                info_text = 'The current extent will now be clipped. This may take some time.'
                QMessageBox.information(self.iface.mainWindow(), 'Info',info_text)

                create_geo_reference = True
                # Start calculating export files
                layer_name = self.create_multiple_rasters(1, create_geo_reference, 6)

                return layer_name

    def get_geo_data(self):
        """
        Return the data needed to geo-reference the snapshot of the current view after saving.

        :return url: The url to the wms-server
        :rtype url: str

        :return wms_crs: The coordinate reference system, which is currently in use
        :rtype wms_crs: str

        :return upper_left_x: The x value of the current extents upper left corner
        :rtype upper_left_x: int

        :return upper_left_y: The y value of the current extents upper left corner
        :rtype upper_left_y: int

        :return lower_right_x: The x value of the current extents lower right corner
        :rtype lower_right_x: int

        :return lower_right_x: The y value of the current extents lower right corner
        :rtype lower_right_y: int
         """

        # get layers source information
        src = self.active_layer.source()

        # extract the current crs from layer-source
        wms_crs = ''
        start = src.find('crs=')
        if start > -1:
            start += 4
            end = src.find('&', start)
            if end > -1:
                wms_crs = src[start:end]
            else:
                wms_crs = src[start:]

        # extract the wms source-url from layer-source
        url = ''
        start = src.find('url=')
        if start > -1:
            start += 4
            end = src.find('&', start)
            if end > -1:
                url = src[start:end]
            else:
                url = src[start:]

        # get the currently viewed coordinate range and crs
        view_extent = self.canvas.extent()
        current_crs = self.canvas.mapSettings().destinationCrs()
        target_crs = QgsCoordinateReferenceSystem(wms_crs)

        # check if the extent coresponds to the same crs as the map on the server
        if not current_crs == target_crs:
            # set extent, by transforming the formerly saved extent to new Projection
            coord_transformer = QgsCoordinateTransform(current_crs, target_crs)
            view_extent = coord_transformer.transform(view_extent)

        self.transformed_extent = view_extent

        upper_left_x = self.transformed_extent.xMinimum()
        upper_left_y = self.transformed_extent.yMaximum()
        lower_right_x = self.transformed_extent.xMaximum()
        lower_right_y = self.transformed_extent.yMinimum()

        return url, wms_crs, upper_left_x, upper_left_y, lower_right_x, lower_right_y

    def create_multiple_rasters(self, amount, geo_ref = False, pyramids = 0):
        """
        Calculate the amount and the resolution of the pyramids based on the number of pyramids requested

        :type amount: int
        :param amount: number of pyramids, that will be created
        :return:
        :rtype: none
        """

        # calculate the extents width and height
        extent_width = numpy.float64(numpy.abs(self.lrx) - numpy.abs(self.ulx))
        extent_height = numpy.float64(numpy.abs(self.uly) - numpy.abs(self.lry))

        # calculate the missing value (width or height) of the output file, based on the extent
        resolution = dict()

        if extent_width >= extent_height:
            height_as_dec = numpy.float64(self.max_res) / extent_width * extent_height
            resolution['width'] = self.max_res
            resolution['height'] = int(height_as_dec)
        else:
            width_as_dec = numpy.float64(self.max_res) / extent_height * extent_width
            resolution['width'] = int(width_as_dec)
            resolution['height'] = self.max_res

        # append the resolution to the filename and call the save method
        filename = self.path_to_file + self.export_name + '-' + str(resolution['width']) + '_' + str(resolution['height'])
        filename = self.save_image(resolution['width'], resolution['height'], filename)

        # check if the image was saved to disk
        if not filename or filename.isspace():
            #ToDo
            QMessageBox.information(self.iface.mainWindow(), 'Info', 'Could not save image.')
            return

        # the image was created and shall get geo-referenced
        elif geo_ref:
            # setup the MacOSX path to both GDAL executables and python modules
            if platform.system() == 'Darwin':
                GdalUtils.setMacOSXDefaultEnvironment()

            environment = GdalUtils.setProcessEnvironment()
            dest_filename = os.path.splitext(filename)[0] + '_geo.tif'

            # wait until the file exists to add geo-references
            while not os.path.exists(filename):
                time.sleep(0.3)


            referencing = self.add_geo_reference(filename, dest_filename, self.crs, self.ulx, self.uly, self.lrx, self.lry, environment)

            if referencing != 0:
                print 'Error number {} occured, while referencing the output .tif'.format(referencing)

            if pyramids > 0:
                # wait until the geo-referenced file was created before building pyramids
                while not os.path.exists(dest_filename):
                    time.sleep(0.1)
                building_pyramids = self.build_pyramids(dest_filename, self.res_algorithm, self.number_of_pyramids, environment)

                if building_pyramids != 0:
                    print 'Error number {} occured, while building pyramids.'.format(building_pyramids)

            # remove the formerly created, non-georeferenced .tif-file
            os.remove(filename)

        # once the layer was created, open in QGIS
        recent_file = os.path.splitext(filename)[0]
        recent_file_name = recent_file + '_geo.tif'
        recent_file_desc_name = recent_file.split('/')[-1]

        while not os.path.exists(recent_file_name):
            time.sleep(0.2)

        if not self.crs or self.crs.isspace() or not QgsCoordinateReferenceSystem().createFromUserInput(self.crs):
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

        rlayer.setCrs(QgsCoordinateReferenceSystem(self.crs))
        QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        self.canvas.refresh()
        # restore former settings
        QSettings().setValue('/Projections/defaultBehaviour', old_validation)

        return recent_file_desc_name

    def save_image(self, width, height, filename='export'):
        """
        Select and save the currently visible extent to a .tif file

        :param width: image width
        :type width: int

        :param height: image height
        :type height: int

        :param name: name of the created file
        :type name: str

        :return:
        :rtype: none
        """
        image_type = 'tif'

        # set image's background color and format
        img_color = QColor(255, 255, 255)
        img_format = QImage.Format_ARGB32_Premultiplied

        # create image
        img = self.active_layer.previewAsImage(QSize(width, height), img_color, img_format)

        # create painter
        painter = QPainter()
        painter.begin(img)
        painter.setRenderHint(QPainter.Antialiasing)

        # set layer set
        renderer = QgsMapRenderer()
        layer_set = []
        layer_set.append(self.active_layer.id())
        renderer.setLayerSet(layer_set)

        # set extent to currently visible extent
        renderer.setExtent(self.transformed_extent)

        # set output size
        renderer.setOutputSize(img.size(), img.logicalDpiX())

        # do the rendering
        renderer.render(painter)

        painter.end()
        # save image
        save_as = filename + '.' + image_type
        if img.save(save_as, image_type):
            return save_as

        return ''

    def add_geo_reference(self, file, dst_filename, crs, ulx, uly, lrx, lry, environment):
        """
        Call the gdal_translate command and add the missing geo-information.

        :param file: The file (in the format "/folder/subfolder/filename.tif") that needs to be referenced
        :type file: str

        :param crs: The destination coordinate reference system
        :type crs: str

        :param ulx: The x-coordinate of the upper left image border
        :type ulx: int

        :param uly: The y-coordinate of the upper left image border
        :type uly: int

        :param lrx: The x-coordinate of the lower right image border
        :type lrx: int

        :param lry: The y-coordinate of the lower right image border
        :type lry: int

        :return:
        :rtype: none
        """

        cmd = ['gdal_translate', '-a_srs', crs, '-a_ullr', repr(ulx), repr(uly), repr(lrx), repr(lry), str(file.encode('utf-8')),
               str(dst_filename.encode('utf-8'))]

        # Error code 127 corresponds to 'command not found'
        gdal_process = subprocess.Popen(cmd, env=environment)

        #ToDo Add timeout function
        return gdal_process.wait()

    def build_pyramids(self, file, sampling_algorithm, amount, environment):

        pyramids = []
        for i in range(1,amount+1):
            pyramids.append(str(2**i))

        cmd = ['gdaladdo', '-r', sampling_algorithm, file] + pyramids

        gdaladdo = subprocess.Popen(cmd, env=environment)

        #ToDo Add timeout function
        return gdaladdo.wait()


