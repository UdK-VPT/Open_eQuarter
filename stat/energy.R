#####################################################################################################################
#                                                                                                                   
# Project:      Open eQuarter 
#
# Part:         STAT: Energetic Predictions
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         21.10.2014
#
# Descrription: 
# The investigation of Open eQuarter Stat is drawing on the results of the demographic survey "Zensus 2011" 
# conducted by the Federal Statistical Office of Germany in 2011. This module includes functions to
# dig for correlations
#
######################################################################################################################
# basic includes
source("config/plotpalettes.R")
source("init.R")
source("mun_db.R")
source("bld_db.R")

#Predict the energy demand for heating based on only a few basic data
energy_demand<-function(population_density, #parameter Type & Fensteranteil
                        

#Predict the energy demand for heating based on only a few basic data
energy_demand<-function(population_density, #parameter Type & Fensteranteil
                        floor_area,
                        floor_perimeter=NULL,
                        building_height=NULL,
                        floors=3,
                        window_ratio=0.2, #window ration for each direction
                        year_of_construction=1960,
                        accumulated_heating_hours=80000
){
  l.goldencut=1.618034
  if(is.null(floor_perimeter)) floor_perimeter=2*sqrt(floor_area*1.618034)+2*sqrt(floor_area/1.618034)
  if(is.null(building_height)) {
    if(is.null(floors)){
     # floors=building_floors_distribution(population_density)
      building_height=building_height_distribution(population_density)
    }else{
      building_height=floors*3.3
    }
  }else{
    floors=building_height/3.3
  }
  l.type_distribution=build_type_distribution_by_population_density(population_density)
  #l.uvalues=component_uvalues(year_of_construction)
  
  l.base_area=floor_area
  l.base_uvalue=l.type_distribution$EFH*l.uvalues$U_BASE_EFH+
    l.type_distribution$DH*l.uvalues$U_BASE_RH+
    l.type_distribution$MFH*l.uvalues$U_BASE_MFH+
    l.type_distribution$GMH*l.uvalues$U_BASE_GMH
  l.base_loss=l.base_area*l.base_uvalue*accumulated_heating_hours
  
  l.wall_area=floor_perimeter*building_height
  l.wall_uvalue=l.type_distribution$EFH*l.uvalues$U_WALL_EFH+
    l.type_distribution$DH*l.uvalues$U_WALL_RH+
    l.type_distribution$MFH*l.uvalues$U_WALL_MFH+
    l.type_distribution$GMH*l.uvalues$U_WALL_GMH
  l.wall_loss=l.wall_area*l.wall_uvalue*accumulated_heating_hours
  
  l.roof_area=floor_area
  l.roof_uvalue=l.type_distribution$EFH*l.uvalues$U_ROOF_EFH+
    l.type_distribution$DH*l.uvalues$U_ROOF_RH+
    l.type_distribution$MFH*l.uvalues$U_ROOF_MFH+
    l.type_distribution$GMH*l.uvalues$U_ROOF_GMH
  l.roof_loss=l.roof_area*l.roof_uvalue*accumulated_heating_hours
  
  l.volume=floor_area*building_height
  l.envelope=l.wall_area+l.roof_area+l.base_area
  
  l.total_loss=l.wall_loss+l.roof_loss+l.base_loss
  l.loss_per_living_area=l.total_loss/floor_area/floors
  return(list(BASE_AREA=floor_area,FLOORS=floors,
              LENGTH=round(sqrt(floor_area*1.618034),2),
              WIDTH=round(sqrt(floor_area/1.618034),2),
              HEIGHT=round(building_height,2),
              PERIMETER=round(floor_perimeter,2),
              VOLUME=round(l.volume,2),
              ENVELOPE=round(l.envelope,2),
              AV_RELATION=round(l.volume/l.envelope,2),
              HEATLOSS_PER_LIVING_AREA=trunc(l.loss_per_living_area/1000),
              HEATLOSS_PER_VOLUME=l.total_loss/l.volume/1000,
              rbind(BASE=list(AREA=l.base_area,UVALUE=l.base_uvalue,
                              TOTAL_HEATLOSS=l.base_loss/1000,HEATLOSS_PER_AREA=l.base_loss/l.base_area/1000),
                    WALL=list(AREA=l.wall_area,UVALUE=l.base_uvalue,
                              TOTAL_HEATLOSS=l.wall_loss/1000,HEATLOSS_PER_AREA=l.wall_loss/l.wall_area/1000),
                    ROOF=list(AREA=l.roof_area,UVALUE=l.roof_uvalue,
                              TOTAL_HEATLOSS=l.roof_loss/1000,HEATLOSS_PER_AREA=l.roof_loss/l.roof_area/1000),
                    ROOF=list(AREA=l.envelope,UVALUE=(l.roof_uvalue*l.roof_area+l.wall_uvalue*l.wall_area+l.base_uvalue*l.base_area)/l.envelope,
                              TOTAL_HEATLOSS=l.total_loss/1000,HEATLOSS_PER_AREA=l.total_loss/l.envelope/1000)
                    )
              )
         )
}


