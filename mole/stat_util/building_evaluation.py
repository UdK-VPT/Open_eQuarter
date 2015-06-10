import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import math
import bld_geometry 
from stat_corr import * 

from qgis.core import *

def isnull(value):
  return type(value) is type(NULL)

def evaluate_building(population_density, 
                      area=NULL, 
                      perimeter= NULL, 
                      height= NULL, 
                      length= NULL, 
                      floors= NULL, 
                      window_ratio= NULL, 
                      year_of_construction=1960, 
                      accumulated_heating_hours=72000,
                      common_walls= NULL):
   # Most buildings have a rectangular floor projection. As the Golden Rule is one of the most common rules 
  # in construction esthetics it seems to make sense to use its ratio for width, length and - if necessary - perimeter estimations.

  ratio_solar_available=0.5
  ratio_solar_installable=0.5
  solar_earnings_per_sqm=3000
  average_heat_demand_per_sqm=120

  print "AREA"
  print area
  if isnull(area): 
    print "AAAAAAARRRRREEEEAAAA IIIISSSSS NUUULLLL"
    return {"FLS_AVG": NULL,
                "WDT_AVG":NULL,
                "LEN_AVG": NULL,
                "HGT_AVG": NULL,
                "VOL_AVG": NULL,
                "AR_BASE": NULL,
                "AR_WALL": NULL,
                "AR_WIND": NULL,
                "AR_ROOF": NULL,
                "AR_ENV1": NULL,
                "AR_ENV2": NULL,
                "AR_LIV": NULL,
                "AR_SOL_AVA": NULL,
                "AR_SOL_INS": NULL,
                "WAL_COM": NULL,
                "RT_WINWALL": NULL,
                "RT_AV1": NULL,
                "RT_AV2": NULL,
                "UP_BASE": NULL,
                "UP_WALL": NULL,
                "UP_WIND": NULL,
                "UP_ROOF": NULL,
                "UC_BASE": NULL,
                "UC_WALL": NULL,
                "UC_WIND": NULL,
                "UC_ROOF": NULL,
                "HLP_BASE": NULL,
                "HLP_WALL": NULL,
                "HLP_WIND": NULL,
                "HLP_ROOF": NULL,
                "HLP_TOT": NULL,
                "HLP_ENV1": NULL,
                "HLP_ENV2": NULL,
                "HLP_LIV": NULL,
                "HLC_BASE": NULL,
                "HLC_WALL": NULL,
                "HLC_WIND": NULL,
                "HLC_ROOF": NULL,
                "HLC_TOT": NULL,
                "HLC_ENV1": NULL,
                "HLC_ENV2": NULL,
                "HLC_LIV":NULL,
                "HD_TOT":NULL,
                "HE_SOL":NULL,
                "HE_SOL_LIV":NULL
                }

  dimensions=bld_geometry.dimensions(area,perimeter,length)
  print 'YOC'
  print year_of_construction
  if isnull(floors):
    floors=5
  if isnull(height):
    building_height = floors * 3.3
  else:
    building_height=height
    
  if isnull(window_ratio):
    window_ratio=window_wall_ratio_AVG_by_building_age_lookup.get(year_of_construction)
 
  if isnull(common_walls):
    common_walls=common_walls_by_population_density_corr.get(population_density)
  base_area=dimensions["AREA"]
  base_uvalue_pres=present_base_uvalue_AVG_by_building_age_lookup.get(year_of_construction)
  base_uvalue_contemp=contemporary_base_uvalue_by_building_age_lookup.get(year_of_construction)
  base_loss_pres=base_area*base_uvalue_pres*0.6*accumulated_heating_hours/1000
  base_loss_contemp=base_area*base_uvalue_contemp*0.6*accumulated_heating_hours/1000
  
  wall_area=(dimensions["PERIMETER"]-common_walls*dimensions["WIDTH"])*building_height*(1-window_ratio)
  wall_uvalue_pres=present_wall_uvalue_AVG_by_building_age_lookup.get(year_of_construction)
  wall_uvalue_contemp=contemporary_wall_uvalue_by_building_age_lookup.get(year_of_construction)
  wall_loss_pres=wall_area*wall_uvalue_pres*accumulated_heating_hours/1000
  wall_loss_contemp=wall_area*wall_uvalue_contemp*accumulated_heating_hours/1000
  
  window_area=(dimensions["PERIMETER"]-common_walls*dimensions["WIDTH"])*building_height*window_ratio
  window_uvalue_pres=present_window_uvalue_AVG_by_building_age_lookup.get(year_of_construction)
  window_uvalue_contemp=contemporary_window_uvalue_by_building_age_lookup.get(year_of_construction)
  window_loss_pres=window_area*window_uvalue_pres*accumulated_heating_hours/1000
  window_loss_contemp=window_area*window_uvalue_contemp*accumulated_heating_hours/1000
  
  roof_area=dimensions["AREA"]
  roof_uvalue_pres=present_roof_uvalue_AVG_by_building_age_lookup.get(year_of_construction)
  roof_uvalue_contemp=contemporary_roof_uvalue_by_building_age_lookup.get(year_of_construction)
  roof_loss_pres=roof_area*roof_uvalue_pres*accumulated_heating_hours/1000
  roof_loss_contemp=roof_area*roof_uvalue_contemp*accumulated_heating_hours/1000
  
  total_loss_pres=base_loss_pres+wall_loss_pres+window_loss_pres+roof_loss_pres
  total_loss_contemp=base_loss_contemp+wall_loss_contemp+window_loss_contemp+roof_loss_contemp
  volume=dimensions["AREA"]*building_height
  envelope1=2*dimensions["AREA"]+dimensions["PERIMETER"]*building_height
  envelope2=  wall_area+base_area+window_area+roof_area
  living_area=floors * base_area * 0.8
  return {"FLS_AVG": floors,
              "WDT_AVG":dimensions["WIDTH"],
              "LEN_AVG":dimensions["LENGTH"],
              "HGT_AVG":building_height,
              "VOL_AVG": volume,
              "AR_BASE":base_area,
              "AR_WALL":wall_area,
              "AR_WIND":window_area,
              "AR_ROOF":roof_area,
              "AR_ENV1":envelope1,
              "AR_ENV2":envelope2,
              "AR_LIV": living_area,
              "AR_SOL_AVA": roof_area * ratio_solar_available,
              "AR_SOL_INS": roof_area * ratio_solar_available * ratio_solar_installable,
              "WAL_COM":common_walls,
              "RT_WINWALL":window_ratio,
              "RT_AV1":envelope1/volume,
              "RT_AV2":envelope2/volume,
              "UP_BASE":base_uvalue_pres,
              "UP_WALL":wall_uvalue_pres,
              "UP_WIND":window_uvalue_pres,
              "UP_ROOF":roof_uvalue_pres,
              "UC_BASE":base_uvalue_contemp,
              "UC_WALL":wall_uvalue_contemp,
              "UC_WIND":window_uvalue_contemp,
              "UC_ROOF":roof_uvalue_contemp,
              "HLP_BASE":base_loss_pres,
              "HLP_WALL":wall_loss_pres,
              "HLP_WIND":window_loss_pres,
              "HLP_ROOF":roof_loss_pres,
              "HLP_TOT":total_loss_pres,
              "HLP_ENV1":total_loss_pres/envelope1,
              "HLP_ENV2":total_loss_pres/envelope2,
              "HLP_LIV":total_loss_pres/living_area,
              "HLC_BASE":base_loss_contemp,
              "HLC_WALL":wall_loss_contemp,
              "HLC_WIND":window_loss_contemp,
              "HLC_ROOF":roof_loss_contemp,
              "HLC_TOT":total_loss_contemp,
              "HLC_ENV1":total_loss_contemp/envelope1,
              "HLC_ENV2":total_loss_contemp/envelope2,
              "HLC_LIV":total_loss_contemp/living_area,
              "HD_TOT": average_heat_demand_per_sqm  * living_area,
              "HE_SOL": solar_earnings_per_sqm * roof_area * ratio_solar_available * ratio_solar_installable,
              "HE_SOL_LIV":solar_earnings_per_sqm * roof_area * ratio_solar_available * ratio_solar_installable/living_area
              }

