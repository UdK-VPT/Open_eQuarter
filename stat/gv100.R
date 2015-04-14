#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / The GV100 Key Base
#
# Status:       Not is use
#
# Author:       Werner Kaul
#
# Date:         21.10.2014
#
# Descrription: 
# The investigation of Open eQuarter Stat is drawing on the results of the demographic survey "Zensus 2011" 
# conducted by the Federal Statistical Office of Germany in 2011. For crossreferencing 
# statistical data of admistrative structures like municpalities, countries, counties etc., 
# a unique ID or key is needed. As european standards were not implemented in that field of work, 
# the german "General Municipality Key" (AGS) will be used here. A solid key base could be
# found in the official municipality list of the time right before the survey (end of 2010). The source is:
# https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugJ/31122010_Auszug_GV.xls?__blob=publicationFile
# The sourcefile was customized according to the needs of R and this investigation:
#   1. Column titles were changed to corresponding abbreviations
#   2. Dispensible lines were removed
#   3. Export to .csv
# 
# Key base file: 31122010_Auszug_GV.csv
#
#######################################################################################

setConstructorS3("OeQ_DB", function(...){
  this <- extend(Object(), "OeQ_DB",
                 .Source=character(0),
                 .ImportDate=character(0),
                 .Database=data.frame(0))
  this;
})

setMethodS3("print", "OeQ_DB", function(this, ...) {
  print("-----OeQ_DB Summary------")
  print(paste(".Source: ",this$.Source,sep=""))
  print(paste(".ImportDate: ",this$.ImportDate,sep=""))
  print(paste(".Database: ---->",sep=""))
  print(this$.Database[1:10,])
})

setMethodS3("loadGV100", "OeQ_DB", function(this,GV100_Source=NULL, ...) {
  if (is.null(GV100_Source)) GV100_Source=AS_choose.file("Select GV100 Sourcefile (*.asc,*.txt)",filetype = c("asc","txt"))
  
  con <- file(GV100_Source, "r", blocking = FALSE)
  GV100_raw=readLines(con,encoding = "latin1") # empty
  close(con)
  l.usingK1=which(substr(GV100_raw,11,12) %in% c("03","07"))
  l.usingR=which(!(substr(GV100_raw,11,12) %in% c("03","07")))
  R_raw=substr(GV100_raw,13,13)
  R_raw[l.usingK1]=0
  K1_raw=substr(GV100_raw,13,13)
  K1_raw[l.usingR]=0
  this$.Raw=GV100_raw
  this$.Source=GV100_Source
  this$.ImportDate=date()
  this$.Database=data.frame(
    L=trim.leading(trim.trailing(substr(GV100_raw,11,12))),
    R=R_raw,
    K1=K1_raw,
    K2=trim.leading(trim.trailing(substr(GV100_raw,14,15))),
    t=trim.leading(trim.trailing(substr(GV100_raw,19,19))),
    V1=trim.leading(trim.trailing(substr(GV100_raw,19,20))),
    V2=trim.leading(trim.trailing(substr(GV100_raw,21,22))),
    G=substr(GV100_raw,16,18),
    Basekey="",
    RS="",
    AGS="",
    AGS8=trim.leading(trim.trailing(substr(GV100_raw,11,18))),
    RegionalCode=trim.leading(trim.trailing(paste(substr(GV100_raw,11,15),substr(GV100_raw,19,22),substr(GV100_raw,16,18),sep=""))),
    Level=unlist(sapply(trim.trailing(paste(substr(GV100_raw,11,15),substr(GV100_raw,19,22),substr(GV100_raw,16,18),sep="")),function(x){
      if(nchar(x)==12) return(5) #Municipality
      if(nchar(x)==9) return(4) #MunAssociation
      if(nchar(x)==5) return(3) #District
      if(nchar(x)==3) return(2) #AdminRegion
      if(x=="00") return(0)
      if(nchar(x)==2) return(1) #State
      return(-1)
    },USE.NAMES = FALSE)),
    State=substr(GV100_raw,11,12),
    AdminRegion=substr(GV100_raw,13,13),
    District=substr(GV100_raw,14,15),
    MunAssociation=substr(GV100_raw,19,22),
    Municipality=substr(GV100_raw,16,18),
    Name=trim.leading(trim.trailing(substr(GV100_raw,23,72))),
    AdminMunicipal=trim.leading(trim.trailing(substr(GV100_raw,73,122))),
    Type=substr(GV100_raw,123,124),
    Typ=unlist(sapply(substr(GV100_raw,123,124),function(x) {n=with(GTypedef,Descr[ID==x])
                                                             if(length(n)==0) n="Ohne Typ"
                                                             return(n)},USE.NAMES=FALSE)),
    Area=as.numeric(substr(GV100_raw,129,139)),
    Inhabitants=as.numeric(substr(GV100_raw,140,150)),
    Density=as.numeric(substr(GV100_raw,140,150))/as.numeric(substr(GV100_raw,129,139)),
    stringsAsFactors=FALSE)
  #this;
})


