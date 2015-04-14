#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Basic Building Data
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         21.10.2014
#
# Descrription: 
# The investigation of Open eQuarter Stat is drawing on the results of the demographic survey "Zensus 2011" 
# conducted by the Federal Statistical Office of Germany in 2011. This module extracts all data regarding 
# buildings and flats from the official file from Destatis 
#
# The source is:
# https://www.destatis.de/DE/Methoden/Zensus_/Downloads/csv_GebauedeWohnungen.zip
#
# There was no need to customized the sourcefile as the column names are coded. A further description can be 
# found in the source folder with the filename :"Datensatzbeschreibung_buildings.xls"
#
# If any changes are done in Excel, it is importat to set the cell format for all cells from Automatic to Text.
# Otherwise, ID fragments like "022" (String) are stored as 22 (integer).
#
# Key base file: Zensus11_Datensatz_buildings.csv  (!!!UTF-8 ENCODING IS MANDATORY!!!)
#
#######################################################################################
# basic includes
source("init.R")
source("mun_db.R")

#defining groups for gui 
BLD_GROUPS=c("BUILDINGS_BY_TYPE","BUILDINGS_BY_TYPE1","BUILDINGS_BY_TYPE2","BUILDINGS_BY_AGE1","BUILDINGS_BY_AGE2","BUILDINGS_BY_OWNER","BUILDINGS_BY_HEATSYS",
             "BUILDINGS_BY_NOFLATS","BUILDINGS_BY_COMWALLS")

FLT_GROUPS=c("FLATS_BY_TYPE","FLATS_BY_TYPE1","FLATS_BY_TYPE2","FLATS_BY_AGE1","FLATS_BY_AGE2","FLATS_BY_OWNER","FLATS_BY_HEATSYS",
             "FLATS_BY_NOROOMS","FLATS_BY_AREA","FLATS_BY_COMWALLS")

#adding verbose for all columns that might be useful in the further analysis to the global VERBOSE property. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BLD_DENS=list(label="Density of Buildings",unit="[n/km2]",info="Density of Buildings",title="Density of buildings",description="Density of buildings"),
                             FLT_DENS=list(label="Density of Flats",unit="[n/km2]",info="Density of Flats",title="Density of flats",description="Density of flats")
),stringsAsFactors=FALSE)

#buildings by type
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_TYPE=c("BLD_TYPE_TOTAL","BLD_TYPE_ONLY","BLD_TYPE_woDORM","BLD_TYPE_DORM","BLD_TYPE_OTHER")
BUILDINGS_BY_TYPE1=c("BLD_TYPE_ONLY","BLD_TYPE_woDORM","BLD_TYPE_DORM")
BUILDINGS_BY_TYPE2=c("BLD_TYPE_TOTAL","BLD_TYPE_ONLY","BLD_TYPE_OTHER")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_TYPE1=list(label="",unit="",info="Bld w Hous by Kind",title="Buildings w/ housing by kind",description="Buildings with housing by kind of the building"),
                             BUILDINGS_BY_TYPE2=list(label="",unit="",info="Bld Resid by Kind",title="Residential buildings by kind",description="Residential buildings by kind of the building"),
                             BUILDINGS_BY_TYPE=list(label="",unit="",info="Bld by kind",title="Buildings w/ housing by kind",description="Buildings with housing by kind of the building"),
                             BLD_TYPE_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing"),
                             BLD_TYPE_ONLY=list(label="Residential buildings",unit="[n]",info="Residential",title="Buildings w/ housing (Residential)",description="Buildings with housing of kind residential"),
                             BLD_TYPE_woDORM=list(label="Residential buildings w/o dormitories",unit="[n]",info="Resid w/o Dorm",title="(Residential w/o dormitories)",description="Buildings with housing of kind residential without dormitories etc."),
                             BLD_TYPE_DORM=list(label="Residential buildings, only dormitories",unit="[n]",info="Dormitories",title="Buildings w/ housing (Dormitories)",description="Buildings with housing of kind residential (only dormitories etc.)"),
                             BLD_TYPE_OTHER=list(label="Nonresidential buildings",unit="[n]",info="Nonresidential",title="Buildings w/ housing (Nonresidential)",description="Buildings with housing of kind nonresidential")
),stringsAsFactors=FALSE)

#buildings by age 1
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_AGE1=c("BLD_AGE1_TOTAL","BLD_AGE1_BEFORE1919","BLD_AGE1_1919TO1949","BLD_AGE1_1950TO1959","BLD_AGE1_1960TO1969",
                    "BLD_AGE1_1970TO1979","BLD_AGE1_1980TO1989","BLD_AGE1_1990TO1999","BLD_AGE1_2000TO2005","BLD_AGE1_AFTER2006")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_AGE1=list(label="",unit="",info="Bld w Hous by Age 1",title="Buildings w/ housing by age 1",description="Buildings with housing by age of the building (div 1)"),
                             BLD_AGE1_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_AGE1_BEFORE1919=list(label="Buildings before 1919",unit="[n]",info="before 1919",title="Buildings w/ housing -1919",description="Buildings with housing built before 1919"),
                             BLD_AGE1_1919TO1949=list(label="Buildings 1919-1949",unit="[n]",info="1919-1949",title="Buildings w/ housing 1919-1949",description="Buildings with housing built between 1919 and 1949"),
                             BLD_AGE1_1950TO1959=list(label="Buildings 1950-1959",unit="[n]",info="1950-1959",title="Buildings w/ housing 1950-1959",description="Buildings with housing built between 1950 and 1959"),
                             BLD_AGE1_1960TO1969=list(label="Buildings 1960-1969",unit="[n]",info="1960-1969",title="Buildings w/ housing 1960-1969",description="Buildings with housing built between 1960 and 1969"),
                             BLD_AGE1_1970TO1979=list(label="Buildings 1970-1979",unit="[n]",info="1970-1979",title="Buildings w/ housing 1970-1979",description="Buildings with housing built between 1970 and 1979"),
                             BLD_AGE1_1980TO1989=list(label="Buildings 1980-1989",unit="[n]",info="1980-1989",title="Buildings w/ housing 1980-1989",description="Buildings with housing built between 1980 and 1989"),
                             BLD_AGE1_1990TO1999=list(label="Buildings 1990-1999",unit="[n]",info="1990-1999",title="Buildings w/ housing 1990-1999",description="Buildings with housing built between 1990 and 1999"),
                             BLD_AGE1_2000TO2005=list(label="Buildings 2000-2005",unit="[n]",info="2000-2005",title="Buildings w/ housing 2000-2005",description="Buildings with housing built between 2000 and 2005"),
                             BLD_AGE1_AFTER2006=list(label="Buildings after 2005",unit="[n]",info="after 2005",title="Buildings w/ housing 2006-",description="Buildings with housing built after 2005"),
                             BLD_AGE1_AVG=list(label="Average Year of Construction",unit="[y]",info="AVG YoC",title="Average Year of Construction",description="Average Year of Construction")
),stringsAsFactors=FALSE)


#buildings by age 2
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_AGE2=c("BLD_AGE2_TOTAL","BLD_AGE2_BEFORE1919","BLD_AGE2_1919TO1948","BLD_AGE2_1949TO1978","BLD_AGE2_1979TO1986",
                    "BLD_AGE2_1987TO1990","BLD_AGE2_1991TO1995","BLD_AGE2_1996TO2000","BLD_AGE2_2001TO2004","BLD_AGE2_2005TO2008","BLD_AGE2_AFTER2009")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_AGE2=list(label="",unit="",info="Bld w Hous by age 2",title="Buildings w/ housing by age 2",description="Buildings with housing by age of the building (div 2)"),
                             BLD_AGE2_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_AGE2_BEFORE1919=list(label="Buildings before 1919",unit="[n]",info="before 1919",title="Buildings w/ housing -1919",description="Buildings with housing built before 1919"),
                             BLD_AGE2_1919TO1948=list(label="Buildings 1919-1948",unit="[n]",info="1919-1948",title="Buildings w/ housing 1919-1948",description="Buildings with housing built between 1919 and 1948"),
                             BLD_AGE2_1949TO1978=list(label="Buildings 1949-1978",unit="[n]",info="1949-1978",title="Buildings w/ housing 1949-1978",description="Buildings with housing built between 1949 and 1978"),
                             BLD_AGE2_1979TO1986=list(label="Buildings 1979-1986",unit="[n]",info="1979-1986",title="Buildings w/ housing 1979-1986",description="Buildings with housing built between 1979 and 1986"),
                             BLD_AGE2_1987TO1990=list(label="Buildings 1987-1990",unit="[n]",info="1987-1990",title="Buildings w/ housing 1987-1990",description="Buildings with housing built between 1987 and 1990"),
                             BLD_AGE2_1991TO1995=list(label="Buildings 1991-1995",unit="[n]",info="1991-1995",title="Buildings w/ housing 1991-1995",description="Buildings with housing built between 1991 and 1995"),
                             BLD_AGE2_1996TO2000=list(label="Buildings 1996-2000",unit="[n]",info="1996-2000",title="Buildings w/ housing 1996-2000",description="Buildings with housing built between 1996 and 2000"),
                             BLD_AGE2_2001TO2004=list(label="Buildings 2001-2004",unit="[n]",info="2001-2004",title="Buildings w/ housing 2001-2004",description="Buildings with housing built between 2001 and 2004"),
                             BLD_AGE2_2005TO2008=list(label="Buildings 2005-2008",unit="[n]",info="2005-2008",title="Buildings w/ housing 2005-2008",description="Buildings with housing built between 2005 and 2008"),
                             BLD_AGE2_AFTER2009=list(label="Buildings after 2008",unit="[n]",info="after 2008",title="Buildings w/ housing 2009-",description="Buildings with housing built after 2008 "),
                             BLD_AGE2_AVG=list(label="Average Year of Construction",unit="[y]",info="AVG YoC",title="Average Year of Construction",description="Average Year of Construction")
),stringsAsFactors=FALSE)


#buildings by owner
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_OWNER=c("BLD_OWNER_TOTAL","BLD_OWNER_ASSOC","BLD_OWNER_PRIV","BLD_OWNER_BUILDSOC","BLD_OWNER_MUNDWELLCOMP",
                     "BLD_OWNER_PRIVDWELLCOMP","BLD_OWNER_OTHERPRIVCOMP","BLD_OWNER_GOV","BLD_OWNER_ORG"  )

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_OWNER=list(label="",unit="",info="Bld w Hous by Owner",title="Buildings w/ housing by owner",description="Buildings with housing by owner of the building"),
                             BLD_OWNER_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_OWNER_ASSOC=list(label="Buildings owned by housing assiciations",unit="[n]",info="Assiciations",title="Buildings w/ housing (assiciations)",description="Buildings with housing owned by assiciations"),
                             BLD_OWNER_PRIV=list(label="Buildings owned by private persons",unit="[n]",info="Private Persons",title="Buildings w/ housing (private persons)",description="Buildings with housing owned by private persons"),
                             BLD_OWNER_BUILDSOC=list(label="Buildings owned by housing societies",unit="[n]",info="Societies",title="Buildings w/ housing (societies)",description=""),
                             BLD_OWNER_MUNDWELLCOMP=list(label="Buildings owned by municipal institutions",unit="[n]",info="Municipalities",title="Buildings w/ housing (municipalities)",description="Buildings with housing owned by muicipalities and municipal housing companies"),
                             BLD_OWNER_PRIVDWELLCOMP=list(label="Buildings owned by private housing companies",unit="[n]",info="Priv Housing Comp",title="Buildings w/ housing (private housing companies)",description="Buildings with housing owned by private housing companies"),
                             BLD_OWNER_OTHERPRIVCOMP=list(label="Buildings owned by other private companies",unit="[n]",info="Other Priv Comp",title="Buildings w/ housing (other private companies)",description="Buildings with housing owned by other private companies"),
                             BLD_OWNER_GOV=list(label="Buildings owned by governmental institutions",unit="[n]",info="Government",title="Buildings w/ housing (government)",description="Buildings with housing owned by government"),
                             BLD_OWNER_ORG=list(label="Buildings owned by NGOs",unit="[n]",info="NGOs",title="Buildings w/ housing (nongovernment organisations)",description="Buildings with housing owned by nongovernment organisations")
),stringsAsFactors=FALSE)

#buildings by heatingsystem
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_HEATSYS=c("BLD_HEAT_TOTAL","BLD_HEAT_DISTR","BLD_HEAT_SCDWELL","BLD_HEAT_BLOCKTYPE","BLD_HEAT_CENTRAL","BLD_HEAT_SNGLROOM","BLD_HEAT_NONE")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_HEATSYS=list(label="",unit="",info="Bld w Hous by Heatsys",title="Buildings w/ housing by heating system",description="Buildings with housing by heating system"),
                             BLD_HEAT_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_HEAT_DISTR=list(label="Buildings with district heating",unit="[n]",info="District",title="Buildings w/ housing (district heating)",description="Buildings with housing heated by district heating systems"),
                             BLD_HEAT_SCDWELL=list(label="Buildings with self contained heating",unit="[n]",info="Self contained",title="Buildings w/ housing (self contained heating)",description="Buildings with housing heated by self-contained central heating systems"),
                             BLD_HEAT_BLOCKTYPE=list(label="Buildings with block-type CHPs",unit="[n]",info="Block-type",title="Buildings w/ housing (block-type CHPs)",description="Buildings with housing heated by block-type combined heat and power plants"),
                             BLD_HEAT_CENTRAL=list(label="Buildings with central heating",unit="[n]",info="Central",title="Buildings w/ housing (central heating)",description="Buildings with housing heated by "),
                             BLD_HEAT_SNGLROOM=list(label="Buildings with single room heating",unit="[n]",info="Single Room",title="Buildings w/ housing (single room heating)",description="Buildings with housing heated by single room heating systems including stoves and night storage heaters"),
                             BLD_HEAT_NONE=list(label="Buildings without heating ",unit="[n]",info="",title="Buildings w/ housing (no heating)",description="Buildings w/ housing without heating systems")
),stringsAsFactors=FALSE)


#buildings by number of flats
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_NOFLATS=c("BLD_NOFLAT_TOTAL","BLD_NOFLAT_1","BLD_NOFLAT_2","BLD_NOFLAT_3TO6","BLD_NOFLAT_7TO12","BLD_NOFLAT_MTH13")
BUILDINGS_BY_NOFLATS_LIMITS=list(KEY=15000,BLD_NOFLAT_1=0,BLD_NOFLAT_2=0,BLD_NOFLAT_3TO6=0.40,BLD_NOFLAT_7TO12=0.40,BLD_NOFLAT_MTH13=0.20)
BUILDINGS_BY_NOFLATS_WEIGHTS=list(1,2,4.5,9.5,20)
#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_NOFLATS=list(label="",unit="",info="Bld w Hous by Flats",title="Buildings w/ housing by number of flats",description="Buildings with housing by number of flats"),
                             BLD_NOFLAT_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_NOFLAT_1=list(label="Buildings with 1 flat",unit="[n]",info="1 Flat",title="Buildings w/ housing (1 flat)",description="Buildings with housing with 1 flat"),
                             BLD_NOFLAT_2=list(label="Buildings with 2 flats",unit="[n]",info="2 Flats",title="Buildings w/ housing (2 flats)",description="Buildings with housing with 2 flats"),
                             BLD_NOFLAT_3TO6=list(label="Buildings with 3 up to 6 flats",unit="[n]",info="3-6 Flats",title="Buildings w/ housing (3-6 flats)",description="Buildings with housing with 3 up to 6 flats"),
                             BLD_NOFLAT_7TO12=list(label="Buildings with 7 up to 12 flats",unit="[n]",info="7-12 Flats",title="Buildings w/ housing (7-12 flats)",description="Buildings with housing with 7 up to 12 flats"),
                             BLD_NOFLAT_MTH13=list(label="Buildings with more than 13 flats",unit="[n]",info=">13 Flats",title="Buildings w/ housing (>13 flats)",description="Buildings with housing with more than 13 flats"),
                             BLD_NOFLAT_AVG=list(label="Average number of flats",unit="[n]",info="AVG N o Flats",title="Average Number of Flats",description="Average Number of Flats per Building")
),stringsAsFactors=FALSE)


#buildings by number of common walls
#defining corresponding datagroups (first ist always the sum of the others)
BUILDINGS_BY_COMWALLS=c("BLD_COMWALL_TOTAL","BLD_COMWALL_0","BLD_COMWALL_1","BLD_COMWALL_2","BLD_COMWALL_OTH")
BUILDINGS_BY_COMWALLS_LIMITS=list(KEY=15000,BLD_COMWALL_0=0.15,BLD_COMWALL_1=0.25,BLD_COMWALL_2=0.53,BLD_COMWALL_OTH=0.07)
BUILDINGS_BY_COMWALLS_TO_NOFLATS_LIMITS=list(KEY=10,BLD_COMWALL_0=0.2,BLD_COMWALL_1=0.15,BLD_COMWALL_2=0.6,BLD_COMWALL_OTH=0.05)

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             BUILDINGS_BY_COMWALL=list(label="",unit="",info="Bld w Hous by Com Walls",title="Buildings w/ housing by common walls",description="Buildings with housing by number of common walls"),
                             BLD_COMWALL_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BLD_COMWALL_0=list(label="Detached buildings",unit="[n]",info="No Common Walls",title="Buildings w/ housing (no common walls)",description="Buildings with housing, no common walls"),
                             BLD_COMWALL_1=list(label="Semi-detached buildings 1",unit="[n]",info="1 Common Wall",title="Buildings w/ housing (semi-detached 1)",description="Buildings with housing, 1 common wall"),
                             BLD_COMWALL_2=list(label="Semi-detached buildings 2",unit="[n]",info="2 Common Walls",title="Buildings w/ housing (semi-detached 2)",description="Buildings with housing, 2 common walls"),
                             BLD_COMWALL_OTH=list(label="No of common walls unknown",unit="[n]",info="Other",title="Buildings w/ housing (other)",description="Buildings with housing, number of common walls unknown"),
                             BLD_COMWALL_AVG=list(label="Average number of common walls",unit="[n]",info="AVG N o Com Walls",title="Average Number of Common Walls",description="Average Number of Common Walls per Building")
),stringsAsFactors=FALSE)


#flats by type
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_TYPE=c("FLT_TYPE_TOTAL","FLT_TYPE_ONLY","FLT_TYPE_woDORM","FLT_TYPE_DORM","FLT_TYPE_OTHER")
FLATS_BY_TYPE1=c("FLT_TYPE_ONLY","FLT_TYPE_woDORM","FLT_TYPE_DORM") #only dwellings, dormitory or not
FLATS_BY_TYPE2=c("FLT_TYPE_TOTAL","FLT_TYPE_ONLY","FLT_TYPE_OTHER") #dwelling or other types

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_TYPE1=list(label="",unit="",info="Flats Resid by Kind",title="Flats in residential buildings by kind",description="Flats in residential buildings by kind of the building"),
                             FLATS_BY_TYPE2=list(label="",unit="",info="Flats Bld w Hous by Kind",title="Flats in buildings w/ housing by kind",description="Flats in buildings with housing by kind of the building"),
                             FLATS_BY_TYPE=list(label="",unit="",info="Flats Bld w Hous by Kind",title="Flats in buildings w/ housing by kind",description="Flats in buildings with housing by kind of the building"),
                             FLT_TYPE_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing"),
                             FLT_TYPE_ONLY=list(label="Flats in residential buildings",unit="[n]",info="Residential",title="Flats in buildings w/ housing (Residential)",description="Flats in buildings with housing of kind residential"),
                             FLT_TYPE_woDORM=list(label="Flats in residential buildings w/o dormitories",unit="[n]",info="Dormitories",title="Flats in buildings w/ housing (Dormitories)",description="Flats in buildings with housing of kind residential (only dormitories etc.)"),
                             FLT_TYPE_DORM=list(label="Flats in residential buildings, only dormitories",unit="[n]",info="Dormitories",title="Flats in buildings w/ housing (Dormitories)",description="Flats in buildings with housing of kind residential (only dormitories etc.)"),
                             FLT_TYPE_OTHER=list(label="Flats in ronresidential buildings",unit="[n]",info="Nonresidential",title="Flats in buildings w/ housing (Nonresidential)",description="Flats in buildings with housing of kind nonresidential")
),stringsAsFactors=FALSE)

#flats by age 1
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_AGE1=c("FLT_AGE1_TOTAL","FLT_AGE1_BEFORE1919","FLT_AGE1_1919TO1949","FLT_AGE1_1950TO1959","FLT_AGE1_1960TO1969",
                "FLT_AGE1_1970TO1979","FLT_AGE1_1980TO1989","FLT_AGE1_1990TO1999","FLT_AGE1_2000TO2005","FLT_AGE1_AFTER2006")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_AGE1=list(label="",unit="",info="Flats Bld w Hous by Age 1",title="Flats in buildings w/ housing by age 1",description="Flats in buildings with housing by age of the building (div 1)"),
                             FLT_AGE1_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing"),
                             FLT_AGE1_BEFORE1919=list(label="Flats in buildings before 1919",unit="[n]",info="before 1919",title="Flats in buildings w/ housing -1919",description="Flats in buildings with housing built before 1919"),
                             FLT_AGE1_1919TO1949=list(label="Flats in buildings 1919-1949",unit="[n]",info="1919-1949",title="Flats in buildings w/ housing 1919-1949",description="Flats in buildings with housing built between 1919 and 1949"),
                             FLT_AGE1_1950TO1959=list(label="Flats in buildings 1950-1959",unit="[n]",info="1950-1959",title="Flats in buildings w/ housing 1950-1959",description="Flats in buildings with housing built between 1950 and 1959"),
                             FLT_AGE1_1960TO1969=list(label="Flats in buildings 1960-1969",unit="[n]",info="1960-1969",title="Flats in buildings w/ housing 1960-1969",description="Flats in buildings with housing built between 1960 and 1969"),
                             FLT_AGE1_1970TO1979=list(label="Flats in buildings 1970-1979",unit="[n]",info="1970-1979",title="Flats in buildings w/ housing 1970-1979",description="Flats in buildings with housing built between 1970 and 1979"),
                             FLT_AGE1_1980TO1989=list(label="Flats in buildings 1980-1989",unit="[n]",info="1980-1989",title="Flats in buildings w/ housing 1980-1989",description="Flats in buildings with housing built between 1980 and 1989"),
                             FLT_AGE1_1990TO1999=list(label="Flats in buildings 1990-1999",unit="[n]",info="1990-1999",title="Flats in buildings w/ housing 1990-1999",description="Flats in buildings with housing built between 1990 and 1999"),
                             FLT_AGE1_2000TO2005=list(label="Flats in buildings 2000-2005",unit="[n]",info="2000-2005",title="Flats in buildings w/ housing 2000-2005",description="Flats in buildings with housing built between 2000 and 2005"),
                             FLT_AGE1_AFTER2006=list(label="Flats in buildings after 2005",unit="[n]",info="after 2005",title="Flats in buildings w/ housing 2006-",description="Flats in buildings with housing built after 2005"),
                             FLT_AGE1_AVG=list(label="Average Year of Construction",unit="[y]",info="AVG YoC",title="Average Year of Construction",description="Average Year of Construction")
),stringsAsFactors=FALSE)

#flats by age 2
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_AGE2=c("FLT_AGE2_TOTAL","FLT_AGE2_BEFORE1919","FLT_AGE2_1919TO1948","FLT_AGE2_1949TO1978","FLT_AGE2_1979TO1986",
                "FLT_AGE2_1987TO1990","FLT_AGE2_1991TO1995","FLT_AGE2_1996TO2000","FLT_AGE2_2001TO2004","FLT_AGE2_2005TO2008","FLT_AGE2_AFTER2009")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_AGE2=list(label="",unit="",info="Flats Bld w Hous by age 2",title="Flats in buildings w/ housing by age 2",description="Flats in buildings with housing by age of the building (div 2)"),
                             FLT_AGE2_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_AGE2_BEFORE1919=list(label="Flats in buildings before 1919",unit="[n]",info="before 1919",title="Flats in buildings w/ housing -1919",description="Flats in buildings with housing built before 1919"),
                             FLT_AGE2_1919TO1948=list(label="Flats in buildings 1919-1948",unit="[n]",info="1919-1948",title="Flats in buildings w/ housing 1919-1948",description="Flats in buildings with housing built between 1919 and 1948"),
                             FLT_AGE2_1949TO1978=list(label="Flats in buildings 1949-1978",unit="[n]",info="1949-1978",title="Flats in buildings w/ housing 1949-1978",description="Flats in buildings with housing built between 1949 and 1978"),
                             FLT_AGE2_1979TO1986=list(label="Flats in buildings 1979-1986",unit="[n]",info="1979-1986",title="Flats in buildings w/ housing 1979-1986",description="Flats in buildings with housing built between 1979 and 1986"),
                             FLT_AGE2_1987TO1990=list(label="Flats in buildings 1987-1990",unit="[n]",info="1987-1990",title="Flats in buildings w/ housing 1987-1990",description="Flats in buildings with housing built between 1987 and 1990"),
                             FLT_AGE2_1991TO1995=list(label="Flats in buildings 1996-2000",unit="[n]",info="1991-1995",title="Flats in buildings w/ housing 1991-1995",description="Flats in buildings with housing built between 1991 and 1995"),
                             FLT_AGE2_1996TO2000=list(label="Flats in buildings 1996-2000",unit="[n]",info="1996-2000",title="Flats in buildings w/ housing 1996-2000",description="Flats in buildings with housing built between 1996 and 2000"),
                             FLT_AGE2_2001TO2004=list(label="Flats in buildings 2001-2004",unit="[n]",info="2001-2004",title="Flats in buildings w/ housing 2001-2004",description="Flats in buildings with housing built between 2001 and 2004"),
                             FLT_AGE2_2005TO2008=list(label="Flats in buildings 2005-2008",unit="[n]",info="2005-2008",title="Flats in buildings w/ housing 2005-2008",description="Flats in buildings with housing built between 2005 and 2008"),
                             FLT_AGE2_AFTER2009=list(label="Flats in buildings after 2008",unit="[n]",info="after 2008",title="Flats in buildings w/ housing 2009-",description="Flats in buildings with housing built after 2008 "),
                             FLT_AGE2_AVG=list(label="Average Year of Construction",unit="[y]",info="AVG YoC",title="Average Year of Construction",description="Average Year of Construction")
),stringsAsFactors=FALSE)

#flats by owner
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_OWNER=c("FLT_OWNER_TOTAL","FLT_OWNER_ASSOC","FLT_OWNER_PRIV","FLT_OWNER_BUILDSOC","FLT_OWNER_MUNDWELLCOMP",
                 "FLT_OWNER_PRIVDWELLCOMP","FLT_OWNER_OTHERPRIVCOMP","FLT_OWNER_GOV","FLT_OWNER_ORG")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_OWNER=list(label="",unit="",info="Flats Bld w Hous by Owner",title="Flats in buildings w/ housing by owner",description="Flats in buildings with housing by owner of the building"),
                             FLT_OWNER_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_OWNER_ASSOC=list(label="Flats owned by housing assiciations",unit="[n]",info="Assiciations",title="Flats in buildings w/ housing (assiciations)",description="Flats owned by assiciations in buildings with housing"),
                             FLT_OWNER_PRIV=list(label="Flats owned by private persons",unit="[n]",info="Private Persons",title="Flats in buildings w/ housing (private persons)",description="Flats owned by private persons in buildings with housing"),
                             FLT_OWNER_BUILDSOC=list(label="Flats owned by housing societies",unit="[n]",info="Societies",title="Flats in buildings w/ housing (societies)",description="Flats owned by societies in buildings with housing"),
                             FLT_OWNER_MUNDWELLCOMP=list(label="Flats owned by municipal institutions",unit="[n]",info="Municipalities",title="Flats in buildings w/ housing (municipalities)",description="Flats owned by muicipalities and municipal housing companies in buildings with housing "),
                             FLT_OWNER_PRIVDWELLCOMP=list(label="Flats owned by private housing companies",unit="[n]",info="Priv Housing Comp",title="Flats in buildings w/ housing (private housing companies)",description="Flats owned by private housing companies in buildings with housing"),
                             FLT_OWNER_OTHERPRIVCOMP=list(label="Flats owned by other private companies",unit="[n]",info="Other Priv Comp",title="Flats in buildings w/ housing (other private companies)",description="Flats owned by other private companies in buildings with housing"),
                             FLT_OWNER_GOV=list(label="Flats owned by governmental institutions",unit="[n]",info="Government",title="Flats in buildings w/ housing (government)",description="Flats owned by government in buildings with housing"),
                             FLT_OWNER_ORG=list(label="Flats owned by NGOs",unit="[n]",info="NGOs",title="Flats in buildings w/ housing (nongovernment organisations)",description="Flats owned by nongovernment organisations in buildings with housing")
),stringsAsFactors=FALSE)


#flats by heating system
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_HEATSYS=c("FLT_HEAT_TOTAL","FLT_HEAT_DISTR","FLT_HEAT_SCDWELL","FLT_HEAT_BLOCKTYPE","FLT_HEAT_CENTRAL","FLT_HEAT_SNGLROOM","FLT_HEAT_NONE")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_HEATSYS=list(label="",unit="",info="Flats Bld w Hous by Heatsys",title="Flats in buildings w/ housing by heating system",description="Flats in buildings with housing by heating system"),
                             FLT_HEAT_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_HEAT_DISTR=list(label="Flats with district heating",unit="[n]",info="District",title="Flats in buildings w/ housing (district heating)",description="Flats heated by a district heating systems in buildings with housing"),
                             FLT_HEAT_SCDWELL=list(label="Flats with self contained heating",unit="[n]",info="Self contained",title="Flats in buildings w/ housing (self contained heating)",description="Flats heated by self-contained central heating systems in buildings with housing"),
                             FLT_HEAT_BLOCKTYPE=list(label="Flats with block-type CHPs",unit="[n]",info="Block-type",title="Flats in buildings w/ housing (block-type CHPs)",description="Flats heated by a block-type combined heat and power plants in buildings with housing"),
                             FLT_HEAT_CENTRAL=list(label="Flats with central heating",unit="[n]",info="Central",title="Flats in buildings w/ housing (central heating)",description="Flats in buildings with housing heated by a centralheating systems"),
                             FLT_HEAT_SNGLROOM=list(label="Flats with single room heating",unit="[n]",info="Single Room",title="Flats in buildings w/ housing (single room heating)",description="Flats in buildings with housing heated by single room heating systems including stoves and night storage heaters"),
                             FLT_HEAT_NONE=list(label="Flats without heating",unit="[n]",info="",title="Flats in buildings w/ housing (no heating)",description="Flats in buildings w/ housing without heating systems")
),stringsAsFactors=FALSE)


#flats by utilization
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_UTIL=c("FLT_UTIL_TOTAL","FLT_UTIL_OWNER","FLT_UTIL_RENT","FLT_UTIL_HOLYDAY","FLT_UTIL_VAC")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_UTIL=list(label="",unit="",info="Flats Bld w Hous by Use",title="Flats in buildings w/ housing by use",description="Flats in buildings with housing by use of the flat"),
                             FLT_UTIL_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_UTIL_OWNER=list(label="Owner-occupied flats",unit="[n]",info="Owner",title="Flats in buildings w/ housing (owner-used)",description="Flats used by the owner in buildings with housing"),
                             FLT_UTIL_RENT=list(label="Rental flats",unit="[n]",info="Rental",title="Flats in buildings w/ housing (rental)",description="Rental flats in buildings with housing"),
                             FLT_UTIL_HOLYDAY=list(label="Holiday Rental flats",unit="[n]",info="Holyday",title="Flats in buildings w/ housing (holyday rental)",description="Holyday rental flats in buildings with housing"),
                             FLT_UTIL_VAC=list(label="Vacant flats",unit="[n]",info="Not in Use",title="Flats in buildings w/ housing (not in use)",description="Unused flats in buildings with housing")
),stringsAsFactors=FALSE)


#flats by living area
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_AREA=c("FLT_AREA_TOTAL","FLT_AREA_LTH40","FLT_AREA_40TO59","FLT_AREA_60TO79","FLT_AREA_80TO99","FLT_AREA_100TO119","FLT_AREA_120TO139",
                "FLT_AREA_140TO159","FLT_AREA_160TO179","FLT_AREA_180TO199","FLT_AREA_MTH200")
FLT_AREA_AVG_LIMITS=list(KEY=15000,BLD_NOFLAT_1=0,BLD_NOFLAT_2=0,BLD_NOFLAT_3TO6=0.40,BLD_NOFLAT_7TO12=0.40,BLD_NOFLAT_MTH13=0.20)

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_AREA=list(label="",unit="",info="Flats Bld w Hous by Area",title="Flats in buildings w/ housing by area",description="Flats in buildings with housing by area of the flat"),
                             FLT_AREA_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_AREA_LTH40=list(label="Flats of less than 40 m2",unit="[n]",info="<40 m2",title="Flats in buildings w/ housing (<40 m2)",description="Flats with an area of less than 40 m2 in buildings with housing"),
                             FLT_AREA_40TO59=list(label="Flats of 40 m2 up to 59 m2",unit="[n]",info="40-59 m2",title="Flats in buildings w/ housing (40-59 m2)",description="Flats with an area of 40 up to 59 m2 in buildings with housing"),
                             FLT_AREA_60TO79=list(label="Flats of 60 m2 up to 79 m2",unit="[n]",info="60-79 m2",title="Flats in buildings w/ housing (60-79 m2)",description="Flats with an area of 60 up to 79 m2 in buildings with housing"),
                             FLT_AREA_80TO99=list(label="Flats of 80 m2 up to 99 m2",unit="[n]",info="80-99 m2",title="Flats in buildings w/ housing (80-99 m2)",description="Flats with an area of 80 up to 99 m2 in buildings with housing"),
                             FLT_AREA_100TO119=list(label="Flats of 100 m2 up to 119 m2",unit="[n]",info="100-119 m2",title="Flats in buildings w/ housing (100-119 m2)",description="Flats with an area of 100 up to 119 m2 in buildings with housing"),
                             FLT_AREA_120TO139=list(label="Flats of 120 m2 up to 139 m2",unit="[n]",info="120-139 m2",title="Flats in buildings w/ housing (120-139 m2)",description="Flats with an area of 120 up to 139 m2 in buildings with housing"),
                             FLT_AREA_140TO159=list(label="Flats of 140 m2 up to 159 m2",unit="[n]",info="140-159 m2",title="Flats in buildings w/ housing (140-159 m2)",description="Flats with an area of 140 up to 159 m2 in buildings with housing"),
                             FLT_AREA_160TO179=list(label="Flats of 160 m2 up to 179 m2",unit="[n]",info="160-179 m2",title="Flats in buildings w/ housing (160-179 m2)",description="Flats with an area of 160 up to 179 m2 in buildings with housing"),
                             FLT_AREA_180TO199=list(label="Flats of 180 m2 up to 199 m2",unit="[n]",info="180-199 m2",title="Flats in buildings w/ housing (180-199 m2)",description="Flats with an area of 180 up to 199 m2 in buildings with housing"),
                             FLT_AREA_MTH200=list(label="Flats of more than 200 m2",unit="[n]",info=">200 m2",title="Flats in buildings w/ housing (<200 m2)",description="Flats with an area of more than 200 m2 in buildings with housing"),
                             FLT_AREA_AVG=list(label="Average area/flat",unit="[n]",info="AVG Area/Flat",title="Average Living Area",description="Average Living Area per Flat")
),stringsAsFactors=FALSE)
FLT_AREA_AVG_LIMITS=list(KEY=15000,FLT_AREA_AVG=60)


#flats by number of rooms
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_NOROOMS=c("FLT_NOROOMS_TOTAL","FLT_NOROOMS_1","FLT_NOROOMS_2","FLT_NOROOMS_3","FLT_NOROOMS_4","FLT_NOROOMS_5","FLT_NOROOMS_6","FLT_NOROOMS_MTH7")

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_NOROOMS=list(label="",unit="",info="Flats Bld w Hous by Rooms",title="Flats in buildings w/ housing by number of rooms",description="Flats in buildings with housing by number of rooms"),
                             FLT_NOROOMS_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_NOROOMS_1=list(label="Single room flats",unit="[n]",info="1 Room",title="Flats in buildings w/ housing (1 room)",description="Single room flats in buildings with housing"),
                             FLT_NOROOMS_2=list(label="Two room flats",unit="[n]",info="2 Room",title="Flats in buildings w/ housing (2 room)",description="Two room flats in buildings with housing"),
                             FLT_NOROOMS_3=list(label="Three room flats",unit="[n]",info="3 Room",title="Flats in buildings w/ housing (3 room)",description="Three room flats in buildings with housing"),
                             FLT_NOROOMS_4=list(label="Four room flats",unit="[n]",info="4 Room",title="Flats in buildings w/ housing (4 room)",description="Four room flats in buildings with housing"),
                             FLT_NOROOMS_5=list(label="Five room flats",unit="[n]",info="5 Room",title="Flats in buildings w/ housing (5 room)",description="Five room flats in buildings with housing"),
                             FLT_NOROOMS_6=list(label="Six room flats",unit="[n]",info="6 Room",title="Flats in buildings w/ housing (6 room)",description="Six room flats in buildings with housing"),
                             FLT_NOROOMS_MTH7=list(label="Flats with more than six rooms",unit="[n]",info=">6 Room",title="Flats in buildings w/ housing (>6 room)",description="More than six room flats in buildings with housing"),
                             FLT_NOROOMS_AVG=list(label="Average number of rooms/flat",unit="[n]",info="AVG Rooms/Flat",title="Average Number of Rooms",description="Average Number of Rooms per Flat")
),stringsAsFactors=FALSE)


#flats by number of common walls
#defining corresponding datagroups (first ist always the sum of the others)
FLATS_BY_COMWALLS=c("FLT_COMWALL_TOTAL","FLT_COMWALL_0","FLT_COMWALL_1","FLT_COMWALL_2","FLT_COMWALL_OTH")
FLATS_BY_COMWALLS_LIMITS=list(KEY=15000,FLT_COMWALL_0=0.1,FLT_COMWALL_1=0.2,FLT_COMWALL_2=0.5,FLT_COMWALL_OTH=0.07)

#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             FLATS_BY_COMWALLS=list(label="",unit="",info="Flats Bld w Hous by Com Walls",title="Flats in buildings w/ housing by common walls",description="Flats in buildings with housing by number of common walls"),
                             FLT_COMWALL_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             FLT_COMWALL_FAM=list(label="Flats in detached buildings",unit="[n]",info="No Common Walls",title="Flats in buildings w/ housing (no common walls)",description="Flats in buildings with housing, no common walls"),
                             FLT_COMWALL_SEMID=list(label="Flats in Semi-detached buildings 1",unit="[n]",info="1 Common Wall",title="Flats in buildings w/ housing (semi-detached 1)",description="Flats in buildings with housing, 1 common wall"),
                             FLT_COMWALL_TOWN=list(label="Flats in Semi-detached buildings 2",unit="[n]",info="2 Common Walls",title="Flats in buildings w/ housing (semi-detached 2)",description="Flats in buildings with housing, 2 common walls"),
                             FLT_COMWALL_OTHER=list(label="No of common walls unknown",unit="[n]",info="Other",title="Flats in buildings w/ housing (other)",description="Flats in buildings with housing, number common walls unknown"),
                             FLT_COMWALL_AVG=list(label="Average number of common walls",unit="[n]",info="AVG Com Walls/Flat",title="Average Number of Common Walls",description="Average Number of Common Walls per Flat")
),stringsAsFactors=FALSE)


get_building_DB<-function()
{
  # database repository  
  db_repo="database"
  # database filename
  db_filename=paste(db_repo,"bld_zensus_2011.RData",sep="/")
  
  # only reload if no database exists
  if(!(file.exists(db_filename, showWarnings = FALSE)[1])){
    # read the csv
    bld_raw=read.csv2(AS_choose.file("Select building data"),colClasses=c("character"),stringsAsFactors=FALSE,encoding="UTF-8",fileEncoding="UTF-8",dec=".")
    # only entries which are available in the muicipality key database
    bld_raw=bld_raw[bld_raw$AGS_12 %in% MUN_KEY_DB$RS,]
    # import useful columns
    building_data=data.frame(
      RS=as.character(bld_raw$AGS_12),
      SET=MUN_KEY_DB[bld_raw$AGS_12,"SET"],
      TYPE=MUN_KEY_DB[bld_raw$AGS_12,"TYPE"],
      AGS=MUN_KEY_DB[bld_raw$AGS_12,"AGS"],
      LAND=as.character(bld_raw$RS_Land),
      RB=as.character(bld_raw$RS_RB_NUTS2),
      DIST=as.character(bld_raw$RS_Kreis),
      MUNASS=as.character(bld_raw$RS_VB),
      MUN=as.character(bld_raw$RS_Gem),
      NAME=as.character(bld_raw$Name),
      POP_DENS=MUN_KEY_DB[bld_raw$AGS_12,"POP_DENS"],
      BLD_DENS=abs.force.numeric(bld_raw$GEB_1.1)/MUN_KEY_DB[bld_raw$AGS_12,"AREA"],
      FLT_DENS=abs.force.numeric(bld_raw$WHG_1.1)/MUN_KEY_DB[bld_raw$AGS_12,"AREA"],
      #Gebäude mit Wohnraum nach Art des Gebäudes
      #Gesamt BUILDINGS_w_FLATS_TOTAL
      BLD_TYPE_TOTAL=abs.force.numeric(bld_raw$GEB_1.1),
      #Wohngebäude BUILDINGS_w_FLATS_wo_DORMITORIES
      BLD_TYPE_ONLY=abs.force.numeric(bld_raw$GEB_1.2),
      #davon Wohngebäude (ohne Wohnheime)  
      BLD_TYPE_woDORM=abs.force.numeric(bld_raw$GEB_1.3),
      #davon Wohnheime  
      BLD_TYPE_DORM=abs.force.numeric(bld_raw$GEB_1.4),
      #sonstige Gebäude mit Wohnraum
      BLD_TYPE_OTHER=abs.force.numeric(bld_raw$GEB_1.5),
      #Gebäude mit Wohnraum nach Baujahr (Jahrzehnte)
      #Gesamt
      BLD_AGE1_TOTAL=abs.force.numeric(bld_raw$GEB_2.1),
      #Vor 1919 
      BLD_AGE1_BEFORE1919=abs.force.numeric(bld_raw$GEB_2.2),
      #1919 - 1949  
      BLD_AGE1_1919TO1949=abs.force.numeric(bld_raw$GEB_2.3),
      #1950-1959  
      BLD_AGE1_1950TO1959=abs.force.numeric(bld_raw$GEB_2.4),
      #1960-1969  
      BLD_AGE1_1960TO1969=abs.force.numeric(bld_raw$GEB_2.5),
      #1970-1979  
      BLD_AGE1_1970TO1979=abs.force.numeric(bld_raw$GEB_2.6),
      #1980-1989  
      BLD_AGE1_1980TO1989=abs.force.numeric(bld_raw$GEB_2.7),
      #1990-1999  
      BLD_AGE1_1990TO1999=abs.force.numeric(bld_raw$GEB_2.8),
      #2000-2005  
      BLD_AGE1_2000TO2005=abs.force.numeric(bld_raw$GEB_2.9),
      #2006 und später
      BLD_AGE1_AFTER2006=abs.force.numeric(bld_raw$GEB_2.10),
      #Average
      BLD_AGE1_AVG=rep(NA,nrow(bld_raw)),
      
      #Gebäude mit Wohnraum nach Baujahr  (Mikrozensus-Klassen)
      #Gesamt
      BLD_AGE2_TOTAL=abs.force.numeric(bld_raw$GEB_3.1),
      #Vor 1919  
      BLD_AGE2_BEFORE1919=abs.force.numeric(bld_raw$GEB_3.2),
      #1919 - 1948  
      BLD_AGE2_1919TO1948=abs.force.numeric(bld_raw$GEB_3.3),
      #1949 - 1978  
      BLD_AGE2_1949TO1978=abs.force.numeric(bld_raw$GEB_3.4),
      #1979 - 1986  
      BLD_AGE2_1979TO1986=abs.force.numeric(bld_raw$GEB_3.5),
      #1987 - 1990  
      BLD_AGE2_1987TO1990=abs.force.numeric(bld_raw$GEB_3.6),
      #1991 - 1995  
      BLD_AGE2_1991TO1995=abs.force.numeric(bld_raw$GEB_3.7),
      #1996 - 2000  
      BLD_AGE2_1996TO2000=abs.force.numeric(bld_raw$GEB_3.8),
      #2001 - 2004  
      BLD_AGE2_2001TO2004=abs.force.numeric(bld_raw$GEB_3.9),
      #2005 - 2008  
      BLD_AGE2_2005TO2008=abs.force.numeric(bld_raw$GEB_3.10),
      #2009 und später
      BLD_AGE2_AFTER2009=abs.force.numeric(bld_raw$GEB_3.11),
      #Average
      BLD_AGE2_AVG=rep(NA,nrow(bld_raw)),
      
      #Gebäude mit Wohnraum nach Eigentumsform des Gebäudes
      #Gesamt
      BLD_OWNER_TOTAL=abs.force.numeric(bld_raw$GEB_4.1),
      #Gemeinschaft von Wohnungseigentümern/-innen
      BLD_OWNER_ASSOC=abs.force.numeric(bld_raw$GEB_4.2),
      #Privatperson/-en  
      BLD_OWNER_PRIV=abs.force.numeric(bld_raw$GEB_4.3),
      #Wohnungsgenossenschaft  
      BLD_OWNER_BUILDSOC=abs.force.numeric(bld_raw$GEB_4.4),
      #Kommune oder kommunales Wohnungsunternehmen     
      BLD_OWNER_MUNDWELLCOMP=abs.force.numeric(bld_raw$GEB_4.5),
      #Privatwirtschaftliches Wohnungsunternehmen
      BLD_OWNER_PRIVDWELLCOMP=abs.force.numeric(bld_raw$GEB_4.6),
      #Anderes privatwirtschaftliches Unternehmen
      BLD_OWNER_OTHERPRIVCOMP=abs.force.numeric(bld_raw$GEB_4.7),
      #Bund oder Land
      BLD_OWNER_GOV=abs.force.numeric(bld_raw$GEB_4.8),
      #Organisation ohne Erwerbszweck
      BLD_OWNER_ORG=abs.force.numeric(bld_raw$GEB_4.9),
      
      
      #Gebäude mit Wohnraum nach Heizungsart      			
      #Gesamt
      BLD_HEAT_TOTAL=abs.force.numeric(bld_raw$GEB_5.1),
      #Fernheizung (Fernwärme)
      BLD_HEAT_DISTR=abs.force.numeric(bld_raw$GEB_5.2),
      #Etagenheizung
      BLD_HEAT_SCDWELL=abs.force.numeric(bld_raw$GEB_5.3),
      #Blockheizung
      BLD_HEAT_BLOCKTYPE=abs.force.numeric(bld_raw$GEB_5.4),
      #Zentralheizung
      BLD_HEAT_CENTRAL=abs.force.numeric(bld_raw$GEB_5.5),
      #Einzel- oder Mehrraumöfen (auch Nachtspeicherheizung)
      BLD_HEAT_SNGLROOM=abs.force.numeric(bld_raw$GEB_5.6),
      #Keine Heizung im Gebäude oder in den Wohnungen"
      BLD_HEAT_NONE=abs.force.numeric(bld_raw$GEB_5.7),
      
      
      #Gebäude mit Wohnraum nach Zahl der Wohnungen im Gebäude  				
      #Gesamt				
      BLD_NOFLAT_TOTAL=abs.force.numeric(bld_raw$GEB_6.1),
      #1 Wohnung  
      BLD_NOFLAT_1=abs.force.numeric(bld_raw$GEB_6.2),
      #2 Wohnungen  
      BLD_NOFLAT_2=abs.force.numeric(bld_raw$GEB_6.3),
      #3 - 6 Wohnungen  
      BLD_NOFLAT_3TO6=abs.force.numeric(bld_raw$GEB_6.4),
      #7 - 12 Wohnungen  
      BLD_NOFLAT_7TO12=abs.force.numeric(bld_raw$GEB_6.5),
      #13 und mehr Wohnungen
      BLD_NOFLAT_MTH13=abs.force.numeric(bld_raw$GEB_6.6),
      #Average
      BLD_NOFLAT_AVG=rep(NA,nrow(bld_raw)),
      #Gebäude mit Wohnraum nach Gebäudetyp-Bauweise  			
      #Gesamt
      BLD_COMWALL_TOTAL=abs.force.numeric(bld_raw$GEB_7.1),
      #Freistehendes Haus
      BLD_COMWALL_0=abs.force.numeric(bld_raw$GEB_7.2),
      #Doppelhaushälfte
      BLD_COMWALL_1=abs.force.numeric(bld_raw$GEB_7.3),
      #Gereihtes Haus
      BLD_COMWALL_2=abs.force.numeric(bld_raw$GEB_7.4),
      #Anderer Gebäudetyp
      BLD_COMWALL_OTH=abs.force.numeric(bld_raw$GEB_7.5),
      #Average
      BLD_COMWALL_AVG=rep(NA,nrow(bld_raw)),
      
      #Wohnungen in Gebäuden mit Wohnraum  			
      #Gesamt	
      FLT_TYPE_TOTAL=abs.force.numeric(bld_raw$WHG_1.1),
      #Wohnungen in Wohngebäuden  		
      FLT_TYPE_ONLY=abs.force.numeric(bld_raw$WHG_1.2),
      #davon in Wohngebäuden (ohne Wohnheime)  	
      FLT_TYPE_woDORM=abs.force.numeric(bld_raw$WHG_1.3),
      #davon in Wohnheimen  
      FLT_TYPE_DORM=abs.force.numeric(bld_raw$WHG_1.4),
      #in sonstigen Gebäuden mit Wohnraum
      FLT_TYPE_OTHER=abs.force.numeric(bld_raw$WHG_1.5),
      
      #Wohnungen nach Baujahr (Jahrzehnte)  								
      #Gesamt							
      FLT_AGE1_TOTAL=abs.force.numeric(bld_raw$WHG_2.1),
      #Vor 1919  
      FLT_AGE1_BEFORE1919=abs.force.numeric(bld_raw$WHG_2.2),
      #1919 - 1949  
      FLT_AGE1_1919TO1949=abs.force.numeric(bld_raw$WHG_2.3),
      #1950-1959  
      FLT_AGE1_1950TO1959=abs.force.numeric(bld_raw$WHG_2.4),
      #1960-1969  
      FLT_AGE1_1960TO1969=abs.force.numeric(bld_raw$WHG_2.5),
      #1970-1979  
      FLT_AGE1_1970TO1979=abs.force.numeric(bld_raw$WHG_2.6),
      #1980-1989  
      FLT_AGE1_1980TO1989=abs.force.numeric(bld_raw$WHG_2.7),
      #1990-1999  
      FLT_AGE1_1990TO1999=abs.force.numeric(bld_raw$WHG_2.8),
      #2000-2005  
      FLT_AGE1_2000TO2005=abs.force.numeric(bld_raw$WHG_2.9),
      #2006 und später
      FLT_AGE1_AFTER2006=abs.force.numeric(bld_raw$WHG_2.10),
      #Average
      FLT_AGE1_AVG=rep(NA,nrow(bld_raw)),
      
      #Wohnungen nach Baujahr (Mikrozenzus-Klassen)  									
      #Gesamt									
      FLT_AGE2_TOTAL=abs.force.numeric(bld_raw$WHG_3.1),
      #Vor 1919  
      FLT_AGE2_BEFORE1919=abs.force.numeric(bld_raw$WHG_3.2),
      #1919 - 1948    
      FLT_AGE2_1919TO1948=abs.force.numeric(bld_raw$WHG_3.3),
      #1949 - 1978    
      FLT_AGE2_1949TO1978=abs.force.numeric(bld_raw$WHG_3.4),
      #1979 - 1986    
      FLT_AGE2_1979TO1986=abs.force.numeric(bld_raw$WHG_3.5),
      #1987 - 1990    
      FLT_AGE2_1987TO1990=abs.force.numeric(bld_raw$WHG_3.6),
      #1991 - 1995    
      FLT_AGE2_1991TO1995=abs.force.numeric(bld_raw$WHG_3.7),
      #1996 - 2000    
      FLT_AGE2_1996TO2000=abs.force.numeric(bld_raw$WHG_3.8),
      #2001 - 2004    
      FLT_AGE2_2001TO2004=abs.force.numeric(bld_raw$WHG_3.9),
      #2005 - 2008    
      FLT_AGE2_2005TO2008=abs.force.numeric(bld_raw$WHG_3.10),
      #2009 und später
      FLT_AGE2_AFTER2009=abs.force.numeric(bld_raw$WHG_3.11),
      #Average
      FLT_AGE2_AVG=rep(NA,nrow(bld_raw)),
      
      
      #Wohnungen nach Eigentumsform des Gebäudes  							
      #Gesamt
      FLT_OWNER_TOTAL=abs.force.numeric(bld_raw$WHG_4.1),
      #Gemeinschaft von Wohnungseigentümern/-innen
      FLT_OWNER_ASSOC=abs.force.numeric(bld_raw$WHG_4.2),
      #Privatperson/-en  
      FLT_OWNER_PRIV=abs.force.numeric(bld_raw$WHG_4.3),
      #Wohnungsgenossenschaft  
      FLT_OWNER_BUILDSOC=abs.force.numeric(bld_raw$WHG_4.4),
      #Kommune oder kommunales Wohnungsunternehmen
      FLT_OWNER_MUNDWELLCOMP=abs.force.numeric(bld_raw$WHG_4.5),
      #Privatwirtschaftliches Wohnungsunternehmen
      FLT_OWNER_PRIVDWELLCOMP=abs.force.numeric(bld_raw$WHG_4.6),
      #Anderes privatwirtschaftliches Unternehmen
      FLT_OWNER_OTHERPRIVCOMP=abs.force.numeric(bld_raw$WHG_4.7),
      #Bund oder Land
      FLT_OWNER_GOV=abs.force.numeric(bld_raw$WHG_4.8),
      #Organisation ohne Erwerbszweck"
      FLT_OWNER_ORG=abs.force.numeric(bld_raw$WHG_4.9),
      
      
      #Wohnungen nach Heizungsart  					
      #Gesamt
      FLT_HEAT_TOTAL=abs.force.numeric(bld_raw$WHG_5.1),
      #Fernheizung (Fernwärme)
      FLT_HEAT_DISTR=abs.force.numeric(bld_raw$WHG_5.2),
      #Etagenheizung
      FLT_HEAT_SCDWELL=abs.force.numeric(bld_raw$WHG_5.3),
      #Blockheizung
      FLT_HEAT_BLOCKTYPE=abs.force.numeric(bld_raw$WHG_5.4),
      #Zentralheizung
      FLT_HEAT_CENTRAL=abs.force.numeric(bld_raw$WHG_5.5),
      #Einzel- oder Mehrraumöfen (auch Nachtspeicherheizung)
      FLT_HEAT_SNGLROOM=abs.force.numeric(bld_raw$WHG_5.6),
      #Keine Heizung im Gebäude oder in den Wohnungen"
      FLT_HEAT_NONE=abs.force.numeric(bld_raw$WHG_5.7),
      
      
      #Wohnungen in Gebäuden mit Wohnraum nach Art der Nutzung  			
      #Gesamt			
      FLT_UTIL_TOTAL=abs.force.numeric(bld_raw$WHG_6.1),
      #Von Eigentümer/-in bewohnt
      FLT_UTIL_OWNER=abs.force.numeric(bld_raw$WHG_6.2),
      #Zu Wohnzwecken vermietet (auch mietfrei)
      FLT_UTIL_RENT=abs.force.numeric(bld_raw$WHG_6.3),
      #Ferien- oder Freizeitwohnung
      FLT_UTIL_HOLYDAY=abs.force.numeric(bld_raw$WHG_6.4),
      #Leer stehend
      FLT_UTIL_VAC=abs.force.numeric(bld_raw$WHG_6.5),
      
      #Wohnungen in Gebäuden mit Wohnraum nach Fläche der Wohnung in m² (20 m²-Intervalle)   									
      #Gesamt	
      FLT_AREA_TOTAL=abs.force.numeric(bld_raw$WHG_7.1),
      #Unter 40    
      FLT_AREA_LTH40=abs.force.numeric(bld_raw$WHG_7.2),
      #40 - 59    
      FLT_AREA_40TO59=abs.force.numeric(bld_raw$WHG_7.3),
      #60 - 79    
      FLT_AREA_60TO79=abs.force.numeric(bld_raw$WHG_7.4),
      #80 - 99    
      FLT_AREA_80TO99=abs.force.numeric(bld_raw$WHG_7.5),
      #100 - 119    
      FLT_AREA_100TO119=abs.force.numeric(bld_raw$WHG_7.6),
      #120 - 139    
      FLT_AREA_120TO139=abs.force.numeric(bld_raw$WHG_7.7),
      #140 - 159    
      FLT_AREA_140TO159=abs.force.numeric(bld_raw$WHG_7.8),
      #160 - 179    
      FLT_AREA_160TO179=abs.force.numeric(bld_raw$WHG_7.9),
      #180 - 199    
      FLT_AREA_180TO199=abs.force.numeric(bld_raw$WHG_7.10),
      #200 und mehr
      FLT_AREA_MTH200=abs.force.numeric(bld_raw$WHG_7.11),
      #Average
      FLT_AREA_AVG=rep(NA,nrow(bld_raw)),
      
      
      #Wohnungen in Gebäuden mit Wohnraum nach Zahl der Räume  						
      #Gesamt					
      FLT_NOROOMS_TOTAL=abs.force.numeric(bld_raw$WHG_8.1),
      #1 Raum  
      FLT_NOROOMS_1=abs.force.numeric(bld_raw$WHG_8.2),
      #2 Räume  
      FLT_NOROOMS_2=abs.force.numeric(bld_raw$WHG_8.3),
      #3 Räume  
      FLT_NOROOMS_3=abs.force.numeric(bld_raw$WHG_8.4),
      #4 Räume  
      FLT_NOROOMS_4=abs.force.numeric(bld_raw$WHG_8.5),
      #5 Räume  
      FLT_NOROOMS_5=abs.force.numeric(bld_raw$WHG_8.6),
      #6 Räume  
      FLT_NOROOMS_6=abs.force.numeric(bld_raw$WHG_8.7),
      #7 und mehr Räume
      FLT_NOROOMS_MTH7=abs.force.numeric(bld_raw$WHG_8.8),
      #Average
      FLT_NOROOMS_AVG=rep(NA,nrow(bld_raw)),
      
      
      
      #Wohnungen nach Gebäudetyp-Bauweise  			
      #Gesamt	
      FLT_COMWALL_TOTAL=abs.force.numeric(bld_raw$WHG_9.1),
      #Freistehendes Haus  
      FLT_COMWALL_0=abs.force.numeric(bld_raw$WHG_9.2),
      #Doppelhaushälfte  
      FLT_COMWALL_1=abs.force.numeric(bld_raw$WHG_9.3),
      #Gereihtes Haus  
      FLT_COMWALL_2=abs.force.numeric(bld_raw$WHG_9.4),
      #Anderer Gebäudetyp
      FLT_COMWALL_OTH=abs.force.numeric(bld_raw$WHG_9.5),
      #Average
      FLT_COMWALL_AVG=rep(NA,nrow(bld_raw)),
      
      
      
      
      stringsAsFactors=FALSE, row.names = NULL)
    
    
    # SET shall be always "60"
    building_data=building_data[building_data$SET=="60",]
    # set rownames to KEY
    row.names(building_data) <- building_data$RS
    # set NA groupwise to 0 if sum is correct
    building_data[,BUILDINGS_BY_TYPE1]=set2zero.na(building_data[,BUILDINGS_BY_TYPE1])
    building_data[,BUILDINGS_BY_TYPE2]=set2zero.na(building_data[,BUILDINGS_BY_TYPE2])
    building_data[,BUILDINGS_BY_AGE1]=set2zero.na(building_data[,BUILDINGS_BY_AGE1])
    building_data[,"BLD_AGE1_AVG"]=round((building_data[,"BLD_AGE1_BEFORE1919"]*1850+building_data[,"BLD_AGE1_1919TO1949"]*1935
                                          +building_data[,"BLD_AGE1_1950TO1959"]*1954.5+building_data[,"BLD_AGE1_1960TO1969"]*1964.5
                                          +building_data[,"BLD_AGE1_1970TO1979"]*1974.5+building_data[,"BLD_AGE1_1980TO1989"]*1984.5
                                          +building_data[,"BLD_AGE1_1990TO1999"]*1994.5+building_data[,"BLD_AGE1_2000TO2005"]*2002.5
                                          +building_data[,"BLD_AGE1_AFTER2006"]*2008.5)/building_data[,"BLD_AGE1_TOTAL"],0)
    building_data[,BUILDINGS_BY_AGE2]=set2zero.na(building_data[,BUILDINGS_BY_AGE2])
    building_data[,"BLD_AGE2_AVG"]=round((building_data[,"BLD_AGE2_BEFORE1919"]*1850+building_data[,"BLD_AGE2_1919TO1948"]*1934.5
                                          +building_data[,"BLD_AGE2_1949TO1978"]*1964.5+building_data[,"BLD_AGE2_1979TO1986"]*1982.5
                                          +building_data[,"BLD_AGE2_1987TO1990"]*1988.5+building_data[,"BLD_AGE2_1991TO1995"]*1993
                                          +building_data[,"BLD_AGE2_1996TO2000"]*1998+building_data[,"BLD_AGE2_2001TO2004"]*2002.5
                                          +building_data[,"BLD_AGE2_2005TO2008"]*2006.5+building_data[,"BLD_AGE2_AFTER2009"]*2010)/building_data[,"BLD_AGE2_TOTAL"],0)
    building_data[,BUILDINGS_BY_OWNER]=set2zero.na(building_data[,BUILDINGS_BY_OWNER])
    building_data[,BUILDINGS_BY_HEATSYS]=set2zero.na(building_data[,BUILDINGS_BY_HEATSYS])
    building_data[,BUILDINGS_BY_NOFLATS]=set2zero.na(building_data[,BUILDINGS_BY_NOFLATS])
    building_data[,"BLD_NOFLAT_AVG"]=round((building_data[,"BLD_NOFLAT_1"]+building_data[,"BLD_NOFLAT_2"]*2
                                            +building_data[,"BLD_NOFLAT_3TO6"]*4.5+building_data[,"BLD_NOFLAT_7TO12"]*9.5
                                            +building_data[,"BLD_NOFLAT_MTH13"]*18)/building_data[,"BLD_NOFLAT_TOTAL"],1)
    
    building_data[,BUILDINGS_BY_COMWALLS]=set2zero.na(building_data[,BUILDINGS_BY_COMWALLS])
    building_data[,"BLD_COMWALL_AVG"]=round((building_data[,"BLD_COMWALL_0"]*0+building_data[,"BLD_COMWALL_1"]*1
                                             +building_data[,"BLD_COMWALL_2"]*2+building_data[,"BLD_COMWALL_OTH"]*3)/building_data[,"BLD_COMWALL_TOTAL"],1)
    
    
    
    building_data[,FLATS_BY_TYPE1]=set2zero.na(building_data[,FLATS_BY_TYPE1])
    building_data[,FLATS_BY_TYPE2]=set2zero.na(building_data[,FLATS_BY_TYPE2])
    building_data[,FLATS_BY_AGE1]=set2zero.na(building_data[,FLATS_BY_AGE1])
    building_data[,"FLT_AGE1_AVG"]=round((building_data[,"FLT_AGE1_BEFORE1919"]*1850+building_data[,"FLT_AGE1_1919TO1949"]*1935
                                          +building_data[,"FLT_AGE1_1950TO1959"]*1954.5+building_data[,"FLT_AGE1_1960TO1969"]*1964.5
                                          +building_data[,"FLT_AGE1_1970TO1979"]*1974.5+building_data[,"FLT_AGE1_1980TO1989"]*1984.5
                                          +building_data[,"FLT_AGE1_1990TO1999"]*1994.5+building_data[,"FLT_AGE1_2000TO2005"]*2002.5
                                          +building_data[,"FLT_AGE1_AFTER2006"]*2008.5)/building_data[,"FLT_AGE1_TOTAL"],0)
    building_data[,FLATS_BY_AGE2]=set2zero.na(building_data[,FLATS_BY_AGE2])
    building_data[,"FLT_AGE2_AVG"]=round((building_data[,"FLT_AGE2_BEFORE1919"]*1850+building_data[,"FLT_AGE2_1919TO1948"]*1934.5
                                          +building_data[,"FLT_AGE2_1949TO1978"]*1964.5+building_data[,"FLT_AGE2_1979TO1986"]*1982.5
                                          +building_data[,"FLT_AGE2_1987TO1990"]*1988.5+building_data[,"FLT_AGE2_1991TO1995"]*1993
                                          +building_data[,"FLT_AGE2_1996TO2000"]*1998+building_data[,"FLT_AGE2_2001TO2004"]*2002.5
                                          +building_data[,"FLT_AGE2_2005TO2008"]*2006.5+building_data[,"FLT_AGE2_AFTER2009"]*2010)/building_data[,"FLT_AGE2_TOTAL"],0)
    building_data[,FLATS_BY_OWNER]=set2zero.na(building_data[,FLATS_BY_OWNER])
    building_data[,FLATS_BY_HEATSYS]=set2zero.na(building_data[,FLATS_BY_HEATSYS])
    building_data[,FLATS_BY_UTIL]=set2zero.na(building_data[,FLATS_BY_UTIL])
    building_data[,FLATS_BY_AREA]=set2zero.na(building_data[,FLATS_BY_AREA])
    building_data[,"FLT_AREA_AVG"]=round((building_data[,"FLT_AREA_LTH40"]*20+building_data[,"FLT_AREA_40TO59"]*50
                                          +building_data[,"FLT_AREA_60TO79"]*70+building_data[,"FLT_AREA_80TO99"]*90
                                          +building_data[,"FLT_AREA_100TO119"]*110+building_data[,"FLT_AREA_120TO139"]*130
                                          +building_data[,"FLT_AREA_140TO159"]*150+building_data[,"FLT_AREA_160TO179"]*170
                                          +building_data[,"FLT_AREA_180TO199"]*190+building_data[,"FLT_AREA_MTH200"]*250)/building_data[,"FLT_AREA_TOTAL"],2)
    building_data[,FLATS_BY_NOROOMS]=set2zero.na(building_data[,FLATS_BY_NOROOMS])
    building_data[,"FLT_NOROOMS_AVG"]=round((building_data[,"FLT_NOROOMS_1"]*1+building_data[,"FLT_NOROOMS_2"]*2
                                             +building_data[,"FLT_NOROOMS_3"]*3+building_data[,"FLT_NOROOMS_4"]*4
                                             +building_data[,"FLT_NOROOMS_5"]*5+building_data[,"FLT_NOROOMS_6"]*6
                                             +building_data[,"FLT_NOROOMS_MTH7"]*8)/building_data[,"FLT_NOROOMS_TOTAL"],1)
    
    
    building_data[,FLATS_BY_COMWALLS]=set2zero.na(building_data[,FLATS_BY_COMWALLS])
    building_data[,"FLT_COMWALL_AVG"]=round((building_data[,"FLT_COMWALL_0"]*0+building_data[,"FLT_COMWALL_1"]*1
                                             +building_data[,"FLT_COMWALL_2"]*2+building_data[,"FLT_COMWALL_OTH"]*3)/building_data[,"FLT_COMWALL_TOTAL"],1)
    # save database
    save(building_data,file=db_filename)
  }else{load(db_filename)}
  return (building_data)
}

BLD_DB=get_building_DB()

#calculating the building type distribution based on population density 
#reliable densitsies of 100p/km2 up to 14500 p/km2
building_type_distribution<-function(population_density){
  Const = -0.0993616868903
  a = 0.881287361427
  b = -0.291989044211
  c = 0.0389614617009
  d= -0.00187133555672
  #calculationg the portion of single family
  l.no_efh=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
  Const = 0.16247873914
  a = -0.0796108197579
  b = 0.0400694636036
  c = -0.00569413833155
  d = 0.00022968371102
  
  l.no_dh=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
  Const = 0.460909016255
  a = -0.36666937572
  b = 0.109422140259
  c = -0.0133029419077
  d = 0.000603627950759
  l.no_mfh=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3 + d*log(population_density)^4
  Const = 0.280021311661
  a = -0.252584358595
  b = 0.0819383436518
  c = -0.0114061164963
  d = 0.000597448674144
  l.no_mfh=l.no_mfh + Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
  Const = 0.195952619835
  a = -0.182422807353
  b = 0.0605590966966
  c = -0.00855826496531
  d = 0.000440575220797
  l.no_gmh= Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
  l.sum=l.no_efh+l.no_dh+l.no_mfh+l.no_gmh
  return(as.data.frame(cbind(EFH=l.no_efh/l.sum,DH=l.no_dh/l.sum,MFH=l.no_mfh/l.sum,GMH=l.no_gmh/l.sum),stringsAsFactors=FALSE))
}
  

#KAL=new_OeQ_Inv(BLD_DB[,c("POP_DENS",BUILDINGS_BY_COMWALLS)],normcolumn="BLD_COMWALL_TOTAL",p_mode="log",limits=BUILDINGS_BY_COMWALLS_LIMITS,xrange=c(50,-1))

#calculating the building type distribution based on population density 
#reliable densitsies of 100p/km2 up to 14500 p/km2
building_common_walls<-function(population_density,mode="distribution"){
  Const = -1.3909502557
  a = 1.26783054073
  b = -0.235302951821
  c = 0.0153111057745
  d= -0.000291689589636
  #calculationg the portion of single family
  l.no_det=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
 
  Const = 0.887194201482
  a = -0.583660235549
  b = 0.14158446563
  c = -0.0135733812942
  d = 0.000462065202752
    l.no_semidet1=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
 
  Const = 1.6185919654
  a = -0.857984759884
  b = 0.148513709844
  c = -0.00830188333307
  d = 0.0000933822050967
  l.no_semidet2=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3 + d*log(population_density)^4
  
  Const = -0.114835911182
  a = 0.1738144547
  b = -0.0547952237862
  c = 0.00656415885278
  d = -0.000263757818213
  l.no_othdet=Const + a*log(population_density) + b*log(population_density)^2 + c*log(population_density)^3+ d*log(population_density)^4
 
  l.sum=l.no_det+l.no_semidet1+l.no_semidet2+l.no_othdet
  if(mode=="distribution"){
    return(as.data.frame(cbind(COMWALL_0=l.no_det/l.sum,COMWALL_1=l.no_semidet1/l.sum,COMWALL_2=l.no_semidet2/l.sum,COMWALL_OTH=l.no_othdet/l.sum),stringsAsFactors=FALSE))
  }
  return(l.no_semidet1/l.sum+l.no_semidet2/l.sum*2+l.no_othdet/l.sum*3)
         
}


#KAL=new_OeQ_Inv(BLD_DB[,c("BLD_NOFLAT_AVG",BUILDINGS_BY_COMWALLS)],normcolumn="BLD_COMWALL_TOTAL",p_mode="log",limits=BUILDINGS_BY_COMWALLS_TO_NOFLATS_LIMITS)


#calculating the building type distribution based on population density 
#reliable densitsies of 100p/km2 up to 14500 p/km2
building_common_walls_by_no_flats<-function(no_of_flats,mode="distribution"){
  Const=  0.856328483874 
  a=  -0.0565504308161 
  b=  -0.430106842527 
  c=  0.228113108826 
  d=  -0.0370470205099
  #calculationg the portion of single family
  l.no_det=Const + a*log(no_of_flats) + b*log(no_of_flats)^2 + c*log(no_of_flats)^3+ d*log(no_of_flats)^4
  
  Const=  -0.0842414630334 
  a=  0.172844609043 
  b=  -0.0428699365349 
  c=  0.00439921919651 
  d=  -0.000161116212725
  l.no_semidet1=Const + a*no_of_flats + b*no_of_flats^2 + c*no_of_flats^3+ d*no_of_flats^4
  
  Const=  0.05608817677 
  a=  -0.278461889568 
  b=  0.872985152354 
  c=  -0.489634333883 
  d=  0.0901145347064
  l.no_semidet2=Const + a*log(no_of_flats) + b*log(no_of_flats)^2 + c*log(no_of_flats)^3 + d*log(no_of_flats)^4
  
  Const=  0.0733977505987 
  a=  -0.0504430300137 
  b=  0.0315591813066 
  c=  -0.00588688675497 
  l.no_othdet=Const + a*log(no_of_flats) + b*log(no_of_flats)^2 + c*log(no_of_flats)^3
  
  l.sum=l.no_det+l.no_semidet1+l.no_semidet2+l.no_othdet
  if(mode=="distribution"){
    return(as.data.frame(cbind(COMWALL_0=l.no_det/l.sum,COMWALL_1=l.no_semidet1/l.sum,COMWALL_2=l.no_semidet2/l.sum,COMWALL_OTH=l.no_othdet/l.sum),stringsAsFactors=FALSE))
  }
  return(l.no_semidet1/l.sum+l.no_semidet2/l.sum*2+l.no_othdet/l.sum*3)
  
}






building_floors_distribution<-function(population_density){
  l.typedistribution=building_type_distribution(population_density)
  
  return((l.typedistribution$EFH*1.5+
           l.typedistribution$DH*2+
           l.typedistribution$MFH*4+
           l.typedistribution$GMH*7))
}

building_height_distribution<-function(population_density){
 return( building_nofloors_distribution(population_density)*3.3)
}
  
