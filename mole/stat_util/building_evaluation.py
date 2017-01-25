import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import math
import bld_geometry 
from stat_corr import * 

from qgis.core import *
from mole.oeq_global import *


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
  solar_earnings_per_sqm=300
  average_heat_demand_per_sqm=120

  #print "AREA"
  #print area
  if isnull(area): 
    return {"YOC":NULL,
                "POP_DENS": NULL,
                "FLS_AVG": NULL,
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
                "HE_SOL_LIV":NULL,
                "RT_SOL":NULL,
                "HTS_FLT":NULL,
                "HTS_BLD":NULL,
                "OWN_FLT":NULL,
                "OWN_BLD":NULL
                }

  dimensions=bld_geometry.dimensions(area,perimeter,length)
  #print 'YOC'
  #print year_of_construction
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
  
  solar_area=roof_area * ratio_solar_available
  solar_installable_area=solar_area*ratio_solar_installable
  solar_earnings=solar_earnings_per_sqm * solar_installable_area
  total_heat_demand=average_heat_demand_per_sqm  * living_area
  solar_coverage_rate=solar_earnings/total_heat_demand*100
  
  bld_owners_rate=building_owner_distribution_by_population_density_correlation.get(population_density)
  owner_keys=bld_owners_rate.keys()
  most_bld_owners=owner_keys[0]
  owner_keys.pop(0)
  for i in owner_keys:
    if bld_owners_rate[i] > bld_owners_rate[most_bld_owners]:
      most_bld_owners=i
  if most_bld_owners == "BLD_OWNER_ASSOC":
    most_bld_owners_descr="ASSOC"
  elif most_bld_owners == "BLD_OWNER_PRIV":
    most_bld_owners_descr="PRIV"
  elif most_bld_owners == "BLD_OWNER_BUILDSOC":
    most_bld_owners_descr="BUILDSOC"
  elif most_bld_owners == "BLD_OWNER_MUNDWELLCOMP":
    most_bld_owners_descr="MUNDWELLCOMP"
  elif most_bld_owners == "BLD_OWNER_PRIVDWELLCOMP":
    most_bld_owners_descr="PRIVDWELLCOMP"
  elif most_bld_owners == "BLD_OWNER_OTHERPRIVCOMP":
    most_bld_owners_descr="OTHERPRIVCOMP"
  elif most_bld_owners == "BLD_OWNER_GOV":
    most_bld_owners_descr="GOV"
  elif most_bld_owners == "BLD_OWNER_ORG":
    most_bld_owners_descr="ORG"
  else:
    most_bld_owners_descr=NULL
 
  flt_owners_rate=flat_owner_distribution_by_population_density_correlation.get(population_density)
  owner_keys=flt_owners_rate.keys()
  most_flt_owners=owner_keys[0]
  owner_keys.pop(0)
  for i in owner_keys:
    if flt_owners_rate[i] > flt_owners_rate[most_flt_owners]:
      most_flt_owners=i
  if most_flt_owners == "FLT_OWNER_ASSOC":
    most_flt_owners_descr="ASSOC"
  elif most_flt_owners == "FLT_OWNER_PRIV":
    most_flt_owners_descr="PRIV"
  elif most_flt_owners == "FLT_OWNER_BUILDSOC":
    most_flt_owners_descr="BUILDSOC"
  elif most_flt_owners == "FLT_OWNER_MUNDWELLCOMP":
    most_flt_owners_descr="MUNDWELLCOMP"
  elif most_flt_owners == "FLT_OWNER_PRIVDWELLCOMP":
    most_flt_owners_descr="PRIVDWELLCOMP"
  elif most_flt_owners == "FLT_OWNER_OTHERPRIVCOMP":
    most_flt_owners_descr="OTHERPRIVCOMP"
  elif most_flt_owners == "FLT_OWNER_GOV":
    most_flt_owners_descr="GOV"
  elif most_flt_owners == "FLT_OWNER_ORG":
    most_flt_owners_descr="ORG"
  else:
    most_flt_owners_descr=NULL
  
  bld_heating_rate=building_heating_type_distribution_by_population_density_correlation.get(population_density)
  heating_keys=bld_heating_rate.keys()
  most_bld_heating=heating_keys[0]
  heating_keys.pop(0)
  for i in heating_keys:
    if bld_heating_rate[i] > bld_heating_rate[most_bld_heating]:
      most_bld_heating=i
  if most_bld_heating == "BLD_HEAT_DISTR":
    most_bld_heating_descr="DISTR"
  elif most_bld_heating == "BLD_HEAT_SCDWELL":
    most_bld_heating_descr="SCDWELL"
  elif most_bld_heating == "BLD_HEAT_BLOCKTYPE":
    most_bld_heating_descr="BLOCKTYPE"
  elif most_bld_heating == "BLD_HEAT_CENTRAL":
    most_bld_heating_descr="CENTRAL"
  elif most_bld_heating == "BLD_HEAT_SNGLROOM":
    most_bld_heating_descr="SNGLROOM"
  elif most_bld_heating == "BLD_HEAT_NONE":
    most_bld_heating_descr="NONE"
  else:
    most_bld_heating_descr=NULL
  
  flt_heating_rate=flat_heating_type_distribution_by_population_density_correlation.get(population_density)
  heating_keys=flt_heating_rate.keys()
  most_flt_heating=heating_keys[0]
  heating_keys.pop(0)
  for i in heating_keys:
    if flt_heating_rate[i] > flt_heating_rate[most_flt_heating]:
      most_flt_heating=i
  if most_flt_heating == "FLT_HEAT_DISTR":
    most_flt_heating_descr="DISTR"
  elif most_flt_heating == "FLT_HEAT_SCDWELL":
    most_flt_heating_descr="SCDWELL"
  elif most_flt_heating == "FLT_HEAT_BLOCKTYPE":
    most_flt_heating_descr="BLOCKTYPE"
  elif most_flt_heating == "FLT_HEAT_CENTRAL":
    most_flt_heating_descr="CENTRAL"
  elif most_flt_heating == "FLT_HEAT_SNGLROOM":
    most_flt_heating_descr="SNGLROOM"
  elif most_flt_heating == "FLT_HEAT_NONE":
    most_flt_heating_descr="NONE"
  else:
    most_flt_heating_descr=NULL

  
  
  return {"POP_DENS":population_density,
              "YOC":year_of_construction,
              "FLS_AVG": floors,
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
              "AR_SOL_AVA": solar_area,
              "AR_SOL_INS": solar_installable_area,
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
              "HD_TOT": total_heat_demand,
              "HE_SOL": solar_earnings,
              "HE_SOL_LIV":solar_earnings/living_area,
              "RT_SOL":solar_coverage_rate,
              "HTS_FLT":most_flt_heating_descr,
              "HTS_BLD":most_bld_heating_descr,
              "OWN_FLT":most_flt_owners_descr,
              "OWN_BLD":most_bld_owners_descr
              }

