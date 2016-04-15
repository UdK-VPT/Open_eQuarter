# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Buildings(models.Model):
    buildingid = models.IntegerField(db_column='buildingID', primary_key=True)  # Field name made lowercase.
    buildingtoken = models.CharField(db_column='buildingToken', max_length=200, primary_key=True)  # Field name made lowercase.
    version = models.IntegerField(primary_key=True)
    datasource = models.CharField(max_length=200, primary_key=True)
    buildingname = models.CharField(db_column='buildingName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=2000, blank=True, null=True)
    associatedproject = models.CharField(db_column='associatedProject', max_length=200, blank=True, null=True)  # Field name made lowercase.
    quarter = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    housenumber = models.CharField(db_column='houseNumber', max_length=200, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.IntegerField(db_column='ZIPcode', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    climate = models.CharField(max_length=200, blank=True, null=True)
    weatherexposure = models.CharField(db_column='weatherExposure', max_length=200, blank=True, null=True)  # Field name made lowercase.
    yearofcompletion = models.IntegerField(db_column='yearOfCompletion', blank=True, null=True)  # Field name made lowercase.
    monumentalprotection = models.CharField(db_column='monumentalProtection', max_length=200, blank=True, null=True)  # Field name made lowercase.
    buildingtype = models.CharField(db_column='buildingType', max_length=200, blank=True, null=True)  # Field name made lowercase.
    architecture = models.CharField(max_length=200, blank=True, null=True)
    cubatur = models.CharField(max_length=200, blank=True, null=True)
    owner = models.CharField(max_length=200, blank=True, null=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    utilization = models.CharField(max_length=200, blank=True, null=True)
    structuralstate = models.CharField(db_column='structuralState', max_length=200, blank=True, null=True)  # Field name made lowercase.
    technicalstate = models.CharField(db_column='technicalState', max_length=200, blank=True, null=True)  # Field name made lowercase.
    developmentpotential = models.CharField(db_column='developmentPotential', max_length=200, blank=True, null=True)  # Field name made lowercase.
    buildingcategorybwz = models.IntegerField(db_column='buildingCategoryBWZ', blank=True, null=True)  # Field name made lowercase.
    buildingageclass = models.CharField(db_column='buildingAgeClass', max_length=8, blank=True, null=True)  # Field name made lowercase.
    usablefloorspacenf = models.FloatField(db_column='usableFloorSpaceNF', blank=True, null=True)  # Field name made lowercase.
    heatedfloorspacengf = models.FloatField(db_column='heatedFloorSpaceNGF', blank=True, null=True)  # Field name made lowercase.
    grossfloorareabgf = models.FloatField(db_column='grossFloorAreaBGF', blank=True, null=True)  # Field name made lowercase.
    buildinggroundarea = models.FloatField(db_column='buildingGroundArea', blank=True, null=True)  # Field name made lowercase.
    avgbuildingheight = models.FloatField(db_column='avgBuildingHeight', blank=True, null=True)  # Field name made lowercase.
    numberoffloors = models.IntegerField(db_column='numberOfFloors', blank=True, null=True)  # Field name made lowercase.
    enclosedvolume = models.FloatField(db_column='enclosedVolume', blank=True, null=True)  # Field name made lowercase.
    wall1area = models.FloatField(db_column='wall1Area', blank=True, null=True)  # Field name made lowercase.
    wall1azimuth = models.FloatField(db_column='wall1Azimuth', blank=True, null=True)  # Field name made lowercase.
    wall2area = models.FloatField(db_column='wall2Area', blank=True, null=True)  # Field name made lowercase.
    wall2azimuth = models.FloatField(db_column='wall2Azimuth', blank=True, null=True)  # Field name made lowercase.
    wall3area = models.FloatField(db_column='wall3Area', blank=True, null=True)  # Field name made lowercase.
    wall3azimuth = models.FloatField(db_column='wall3Azimuth', blank=True, null=True)  # Field name made lowercase.
    wall4area = models.FloatField(db_column='wall4Area', blank=True, null=True)  # Field name made lowercase.
    wall4azimuth = models.FloatField(db_column='wall4Azimuth', blank=True, null=True)  # Field name made lowercase.
    envelopingsurface = models.FloatField(db_column='envelopingSurface', blank=True, null=True)  # Field name made lowercase.
    windowarea = models.FloatField(db_column='windowArea', blank=True, null=True)  # Field name made lowercase.
    windowwallratio = models.FloatField(db_column='windowWallRatio', blank=True, null=True)  # Field name made lowercase.
    avgthicknessouterwall = models.FloatField(db_column='avgThicknessOuterWall', blank=True, null=True)  # Field name made lowercase.
    avgthicknessinnerwall = models.FloatField(db_column='avgThicknessInnerWall', blank=True, null=True)  # Field name made lowercase.
    avgthicknessinsulation = models.FloatField(db_column='avgThicknessInsulation', blank=True, null=True)  # Field name made lowercase.
    materialouterwall = models.CharField(db_column='materialOuterWall', max_length=200, blank=True, null=True)  # Field name made lowercase.
    materialinnerwall = models.CharField(db_column='materialInnerWall', max_length=200, blank=True, null=True)  # Field name made lowercase.
    materialinsulation = models.CharField(db_column='materialInsulation', max_length=200, blank=True, null=True)  # Field name made lowercase.
    materialwindowframe = models.CharField(db_column='materialWindowFrame', max_length=200, blank=True, null=True)  # Field name made lowercase.
    materialwindowglazing = models.CharField(db_column='materialWindowGlazing', max_length=200, blank=True, null=True)  # Field name made lowercase.
    basematerial = models.CharField(db_column='baseMaterial', max_length=200, blank=True, null=True)  # Field name made lowercase.
    avguvalue = models.FloatField(db_column='avgUvalue', blank=True, null=True)  # Field name made lowercase.
    cellar = models.CharField(max_length=2, blank=True, null=True)
    externalshading = models.CharField(db_column='externalShading', max_length=200, blank=True, null=True)  # Field name made lowercase.
    heating = models.CharField(max_length=2, blank=True, null=True)
    cooling = models.CharField(max_length=2, blank=True, null=True)
    centralizedcoolingsystem = models.CharField(db_column='centralizedCoolingSystem', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ahu = models.CharField(db_column='AHU', max_length=2, blank=True, null=True)  # Field name made lowercase.
    absorptionchiller = models.CharField(db_column='absorptionChiller', max_length=2, blank=True, null=True)  # Field name made lowercase.
    computercenter = models.CharField(db_column='computerCenter', max_length=2, blank=True, null=True)  # Field name made lowercase.
    laboratory = models.CharField(max_length=2, blank=True, null=True)
    serverroomwiringcenter = models.CharField(db_column='serverRoomWiringCenter', max_length=2, blank=True, null=True)  # Field name made lowercase.
    heatenergysource = models.CharField(db_column='heatEnergySource', max_length=200, blank=True, null=True)  # Field name made lowercase.
    heatingsystem = models.CharField(db_column='heatingSystem', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    coolingsystem = models.CharField(db_column='coolingSystem', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    ventilationsystem = models.CharField(db_column='ventilationSystem', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    lightingsystem = models.CharField(db_column='lightingSystem', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    reasonsforhighconsumption = models.CharField(db_column='reasonsForHighConsumption', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    renovationmeasures = models.CharField(db_column='renovationMeasures', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    districtcoolingpower = models.FloatField(db_column='districtCoolingPower', blank=True, null=True)  # Field name made lowercase.
    districtcoolingtransferstationname = models.CharField(db_column='districtCoolingTransferStationName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    districtheatingvariabletemppower = models.FloatField(db_column='districtHeatingVariableTempPower', blank=True, null=True)  # Field name made lowercase.
    districtheatingconstanttemppower = models.FloatField(db_column='districtHeatingConstantTempPower', blank=True, null=True)  # Field name made lowercase.
    districtheatingtransferstationname = models.CharField(db_column='districtHeatingTransferStationName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    transferstationcoordinatex = models.FloatField(db_column='transferStationCoordinateX', blank=True, null=True)  # Field name made lowercase.
    transferstationcoordinatey = models.FloatField(db_column='transferStationCoordinateY', blank=True, null=True)  # Field name made lowercase.
    ratiousetransferstation = models.FloatField(db_column='ratioUseTransferStation', blank=True, null=True)  # Field name made lowercase.
    solarthermalmodularea = models.FloatField(db_column='solarThermalModulArea', blank=True, null=True)  # Field name made lowercase.
    pvproduction = models.FloatField(db_column='PVProduction', blank=True, null=True)  # Field name made lowercase.
    pvmoduleareabestsuited = models.FloatField(db_column='PVModuleAreaBestSuited', blank=True, null=True)  # Field name made lowercase.
    pvmoduleareawellsuited = models.FloatField(db_column='PVModuleAreaWellSuited', blank=True, null=True)  # Field name made lowercase.
    pvmoduleareasuited = models.FloatField(db_column='PVModuleAreaSuited', blank=True, null=True)  # Field name made lowercase.
    solarmoduleareashadowed = models.FloatField(db_column='solarModuleAreaShadowed', blank=True, null=True)  # Field name made lowercase.
    solarmodulearea = models.FloatField(db_column='solarModuleArea', blank=True, null=True)  # Field name made lowercase.
    roofarea = models.FloatField(db_column='roofArea', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011 = models.FloatField(db_column='heatConsumption2011', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_1 = models.FloatField(db_column='heatConsumption2011_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_2 = models.FloatField(db_column='heatConsumption2011_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_3 = models.FloatField(db_column='heatConsumption2011_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_4 = models.FloatField(db_column='heatConsumption2011_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_5 = models.FloatField(db_column='heatConsumption2011_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_6 = models.FloatField(db_column='heatConsumption2011_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_7 = models.FloatField(db_column='heatConsumption2011_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_8 = models.FloatField(db_column='heatConsumption2011_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_9 = models.FloatField(db_column='heatConsumption2011_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_10 = models.FloatField(db_column='heatConsumption2011_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_11 = models.FloatField(db_column='heatConsumption2011_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2011_12 = models.FloatField(db_column='heatConsumption2011_12', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012 = models.FloatField(db_column='heatConsumption2012', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_1 = models.FloatField(db_column='heatConsumption2012_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_2 = models.FloatField(db_column='heatConsumption2012_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_3 = models.FloatField(db_column='heatConsumption2012_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_4 = models.FloatField(db_column='heatConsumption2012_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_5 = models.FloatField(db_column='heatConsumption2012_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_6 = models.FloatField(db_column='heatConsumption2012_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_7 = models.FloatField(db_column='heatConsumption2012_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_8 = models.FloatField(db_column='heatConsumption2012_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_9 = models.FloatField(db_column='heatConsumption2012_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_10 = models.FloatField(db_column='heatConsumption2012_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_11 = models.FloatField(db_column='heatConsumption2012_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2012_12 = models.FloatField(db_column='heatConsumption2012_12', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013 = models.FloatField(db_column='heatConsumption2013', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_1 = models.FloatField(db_column='heatConsumption2013_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_2 = models.FloatField(db_column='heatConsumption2013_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_3 = models.FloatField(db_column='heatConsumption2013_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_4 = models.FloatField(db_column='heatConsumption2013_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_5 = models.FloatField(db_column='heatConsumption2013_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_6 = models.FloatField(db_column='heatConsumption2013_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_7 = models.FloatField(db_column='heatConsumption2013_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_8 = models.FloatField(db_column='heatConsumption2013_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_9 = models.FloatField(db_column='heatConsumption2013_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_10 = models.FloatField(db_column='heatConsumption2013_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_11 = models.FloatField(db_column='heatConsumption2013_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumption2013_12 = models.FloatField(db_column='heatConsumption2013_12', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011 = models.FloatField(db_column='heatConsumptionHVAC2011', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_1 = models.FloatField(db_column='heatConsumptionHVAC2011_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_2 = models.FloatField(db_column='heatConsumptionHVAC2011_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_3 = models.FloatField(db_column='heatConsumptionHVAC2011_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_4 = models.FloatField(db_column='heatConsumptionHVAC2011_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_5 = models.FloatField(db_column='heatConsumptionHVAC2011_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_6 = models.FloatField(db_column='heatConsumptionHVAC2011_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_7 = models.FloatField(db_column='heatConsumptionHVAC2011_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_8 = models.FloatField(db_column='heatConsumptionHVAC2011_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_9 = models.FloatField(db_column='heatConsumptionHVAC2011_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_10 = models.FloatField(db_column='heatConsumptionHVAC2011_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_11 = models.FloatField(db_column='heatConsumptionHVAC2011_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2011_12 = models.FloatField(db_column='heatConsumptionHVAC2011_12', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012 = models.FloatField(db_column='heatConsumptionHVAC2012', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_1 = models.FloatField(db_column='heatConsumptionHVAC2012_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_2 = models.FloatField(db_column='heatConsumptionHVAC2012_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_3 = models.FloatField(db_column='heatConsumptionHVAC2012_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_4 = models.FloatField(db_column='heatConsumptionHVAC2012_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_5 = models.FloatField(db_column='heatConsumptionHVAC2012_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_6 = models.FloatField(db_column='heatConsumptionHVAC2012_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_7 = models.FloatField(db_column='heatConsumptionHVAC2012_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_8 = models.FloatField(db_column='heatConsumptionHVAC2012_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_9 = models.FloatField(db_column='heatConsumptionHVAC2012_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_10 = models.FloatField(db_column='heatConsumptionHVAC2012_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_11 = models.FloatField(db_column='heatConsumptionHVAC2012_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2012_12 = models.FloatField(db_column='heatConsumptionHVAC2012_12', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013 = models.FloatField(db_column='heatConsumptionHVAC2013', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_1 = models.FloatField(db_column='heatConsumptionHVAC2013_1', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_2 = models.FloatField(db_column='heatConsumptionHVAC2013_2', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_3 = models.FloatField(db_column='heatConsumptionHVAC2013_3', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_4 = models.FloatField(db_column='heatConsumptionHVAC2013_4', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_5 = models.FloatField(db_column='heatConsumptionHVAC2013_5', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_6 = models.FloatField(db_column='heatConsumptionHVAC2013_6', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_7 = models.FloatField(db_column='heatConsumptionHVAC2013_7', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_8 = models.FloatField(db_column='heatConsumptionHVAC2013_8', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_9 = models.FloatField(db_column='heatConsumptionHVAC2013_9', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_10 = models.FloatField(db_column='heatConsumptionHVAC2013_10', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_11 = models.FloatField(db_column='heatConsumptionHVAC2013_11', blank=True, null=True)  # Field name made lowercase.
    heatconsumptionhvac2013_12 = models.FloatField(db_column='heatConsumptionHVAC2013_12', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011 = models.FloatField(db_column='electricityConsumption2011', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_1 = models.FloatField(db_column='electricityConsumption2011_1', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_2 = models.FloatField(db_column='electricityConsumption2011_2', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_3 = models.FloatField(db_column='electricityConsumption2011_3', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_4 = models.FloatField(db_column='electricityConsumption2011_4', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_5 = models.FloatField(db_column='electricityConsumption2011_5', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_6 = models.FloatField(db_column='electricityConsumption2011_6', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_7 = models.FloatField(db_column='electricityConsumption2011_7', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_8 = models.FloatField(db_column='electricityConsumption2011_8', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_9 = models.FloatField(db_column='electricityConsumption2011_9', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_10 = models.FloatField(db_column='electricityConsumption2011_10', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_11 = models.FloatField(db_column='electricityConsumption2011_11', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2011_12 = models.FloatField(db_column='electricityConsumption2011_12', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012 = models.FloatField(db_column='electricityConsumption2012', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_1 = models.FloatField(db_column='electricityConsumption2012_1', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_2 = models.FloatField(db_column='electricityConsumption2012_2', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_3 = models.FloatField(db_column='electricityConsumption2012_3', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_4 = models.FloatField(db_column='electricityConsumption2012_4', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_5 = models.FloatField(db_column='electricityConsumption2012_5', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_6 = models.FloatField(db_column='electricityConsumption2012_6', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_7 = models.FloatField(db_column='electricityConsumption2012_7', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_8 = models.FloatField(db_column='electricityConsumption2012_8', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_9 = models.FloatField(db_column='electricityConsumption2012_9', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_10 = models.FloatField(db_column='electricityConsumption2012_10', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_11 = models.FloatField(db_column='electricityConsumption2012_11', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2012_12 = models.FloatField(db_column='electricityConsumption2012_12', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013 = models.FloatField(db_column='electricityConsumption2013', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_1 = models.FloatField(db_column='electricityConsumption2013_1', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_2 = models.FloatField(db_column='electricityConsumption2013_2', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_3 = models.FloatField(db_column='electricityConsumption2013_3', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_4 = models.FloatField(db_column='electricityConsumption2013_4', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_5 = models.FloatField(db_column='electricityConsumption2013_5', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_6 = models.FloatField(db_column='electricityConsumption2013_6', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_7 = models.FloatField(db_column='electricityConsumption2013_7', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_8 = models.FloatField(db_column='electricityConsumption2013_8', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_9 = models.FloatField(db_column='electricityConsumption2013_9', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_10 = models.FloatField(db_column='electricityConsumption2013_10', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_11 = models.FloatField(db_column='electricityConsumption2013_11', blank=True, null=True)  # Field name made lowercase.
    electricityconsumption2013_12 = models.FloatField(db_column='electricityConsumption2013_12', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'buildings'
        unique_together = (('buildingid', 'buildingtoken', 'version', 'datasource'),)
        verbose_name_plural = 'Buildings'


class Materials(models.Model):
    material = models.CharField(primary_key=True, max_length=200)
    category = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    density = models.FloatField(blank=True, null=True)
    specificheatcapacity = models.FloatField(db_column='specificHeatCapacity', blank=True, null=True)  # Field name made lowercase.
    heatconductivity = models.FloatField(db_column='heatConductivity', blank=True, null=True)  # Field name made lowercase.
    diffusionresistancecoefficient = models.FloatField(db_column='diffusionResistanceCoefficient', blank=True, null=True)  # Field name made lowercase.
    diffusionequivalentairlayerthickness = models.FloatField(db_column='diffusionEquivalentAirLayerThickness', blank=True, null=True)  # Field name made lowercase.
    sorption = models.FloatField(blank=True, null=True)
    freewatersaturation = models.FloatField(db_column='freeWaterSaturation', blank=True, null=True)  # Field name made lowercase.
    waterabsorptioncoefficient = models.FloatField(db_column='waterAbsorptionCoefficient', blank=True, null=True)  # Field name made lowercase.
    openporosity = models.FloatField(db_column='openPorosity', blank=True, null=True)  # Field name made lowercase.
    shortwavetransmissioncoefficient = models.FloatField(db_column='shortWaveTransmissionCoefficient', blank=True, null=True)  # Field name made lowercase.
    shortwaveabsorptioncoefficient = models.FloatField(db_column='shortWaveAbsorptionCoefficient', blank=True, null=True)  # Field name made lowercase.
    shortwavereflectioncoefficient = models.FloatField(db_column='shortWaveReflectionCoefficient', blank=True, null=True)  # Field name made lowercase.
    longwavetransmissioncoefficient = models.FloatField(db_column='longWaveTransmissionCoefficient', blank=True, null=True)  # Field name made lowercase.
    longwaveabsorptioncoefficient = models.FloatField(db_column='longWaveAbsorptionCoefficient', blank=True, null=True)  # Field name made lowercase.
    longwavereflectioncoefficient = models.FloatField(db_column='longWaveReflectionCoefficient', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materials'
        verbose_name_plural = 'Materials'



class Quarters(models.Model):
    quarter = models.CharField(primary_key=True, max_length=200)
    associatedproject = models.CharField(db_column='associatedProject', max_length=200, blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    climate = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quarters'
        verbose_name_plural = 'Quarters'


class SurfacesRaw(models.Model):
    buildingid = models.IntegerField(blank=True, null=True)
    building2id = models.IntegerField(blank=True, null=True)
    normal_vector_id = models.IntegerField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    azimuth = models.FloatField(blank=True, null=True)
    tilt = models.FloatField(blank=True, null=True)
    vector1_id = models.IntegerField()
    vector2_id = models.IntegerField()
    vector3_id = models.IntegerField()
    vector4_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'surfaces_raw'
        unique_together = (('vector1_id', 'vector2_id', 'vector3_id', 'vector4_id'),)
        verbose_name_plural = 'Surfaces (Raw)'


class Usageprofiles(models.Model):
    profilename = models.CharField(db_column='profileName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    hour1 = models.FloatField(blank=True, null=True)
    hour2 = models.FloatField(blank=True, null=True)
    hour3 = models.FloatField(blank=True, null=True)
    hour4 = models.FloatField(blank=True, null=True)
    hour5 = models.FloatField(blank=True, null=True)
    hour6 = models.FloatField(blank=True, null=True)
    hour7 = models.FloatField(blank=True, null=True)
    hour8 = models.FloatField(blank=True, null=True)
    hour9 = models.FloatField(blank=True, null=True)
    hour10 = models.FloatField(blank=True, null=True)
    hour11 = models.FloatField(blank=True, null=True)
    hour12 = models.FloatField(blank=True, null=True)
    hour13 = models.FloatField(blank=True, null=True)
    hour14 = models.FloatField(blank=True, null=True)
    hour15 = models.FloatField(blank=True, null=True)
    hour16 = models.FloatField(blank=True, null=True)
    hour17 = models.FloatField(blank=True, null=True)
    hour18 = models.FloatField(blank=True, null=True)
    hour19 = models.FloatField(blank=True, null=True)
    hour20 = models.FloatField(blank=True, null=True)
    hour21 = models.FloatField(blank=True, null=True)
    hour22 = models.FloatField(blank=True, null=True)
    hour23 = models.FloatField(blank=True, null=True)
    hour24 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usageProfiles'
        verbose_name_plural = 'Usageprofiles'


class Vectors(models.Model):
    id = models.BigIntegerField(primary_key=True)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    class Meta:
        managed = False
        db_table = 'vectors'
        unique_together = (('y', 'x', 'z'),)
        verbose_name_plural = 'Vectors'