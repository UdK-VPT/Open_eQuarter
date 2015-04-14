#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Basic Municipality Data
#
# Status:       Active
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
# found in the official municipality list for end of 2011 as the included data are based on the Zensus results.
#
# The source is:
# https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugJ/31122011_Auszug_GV.xls
#
# The sourcefile was customized according to the needs of R and this investigation:
#   1. Column titles were changed to corresponding abbreviations:
#
#      SETTYPE <- "Satzart"  
#            t <- "Textkennzeichen"	
#        STATE <- "Regionalschlüssel (RS) / Land"
#     DISTRICT <- "Regionalschlüssel (RS) / Kreis"
#        ADMIN <- "Regionalschlüssel (RS) / VB"
#          MUN <- "Regionalschlüssel (RS) / Gem"
#         NAME <- "Gemeindename"
#         AREA <- "Fläche km2"
#    POP_TOTAL <- "Bevölkerung / insgesamt"
#     POP_MALE <- "Bevölkerung / männlich"
#   POP_FEMALE <- "Bevölkerung / weiblich"
#     POP_DENS <- "Bevölkerung / je km2"
#     POSTCODE <- "Postleitzahl"
#        GEO_L <- "Geografische Mittelpunktkoordinaten / Längengrad"
#        GEO_W <- "Geografische Mittelpunktkoordinaten / Breitengrad"
#        GEO_W <- "Geografische Mittelpunktkoordinaten / Breitengrad"
#       EU_KEY <- "EU-Stadt-/Landgliederung / Schlüssel"
#     EU_DESCR <- "EU-Stadt-/Landgliederung / Bezeichnung"
#
#   2. Dispensible columns and rows were removed
#
#  dropped <- "Reisegebiete / Schlüssel"
#  dropped <- "Reisegebiete / Bezeichnung"
#
#   3. Export to .csv
#
# If these changes are done in Excel, it is important to set the cell format for all cells from Automatic to Text.
# Otherwise, ID fragments like "022" (String) are stored as 22 (integer).
#
# Key base file: 31122011_Auszug_GV.csv   (!!!UTF-8 ENCODING IS MANDATORY!!!)
#
#######################################################################################
# basic includes
source("init.R")

#defining corresponding datagroups (first ist always the sum of the others)
POPULATION_BY_GENDER=c("POP_TOTAL","POP_M","POP_F")

# adding verbose for all columns that might be useful in the further analysis to the global VERBOSE property. VERBOSE is initialized in init.R
VERBOSE=as.data.frame(rbind(VERBOSE,
  POPULATION_BY_GENDER=list(label="Population by Gender",unit="[n/km2]",info="Pop by Gend",title="Population by Gender",description="Population by Gender"),
  POP_DENS=list(label="Population Density",unit="[n/km2]",info="Pop Density",title="Density of Population",description="Density of Population"),
  AREA =list(label="Municipality Area",unit="[km2]",info="Mun Area",title="Area of Municipality",description="Area of Municipality")
),stringsAsFactors=FALSE)


#load db with basic municipality data, used as key
get_municipalities_DB<-function()
{
  # database repository  
  db_repo="database"
  # database filename
  db_filename=paste(db_repo,"mun_key_zensus_2011.RData",sep="/")
  
  # only reload if no database exists
  if(!(file.exists(db_filename, showWarnings = FALSE)[1])){
    # read the csv
    l.GV100=read.csv2(AS_choose.file("Select municipality list (GV100)"),colClasses=c("character"),stringsAsFactors=FALSE,fileEncoding="UTF-8",encoding="UTF-8",dec=".")
    #Encoding(l.GV100) <- "UTF-8"
    # import useful columns
    municipalities_key=data.frame(RS=remove.spaces(paste( l.GV100$Land,
                                                           l.GV100$RB,
                                                           l.GV100$Kreis,
                                                           l.GV100$VB,
                                                           l.GV100$Gem,sep="")),
                                   AGS=remove.spaces(paste( l.GV100$Land,
                                                            l.GV100$RB,
                                                            l.GV100$Kreis,
                                                            l.GV100$Gem,sep="")),
                                   SET=as.character( l.GV100$Satz),
                                   TYPE=as.character( l.GV100$t),
                                   LAND=as.character( l.GV100$Land),
                                   RB=as.character( l.GV100$RB),
                                   DIST=as.character( l.GV100$Kreis),
                                   MUNASS=as.character( l.GV100$VB),
                                   MUN=as.character( l.GV100$Gem),
                                   NAME=as.character( l.GV100$Name),
                                   AREA=abs.force.numeric( l.GV100$AREA),
                                   POP_TOTAL=abs.force.numeric( l.GV100$POP_TOTAL),
                                   POP_M=abs.force.numeric( l.GV100$POP_M),
                                   POP_F=abs.force.numeric( l.GV100$POP_F),
                                   POP_DENS=abs.force.numeric( l.GV100$POP_DENS),
                                   POSTCODE=abs.force.numeric( l.GV100$POSTCODE),
                                   GEO_L=abs.force.numeric( l.GV100$GEO_L),
                                   GEO_W=abs.force.numeric( l.GV100$GEO_W),
                                   EU_KEY=abs.force.numeric( l.GV100$EU_KEY),
                                   EU_DESCR=abs.force.numeric( l.GV100$EU_DESCR),
                                   stringsAsFactors=FALSE)
    #remove all rows which do not describe a municipality
    municipalities_key=municipalities_key[municipalities_key$MUN!="",]
    # SET shall be always "60"
    municipalities_key=municipalities_key[municipalities_key$SET=="60",]
    #sort by KEY
    municipalities_key=municipalities_key[order(municipalities_key$RS),]
    View(municipalities_key)
    # set rownames to KEY
    row.names(municipalities_key) <- municipalities_key$RS
    # save database
    save(municipalities_key,file=db_filename)
  }else{
    load(db_filename)
  }
  return (municipalities_key)
}

MUN_KEY_DB=get_municipalities_DB()