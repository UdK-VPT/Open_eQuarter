from math import log

class lookuptable:
  def __init__(self,*args):
   # print len(args)
  #  print args[0::2]
  #  print args[1::2]
    if len(args) == 1 and len(args[0]) > 1: args=args[0]
    if len(args)==2 and len(args[0])==len(args[1]):
      self.dat= dict(zip(args[0],args[1]))
    else:
      self.dat=dict(zip(args[0::2],args[1::2]))
      
  def __getitem__(self,args): 
    ret = [ self.values()[i] for i in [self.keys().index(j) for j in args]]
    if len(ret) == 1: return ret[0]#
    else: return ret
 
  def keys(self):
    return self.dat.keys()
  
  def values(self):
    return self.dat.values()

  def lookup(self,args):
    ret = [ self.values()[i] for i in [self.keys().index(j) for j in args]]
    if len(ret) == 1: return ret[0]#
    else: return ret
 
  def reverse_lookup(self,args):
     return [ self.keys()[i] for i in [i for i, j in enumerate(self.values()) if j in args]]


