
import math
import numpy as np
import oeqLookuptable as oeq

def typical_present_wall_uvalue_FH_by_year_of_construction(xin):

  # print {1850 : 1.8,1851 : 1.8}
  l_lookup = oeq.lookuptable(1850,1.8,1851,1.8,1855,2.0)
  l_lookup2 = oeq.lookuptable([1850,1851,1855],[1.8,1.8,2.0])
  print l_lookup.keys()
  print l_lookup2.keys()
  print l_lookup.values()
  print l_lookup2.values()
  l_lookup2 = oeq.lookuptable(l_lookup)
  print l_lookup2

  return(l_lookup.lookup(xin))

print typical_present_wall_uvalue_FH_by_year_of_construction(1995)
