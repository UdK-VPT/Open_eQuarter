# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OpenEQuartersMain
                                 A QGIS plugin
 The plugin automates the setup for investigating an area.
                             -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 by Kim Gülle / UdK-Berlin
        email                : kimonline@example.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
#add the gdal_path to the environment
import platform
import os
if platform.system() == 'Darwin':
    os.environ['PATH'] += ":"+"/Library/Frameworks/GDAL.framework/Versions/1.11/Programs"

def classFactory(iface):
    # load OpenEQuarterMain class from file open_equarter_main
    from .open_equarter_main import OpenEQuarterMain
    return OpenEQuarterMain(iface)
