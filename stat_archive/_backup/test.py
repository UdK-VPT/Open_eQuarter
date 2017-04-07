import math

def building_common_walls(population_density,mode="distribution"):
  Const = -1.3909502557
  a = 1.26783054073
  b = -0.235302951821
  c = 0.0153111057745
  d= -0.000291689589636
#calculationg the portion of single family
  l_no_det= Const + a*math.log(population_density) + b*math.log(population_density)**2 + c*math.log(population_density)**3+ d*math.log(population_density)**4
 
  Const = 0.887194201482
  a = -0.583660235549
  b = 0.14158446563
  c = -0.0135733812942
  d = 0.000462065202752
  l_no_semidet1=Const + a*math.log(population_density) + b*math.log(population_density)**2 + c*math.log(population_density)**3+ d*math.log(population_density)**4
 
  Const = 1.6185919654
  a = -0.857984759884
  b = 0.148513709844
  c = -0.00830188333307
  d = 0.0000933822050967
  l_no_semidet2=Const + a*math.log(population_density) + b*math.log(population_density)**2 + c*math.log(population_density)**3 + d*math.log(population_density)**4
  
  Const = -0.114835911182
  a = 0.1738144547
  b = -0.0547952237862
  c = 0.00656415885278
  d = -0.000263757818213
  l_no_othdet=Const + a*math.log(population_density) + b*math.log(population_density)**2 + c*math.log(population_density)**3+ d*math.log(population_density)**4
 
  l_sum=l_no_det+l_no_semidet1+l_no_semidet2+l_no_othdet
  if mode=="distribution":
    return(dict(COMWALL_0=l_no_det/l_sum,COMWALL_1=l_no_semidet1/l_sum,COMWALL_2=l_no_semidet2/l_sum,COMWALL_OTH=l_no_othdet/l_sum))
  
  return(l_no_semidet1/l_sum+l_no_semidet2/l_sum*2+l_no_othdet/l_sum*3)

x= building_common_walls(500)
print x['COMWALL_OTH']
