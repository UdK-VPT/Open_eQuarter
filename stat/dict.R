# python like dictionary
lookup<-function(
  keys="",
  objects=NULL,  # verbose formula (py-string)
  ...){ # Constructor for a single regression model 1
  if(is.null(objects)){
    dict=unlist(keys)[c(1:(length(unlist(keys))%/%2)*2)]
    keys=unlist(keys)[c(1:(length(unlist(keys))%/%2)*2-1)]
  }else{
      dict=objects
    }
  names(dict)<- keys
   #setClass("dict",
  #          slots = the.list,
  #          prototype=list(0))
  dict
}



