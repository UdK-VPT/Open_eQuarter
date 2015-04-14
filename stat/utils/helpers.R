#Little helpers
library(jsonlite)
export_to_json<-function(){ #Export Geodata and postcode for municipalities in germany
  db_output="for_qgis_plugin/municipal_db.json"
  l.munkey=cbind(MUN_KEY_DB[MUN_KEY_DB$RS,c("NAME","POP_DENS","POSTCODE","GEO_L","GEO_W")],
               AVG_YOC=BLD_DB[MUN_KEY_DB$RS,"BLD_AGE1_AVG"])
  print(length(which(l.munkey$POSTCODE!="")))
  l.munkey=l.munkey[l.munkey$POSTCODE!="",]
  l.munkey=l.munkey[!is.na(l.munkey$POSTCODE),]
  View(l.munkey)
  stream_out(l.munkey, file(db_output))
}

sigmoid <- function(z,precision=4,width=NULL)
{
  if(is.null(width)) width=1.260+4.665*precision
  g <- 1-1/(1+exp(-width*(z-0.5)))
  return(round(g,precision))
}

highlm<-function(x,y){
  print(data.frame(x,y))
#  l.lm1=lm(y~ poly(x,I(length(x)-1),raw=TRUE))
 # l.lm2=lm(y~ poly(x,length(x)-2,raw=TRUE))
l.lm2=lm(y~ poly(x,,raw=TRUE))
l.lm3=lm(y~ poly(x,3,raw=TRUE))
l.lm4=lm(y~ poly(x,4,raw=TRUE))
  l.lm5=lm(y~ poly(x,3,raw=TRUE))
  l.lm6=lm(y~ poly(log(x),3,raw=TRUE))
  plot(x,y)
  l.x=seq(min(x),max(x),length.out=100)
  print(l.x)
 # l.y=predict(l.lm5,newdata=data.frame(x=l.x))
 #exit
lines(x,predict(l.lm2),col="RED")
lines(x,predict(l.lm3))
#lines(x,predict(l.lm4))
#lines(x,predict(l.lm5))
#lines(x,predict(l.lm6))
}