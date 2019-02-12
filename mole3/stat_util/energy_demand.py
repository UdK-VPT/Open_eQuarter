import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#print sys.path
import math
from . import bld_geometry
from stat_corr import *

def evaluate_building(population_density,
                      area='NULL',
                      perimeter='NULL',
                      height='NULL',
                      length='NULL',
                      floors=5,
                      window_ratio='NULL',
                      year_of_construction=1960,
                      accumulated_heating_hours=80000,
                      common_walls='NULL'):
   # Most buildings have a rectangular floor projection. As the Golden Rule is one of the most common rules
  # in construction esthetics it seems to make sense to use its ratio for width, length and - if necessary - perimeter estimations.
  dimensions=bld_geometry.dimensions(area,perimeter,length)
  if height=='NULL':
    if floors==0: floors=5
    building_height=floors*3.3
  else:
    floors=building_height/3.3

  if window_ratio=='NULL':
    window_ratio=window_wall_ratio_AVG_by_building_age_lookup.get(year_of_construction)

  if common_walls=='NULL':
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

  return {"WDT_AVG":dimensions["WIDTH"],
              "LEN_AVG":dimensions["LENGTH"],
              "HGT_AVG":building_height,
              "AR_BASE":base_area,
              "AR_WALL":wall_area,
              "AR_WIND":window_area,
              "AR_ROOF":roof_area,
              "AR_ENV1":envelope1,
              "AR_ENV2":envelope2,
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
              "HLP_TOT":total_loss_contemp,
              "HLC_BASE":base_loss_contemp,
              "HLC_WALL":wall_loss_contemp,
              "HLC_WIND":window_loss_contemp,
              "HLC_ROOF":roof_loss_contemp,
              "HLC_TOT":total_loss_pres
              }

#print evaluate_building(15000,10000,year_of_construction=1970)
#round(12.34448,2)
