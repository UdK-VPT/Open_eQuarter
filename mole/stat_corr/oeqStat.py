from math import log

class lookuptable:
  def __init__(self,*args):
    if len(args) == 1 and len(args[0]) > 1: args=args[0]
    if len(args)==2 and len(args[0])==len(args[1]):
      self.dat= dict(zip(args[0],args[1]))
    else:
      self.dat=dict(zip(args[::2],args[1::2]))
    
  def keys(self):
    return self.dat.keys()
  
  def values(self):
    return self.dat.values()

  def lookup(self,*args):
     return [ self.values()[i] for i in [i for i, j in enumerate(self.keys()) if j in args]]
    #return [self.dat[x] for x in args]

  def reverse_lookup(self,*args):
     return [ self.keys()[i] for i in [i for i, j in enumerate(self.values()) if j in args]]


class correlation:
  def __init__(self,const=0,a=0,b=0,c=0,d=0,mode="lin"):
    self.const=const
    self.a=a
    self.b=b
    self.c=c
    self.d=d
    self.mode=mode
    
  def lookup(self,*args):
    if self.mode == "log":
      args = [log(x) for x in args]
    return [self.const + self.a*x + self.b*x**2 + self.c*x**3 + self.d*x**4  for x in args]
    
