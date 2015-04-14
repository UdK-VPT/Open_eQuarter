


if(!(file.exists("database/oeq_uvalues_wall.RData", showWarnings = FALSE)[1])){
  oeq_uvalues_wall_src=read.csv2(AS_choose.file("Select UValues Data for Walls"),stringsAsFactors=FALSE,encoding="latin1",dec=",")
  oeq_uvalues_wall_src=oeq_uvalues_wall_src[-nrow(oeq_uvalues_wall_src),]
  oeq_uvalues_wall_src=apply(oeq_uvalues_wall_src,c(1,2),force.numeric)
  oeq_uvalues_wall_src=data.frame(oeq_uvalues_wall_src,stringsAsFactors=FALSE)
  oeq_uvalues_wall=data.frame(U_WALL_YEAR=oeq_uvalues_wall_src$Year,
                              U_WALL_EFH=oeq_uvalues_wall_src$EFH,
                              U_WALL_RH=oeq_uvalues_wall_src$RH,
                              U_WALL_MFH=oeq_uvalues_wall_src$MFH,
                              U_WALL_GMH=oeq_uvalues_wall_src$GMH,
                              U_WALL_URB_AVG=oeq_uvalues_wall_src$Urb.AVG,
                              U_WALL_SUBURB_AVG=oeq_uvalues_wall_src$SubUrb.AVG.,
                              U_WALL_RUR_AVG=oeq_uvalues_wall_src$Rur.AVG,
                              U_WALL_AVG=oeq_uvalues_wall_src$Total.AVG,
                              stringsAsFactors=FALSE)  
  save(oeq_uvalues_wall,file="database/oeq_uvalues_wall.RData")
}else{load("database/oeq_uvalues_wall.RData")}



uvalue_of_wall<-function(year=NULL){
  if(length(year)==1){
    year=c(year)
  }
  l.out=oeq_uvalues_wall
  l.out=l.out[0,]
  for (i in year){
    if(suppressWarnings(is.na(i))) {
      warning("Year is NA!")
      l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_wall)))
      next
    }else{
      if(i<min(oeq_uvalues_wall$U_WALL_YEAR)) {
        warning(paste(i,"is too far in the past!") )
        l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_wall)))
      }else{
        
        if(i>max(oeq_uvalues_wall$U_WALL_YEAR)) {
          warning(paste(i,"is too far in the future!") )
          l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_wall)))
        }else{
          
          l.out=rbind(l.out,oeq_uvalues_wall[oeq_uvalues_wall$U_WALL_YEAR==i,])
        }
      }
    }
  }
  return(l.out[,-1])
}



if(!(file.exists("database/oeq_uvalues_roof.RData", showWarnings = FALSE)[1])){
  oeq_uvalues_roof_src=read.csv2(AS_choose.file("Select UValues Data for Roofs"),stringsAsFactors=FALSE,encoding="latin1",dec=",")
  oeq_uvalues_roof_src=oeq_uvalues_roof_src[-nrow(oeq_uvalues_roof_src),]
  oeq_uvalues_roof_src=apply(oeq_uvalues_roof_src,c(1,2),force.numeric)
  oeq_uvalues_roof_src=data.frame(oeq_uvalues_roof_src,stringsAsFactors=FALSE)
  oeq_uvalues_roof=data.frame(U_ROOF_YEAR=oeq_uvalues_roof_src$Year,
                              U_ROOF_EFH=oeq_uvalues_roof_src$EFH,
                              U_ROOF_RH=oeq_uvalues_roof_src$RH,
                              U_ROOF_MFH=oeq_uvalues_roof_src$MFH,
                              U_ROOF_GMH=oeq_uvalues_roof_src$GMH,
                              U_ROOF_URB_AVG=oeq_uvalues_roof_src$UrbAVG,
                              U_ROOF_SUBURB_AVG=oeq_uvalues_roof_src$SubUrb_AVG,
                              U_ROOF_RUR_AVG=oeq_uvalues_roof_src$Rur_AVG,
                              U_ROOF_AVG=oeq_uvalues_roof_src$Total_AVG.,
                              U_ROOF_EFH_VERT=oeq_uvalues_roof_src$EFH_Vert,
                              U_ROOF_RH_VERT=oeq_uvalues_roof_src$RH_Vert,
                              U_ROOF_MFH_VERT=oeq_uvalues_roof_src$MFH_Vert,
                              U_ROOF_GMH_VERT=oeq_uvalues_roof_src$GMH_Vert,
                              U_ROOF_URB_VERT_AVG=oeq_uvalues_roof_src$UrbAVG_Vert,
                              U_ROOF_SUBURB_AVG_VERT=oeq_uvalues_roof_src$SubUrb_AVG_Vert,
                              U_ROOF_RUR_AVG_VERT=oeq_uvalues_roof_src$Rur_AVG_Vert,
                              U_ROOF_AVG_VERT=oeq_uvalues_roof_src$Total_AVG_Vert,
                              stringsAsFactors=FALSE)  
  save(oeq_uvalues_roof,file="database/oeq_uvalues_roof.RData")
}else{load("database/oeq_uvalues_roof.RData")}


uvalue_of_roof<-function(year=NULL){
  if(length(year)==1){
    year=c(year)
  }
  l.out=oeq_uvalues_roof
  l.out=l.out[0,]
  for (i in year){
    if(suppressWarnings(is.na(i))) {
      warning("Year is NA!")
      l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_roof)))
      next
    }else{
      if(i<min(oeq_uvalues_roof$U_ROOF_YEAR)) {
        warning(paste(i,"is too far in the past!") )
        l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_roof)))
      }else{
        
        if(i>max(oeq_uvalues_roof$U_ROOF_YEAR)) {
          warning(paste(i,"is too far in the future!") )
          l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_roof)))
        }else{
          
          l.out=rbind(l.out,oeq_uvalues_roof[oeq_uvalues_roof$U_ROOF_YEAR==i,])
          #     colnames(l.out)<-colnames(oeq_uvalues_roof)
        }
      }
    }
  }
  return(l.out[,-1])
}


if(!(file.exists("database/oeq_uvalues_base.RData", showWarnings = FALSE)[1])){
  oeq_uvalues_base_src=read.csv2(AS_choose.file("Select UValues Data for Bases"),stringsAsFactors=FALSE,encoding="latin1",dec=",")
  oeq_uvalues_base_src=oeq_uvalues_base_src[-nrow(oeq_uvalues_base_src),]
  oeq_uvalues_base_src=apply(oeq_uvalues_base_src,c(1,2),force.numeric)
  oeq_uvalues_base_src=data.frame(oeq_uvalues_base_src,stringsAsFactors=FALSE)
  oeq_uvalues_base=data.frame(U_BASE_YEAR=oeq_uvalues_base_src$Year,
                              U_BASE_EFH=oeq_uvalues_base_src$EFH,
                              U_BASE_RH=oeq_uvalues_base_src$RH,
                              U_BASE_MFH=oeq_uvalues_base_src$MFH,
                              U_BASE_GMH=oeq_uvalues_base_src$GMH,
                              U_BASE_URB_AVG=oeq_uvalues_base_src$Urb.AVG,
                              U_BASE_SUBURB_AVG=oeq_uvalues_base_src$SubUrb.AVG.,
                              U_BASE_RUR_AVG=oeq_uvalues_base_src$Rur.AVG,
                              U_BASE_AVG=oeq_uvalues_base_src$Total.AVG,
                              stringsAsFactors=FALSE)  
  save(oeq_uvalues_base,file="database/oeq_uvalues_base.RData")
}else{load("database/oeq_uvalues_base.RData")}

uvalue_of_base<-function(year=NULL){
  if(length(year)==1){
    year=c(year)
  }
  l.out=oeq_uvalues_base
  l.out=l.out[0,]
  for (i in year){
    if(suppressWarnings(is.na(i))) {
      warning("Year is NA!")
      l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_base)))
      next
    }else{
      if(i<min(oeq_uvalues_base$U_BASE_YEAR)) {
        warning(paste(i,"is too far in the past!") )
        l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_base)))
      }else{
        
        if(i>max(oeq_uvalues_base$U_BASE_YEAR)) {
          warning(paste(i,"is too far in the future!") )
          l.out=rbind(l.out,rep(NA,ncol(oeq_uvalues_base)))
        }else{
          
          l.out=rbind(l.out,oeq_uvalues_base[oeq_uvalues_base$U_BASE_YEAR==i,])
        }
      }
    }
  }
  return(l.out[,-1])
}

UVAL_DB=cbind(YEAR=c(1900:2015),uvalue_of_base(c(1900:2015))[,c( "U_BASE_EFH","U_BASE_RH","U_BASE_MFH","U_BASE_GMH")])
UVAL_DB=cbind(UVAL_DB,uvalue_of_roof(c(1900:2015))[,c(  "U_ROOF_EFH","U_ROOF_RH","U_ROOF_MFH","U_ROOF_GMH" )])
UVAL_DB=cbind(UVAL_DB,uvalue_of_wall(c(1900:2015))[,c(  "U_WALL_EFH","U_WALL_RH","U_WALL_MFH","U_WALL_GMH" )])
plot(c(1900:2015),UVAL_DB[,"U_BASE_EFH"],type="l",col="RED",ylim=c(0,3))
lines(c(1900:2015),UVAL_DB[,"U_WALL_EFH"],col="DARK GREEN")
lines(c(1900:2015),UVAL_DB[,"U_ROOF_EFH"],col="BLUE")
plot(c(1900:2015),UVAL_DB[,"U_BASE_RH"],type="l",col="RED",ylim=c(0,3))
lines(c(1900:2015),UVAL_DB[,"U_WALL_RH"],col="DARK GREEN")
lines(c(1900:2015),UVAL_DB[,"U_ROOF_RH"],col="BLUE")
plot(c(1900:2015),UVAL_DB[,"U_BASE_MFH"],type="l",col="RED",ylim=c(0,3))
lines(c(1900:2015),UVAL_DB[,"U_WALL_MFH"],col="DARK GREEN")
lines(c(1900:2015),UVAL_DB[,"U_ROOF_MFH"],col="BLUE")
plot(c(1900:2015),UVAL_DB[,"U_BASE_GMH"],type="l",col="RED",ylim=c(0,3))
lines(c(1900:2015),UVAL_DB[,"U_WALL_GMH"],col="DARK GREEN")
lines(c(1900:2015),UVAL_DB[,"U_ROOF_GMH"],col="BLUE")

#querschnitt=read.csv(AS_choose.file("Select U-Values csv"),stringsAsFactors=FALSE,encoding="latin1",dec=".")
#querschnitt=cbind(querschnitt,uwall=uvalue_of_wall(querschnitt$Baujahr)$U_WALL_AVG,
#  uroof=uvalue_of_roof(querschnitt$Baujahr)$U_ROOF_AVG,
#  ubase=uvalue_of_base(querschnitt$Baujahr)$U_BASE_AVG)
#write.csv(querschnitt,"U-Values_Calculated.csv")


component_uvalues<-function(year_of_construction){
  return(UVAL_DB[UVAL_DB$YEAR==year_of_construction,])
}




