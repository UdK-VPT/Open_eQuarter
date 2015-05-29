import math 
import present_base_uvalue_AVG_by_building_age_lookup as pbau
import present_wall_uvalue_AVG_by_building_age_lookup as pwau
import present_window_uvalue_AVG_by_building_age_lookup as pwiu
import present_roof_uvalue_AVG_by_building_age_lookup as prou

def energy_demand(population_density, floor_area, floor_perimeter=0, building_height=0, floors=0, window_ratio=0.2, year_of_construction=1960, accumulated_heating_hours=80000,common_walls=2):
  f_goldencut=1.618034
  if floor_perimeter==0:
    floor_perimeter=2*math.sqrt(floor_area*1.618034)+2*math.sqrt(floor_area/1.618034)
  pA_ratio=floor_perimeter/math.sqrt(floor_area)/2
  ab_ratio=pA_ratio/2+math.sqrt(pA_ratio**2/4-1)
  building_length=math.sqrt(floor_area)*ab_ratio
  building_width=math.sqrt(floor_area)/ab_ratio
  if building_height==0:
    if floors==0: floors=5
    building_height=floors*3.3
  else:
    floors=building_height/3.3
    
  print building_length
  print building_width
  print floor_perimeter
  print floor_area
  print building_length*building_width
  print 2*(building_width+building_length)
  base_area=floor_area
  base_uvalue_pres=pbau.present_base_uvalue_AVG_by_building_age_lookup(year_of_construction)
  base_loss_pres=base_area*base_uvalue_pres*0.6*accumulated_heating_hours/1000
  
  wall_area=(floor_perimeter-common_walls*building_width)*building_height*(1-window_ratio)
  wall_uvalue_pres=pwau.present_wall_uvalue_AVG_by_building_age_lookup(year_of_construction)
  wall_loss_pres=wall_area*wall_uvalue_pres*accumulated_heating_hours/1000
  
  window_area=(floor_perimeter-common_walls*building_width)*building_height*window_ratio
  window_uvalue_pres=pwiu.present_window_uvalue_AVG_by_building_age_lookup(year_of_construction)
  window_loss_pres=window_area*window_uvalue_pres*accumulated_heating_hours/1000
  
  roof_area=floor_area
  roof_uvalue_pres=prou.present_roof_uvalue_AVG_by_building_age_lookup(year_of_construction)
  roof_loss_pres=roof_area*roof_uvalue_pres*accumulated_heating_hours/1000
  
  total_loss_pres=base_loss_pres+wall_loss_pres+window_loss_pres+roof_loss_pres
  volume=floor_area*building_height
  envelope=2*floor_area+floor_perimeter*building_height
    
  return total_loss_pres


#print energy_demand(1500,480,100,year_of_construction=2000)
