from math import sqrt
from scipy.constants import golden
def dimensions(area='NULL',perimeter='NULL',length='NULL'):
 # golden_rule_ratio=(1 + 5 ** 0.5) / 2 
  if (area == 'NULL') & (perimeter == 'NULL'): 
    if length=='NULL': return 'NULL'
    width = perimeter/2-length
    perimeter=2*length*(1+1/golden)
    area = width * length
    return {'AREA':area,'PERIMETER':perimeter,'WIDTH':min(width,length), 'LENGTH':max(width,length)}
    
  if perimeter == 'NULL':
    if length == 'NULL': 
      length = sqrt(area*golden)
    width = area/length
    perimeter = 2*width + 2*length
    return {'AREA':area,'PERIMETER':perimeter,'WIDTH':min(width,length), 'LENGTH':max(width,length)}
    
  if area == 'NULL':
    if length == 'NULL': 
      length = perimeter/(2*(1/golden+1))
    width = perimeter/2-length
    area = width * length
    return {'AREA':area,'PERIMETER':perimeter,'WIDTH':min(width,length), 'LENGTH':max(width,length)}

  if (perimeter**2-16*area) > 0:
    length= abs(sqrt(perimeter**2-16*area)-perimeter)/4
  else:
    #if not rectangle use square PROBLEM: leads to wrong perimeter ....
    length=sqrt(area)
  width = area/length
  return {'AREA':area,'PERIMETER':perimeter,'WIDTH':min(width,length), 'LENGTH':max(width,length)}
  
def area(perimeter='NULL',length='NULL'):
  l_dim=dimensions(area='NULL',perimeter=perimeter,length=length)
  return l_dim["AREA"] 

def perimeter(area='NULL',length='NULL'):
  l_dim=dimensions(area=area,perimeter='NULL',length=length)
  return l_dim["PERIMETER"] 
  
def width(area='NULL',perimeter='NULL',width='NULL'):
  l_dim=dimensions(area=area,perimeter=perimeter,length=width)
  return l_dim["LENGTH"] 

def length(area='NULL',perimeter='NULL',length='NULL'):
  l_dim=dimensions(area=area,perimeter=perimeter,length=length)
  return l_dim["LENGTH"] 
