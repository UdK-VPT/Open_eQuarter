# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Open eQuarter MOLE
        A QGIS plugin: Automated building data akquisition
                              -------------------
        begin                : 2014-10-07
        copyright            : (C) 2014 VPT UdK-Berlin
        email                : werner.kaul@udk-berlin.de,kimonline@posteo.de
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


# class definition Quarter

class OeQ_Quarter:
    def __init__(self, iface):
        self.layername = NULL
        self.featurelist = []
        self.Area = 0
        self.Inhabitants = 0
        self.PopulationDensity = 0
        self.BuildingList = []

    def add_building(self, building):
        self.BuildingList.append(building)
