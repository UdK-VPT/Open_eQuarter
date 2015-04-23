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


test2 = lookuptable("kult",1,
                    "uhu",2,
                    "bart",7,
                    "kulti",2)
#print test2.keys()
#print test2.lookup("uhu","bart")
print test2.dat
print test2.lookup("uhu",'bart')
print test2.reverse_lookup(7,2)
