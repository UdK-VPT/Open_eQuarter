# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenEQuarterMain
                                 A QGIS plugin
 The plugin automates the setup for investigating an area.
                              -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : kimonline@posteo.de
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

from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsVectorFileWriter
from qgis.core import QgsProject, QgsMapLayer, QgsMapRendererJob, QgsProject, QgsField
from qgis.core.processing import QgsOverlayUtils
from qgis.PyQt.QtCore import QSettings, QSize, QVariant
from qgis.PyQt.QtGui import QPainter, QColor, QImage, QProgressDialog, QLabel
import os
import time
from string import find
from mole.project import config
from mole import oeq_global
