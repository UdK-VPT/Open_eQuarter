load_gem_level<-function(){
  load("USE6_GEMEINDEEBENE.RData")
  return(USE6_GEMEINDEEBENE)
}

on recvalue(theLabel, theRecord)
return theLabel & \":\" & (run script \"
    on run{y}
    return \" & theLabel & \" of y 
    end run\" with parameters {theRecord})
end recvalue",sep="")

