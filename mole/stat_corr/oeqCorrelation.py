from math import log

class correlation:
  def __init__(self,const=0,a=0,b=0,c=0,d=0,mode="lin"):
    self.const=const
    self.a=a
    self.b=b
    self.c=c
    self.d=d
    self.mode=mode
    
  def lookup(self,*args):
  # args = [float(x) for x in args]
    if self.mode == "log":
      args = [log(x) for x in args]
    ret = [self.const + self.a*x + self.b*x**2 + self.c*x**3 + self.d*x**4  for x in args]
    if len(ret) == 1: return ret[0]#
    else: return ret
    
