#This file contains all definitions to import data from specific .csv sources for use with the Open eQuarter 
#The basic structure is a data.frame <COLUMNNAME>=list(src_col=<Column Name in the .csv )

IMPORT_MAPPING=data.frame(
  RS="as.character(gebaeude$AGS_12),
  SET=gemeinden_zensus_2011[gebaeude$AGS_12,"SET"],
  TYPE=gemeinden_zensus_2011[gebaeude$AGS_12,"TYPE"],
  AGS=gemeinden_zensus_2011[gebaeude$AGS_12,"AGS"],
  LAND=as.character(gebaeude$RS_Land),
  RB=as.character(gebaeude$RS_RB_NUTS2),
  DIST=as.character(gebaeude$RS_Kreis),
  MUNASS=as.character(gebaeude$RS_VB),
  MUN=as.character(gebaeude$RS_Gem),
  NAME=as.character(gebaeude$Name),
  P_DENS=gemeinden_zensus_2011[gebaeude$AGS_12,"DENS"],
  B_DENS=redefine_col(gebaeude$GEB_1.1)/gemeinden_zensus_2011[gebaeude$AGS_12,"AREA"],
  D_DENS=redefine_col(gebaeude$WHG_1.1)/gemeinden_zensus_2011[gebaeude$AGS_12,"AREA"],
  AREA=gemeinden_zensus_2011[gebaeude$AGS_12,"AREA"],
  #Gebäude mit Wohnraum nach Art des Gebäudes
  #Gesamt BUILDINGS_w_DWELLINGS_TOTAL
  BwD_UTIL_TOTAL=redefine_col(gebaeude$GEB_1.1),
  #Wohngebäude BUILDINGS_w_DWELLINGS_wo_DORMITORIES
  BwD_UTIL_ONLY=redefine_col(gebaeude$GEB_1.2),
  #davon Wohngebäude (ohne Wohnheime)  
  BwD_UTIL_woDORM=redefine_col(gebaeude$GEB_1.3),
  #davon Wohnheime  
  BwD_UTIL_DORM=redefine_col(gebaeude$GEB_1.4),
  #sonstige Gebäude mit Wohnraum
  BwD_UTIL_OTHER=redefine_col(gebaeude$GEB_1.5),
  
  #Gebäude mit Wohnraum nach Baujahr (Jahrzehnte)
  #Gesamt
  BwD_AGE_TOTAL=redefine_col(gebaeude$GEB_2.1),
  #Durchschnittsalter
  #BwD_AGE_AVERAGE=redefine_col(gebaeude$GEB_2.2)/100+redefine_col(gebaeude$GEB_2.3)/30+
  
  #Vor 1919  AEWZ_M=redefine_col(gebaeude$GEB_2_2),
  BwD_AGE_BEFORE1919=redefine_col(gebaeude$GEB_2.2),
  #1919 - 1949  
  BwD_AGE_1919TO1949=redefine_col(gebaeude$GEB_2.3),
  #1950-1959  
  BwD_AGE_1950TO1959=redefine_col(gebaeude$GEB_2.4),
  #1960-1969  
  BwD_AGE_1960TO1969=redefine_col(gebaeude$GEB_2.5),
  #1970-1979  
  BwD_AGE_1970TO1979=redefine_col(gebaeude$GEB_2.6),
  #1980-1989  
  BwD_AGE_1980TO1989=redefine_col(gebaeude$GEB_2.7),
  #1990-1999  
  BwD_AGE_1990TO1999=redefine_col(gebaeude$GEB_2.8),
  #2000-2005  
  BwD_AGE_2000TO2005=redefine_col(gebaeude$GEB_2.9),
  #2006 und später(2011)
  BwD_AGE_2006TO2011=redefine_col(gebaeude$GEB_2.10),
  #Average Age
  BwD_AGE_AVG=(redefine_col(gebaeude$GEB_2.2)*1850+redefine_col(gebaeude$GEB_2.3)*1935
               +redefine_col(gebaeude$GEB_2.4)*1954.5+redefine_col(gebaeude$GEB_2.5)*1964.5
               +redefine_col(gebaeude$GEB_2.6)*1974.5+redefine_col(gebaeude$GEB_2.7)*1984.5
               +redefine_col(gebaeude$GEB_2.8)*1994.5+redefine_col(gebaeude$GEB_2.9)*2002.5
               +redefine_col(gebaeude$GEB_2.10)*2008.5)/redefine_col(gebaeude$GEB_2.1),
  
  #Gebäude mit Wohnraum nach Baujahr  (Mikrozensus-Klassen)
  #Gesamt
  BwD_AGE2_TOTAL=redefine_col(gebaeude$GEB_3.1),
  #Vor 1919  
  BwD_AGE2_BEFORE1919=redefine_col(gebaeude$GEB_3.2),
  #1919 - 1948  
  BwD_AGE2_1919TO1948=redefine_col(gebaeude$GEB_3.3),
  #1949 - 1978  
  BwD_AGE2_1949TO1978=redefine_col(gebaeude$GEB_3.4),
  #1979 - 1986  
  BwD_AGE2_1979TO1986=redefine_col(gebaeude$GEB_3.5),
  #1987 - 1990  
  BwD_AGE2_1987TO1990=redefine_col(gebaeude$GEB_3.6),
  #1991 - 1995  
  BwD_AGE2_1991TO1995=redefine_col(gebaeude$GEB_3.7),
  #1996 - 2000  
  BwD_AGE2_1996TO2000=redefine_col(gebaeude$GEB_3.8),
  #2001 - 2004  
  BwD_AGE2_2001TO2004=redefine_col(gebaeude$GEB_3.9),
  #2005 - 2008  
  BwD_AGE2_2005TO2008=redefine_col(gebaeude$GEB_3.10),
  #2009 und später
  BwD_AGE2_2009TO2011=redefine_col(gebaeude$GEB_3.11),
  #Average Age
  BwD_AGE2_AVG=(redefine_col(gebaeude$GEB_3.2)*1850+redefine_col(gebaeude$GEB_3.3)*1934.5
                +redefine_col(gebaeude$GEB_3.4)*1964.5+redefine_col(gebaeude$GEB_3.5)*1982.5
                +redefine_col(gebaeude$GEB_3.6)*1988.5+redefine_col(gebaeude$GEB_3.7)*1993
                +redefine_col(gebaeude$GEB_3.8)*1998+redefine_col(gebaeude$GEB_3.9)*2002.5
                +redefine_col(gebaeude$GEB_3.10)*2006.5+redefine_col(gebaeude$GEB_3.11)*2010)
  /redefine_col(gebaeude$GEB_3.1),
  
  #Gebäude mit Wohnraum nach Eigentumsform des Gebäudes
  #Gesamt
  BwD_OWNER_TOTAL=redefine_col(gebaeude$GEB_4.1),
  #Gemeinschaft von Wohnungseigentümern/-innen
  BwD_OWNER_ASSOC=redefine_col(gebaeude$GEB_4.2),
  #Privatperson/-en  
  BwD_OWNER_PRIV=redefine_col(gebaeude$GEB_4.3),
  #Wohnungsgenossenschaft  
  BwD_OWNER_BUILDSOC=redefine_col(gebaeude$GEB_4.4),
  #Kommune oder kommunales Wohnungsunternehmen     
  BwD_OWNER_MUNDWELLCOMP=redefine_col(gebaeude$GEB_4.5),
  #Privatwirtschaftliches Wohnungsunternehmen
  BwD_OWNER_PRIVDWELLCOMP=redefine_col(gebaeude$GEB_4.6),
  #Anderes privatwirtschaftliches Unternehmen
  BwD_OWNER_OTHERPRIVCOMP=redefine_col(gebaeude$GEB_4.7),
  #Bund oder Land
  BwD_OWNER_GOV=redefine_col(gebaeude$GEB_4.8),
  #Organisation ohne Erwerbszweck
  BwD_OWNER_ORG=redefine_col(gebaeude$GEB_4.9),
  
  
  #Gebäude mit Wohnraum nach Heizungsart    				
  #Gesamt
  BwD_HEAT_TOTAL=redefine_col(gebaeude$GEB_5.1),
  #Fernheizung (Fernwärme)
  BwD_HEAT_DISTR=redefine_col(gebaeude$GEB_5.2),
  #Etagenheizung
  BwD_HEAT_SCDWELL=redefine_col(gebaeude$GEB_5.3),
  #Blockheizung
  BwD_HEAT_BLOCKTYPE=redefine_col(gebaeude$GEB_5.4),
  #Zentralheizung
  BwD_HEAT_CENTRAL=redefine_col(gebaeude$GEB_5.5),
  #Einzel- oder Mehrraumöfen (auch Nachtspeicherheizung)
  BwD_HEAT_SNGLROOM=redefine_col(gebaeude$GEB_5.6),
  #Keine Heizung im Gebäude oder in den Wohnungen"
  BwD_HEAT_NONE=redefine_col(gebaeude$GEB_5.7),
  
  
  #Gebäude mit Wohnraum nach Zahl der Wohnungen im Gebäude  				
  #Gesamt				
  BwD_NODWELL_TOTAL=redefine_col(gebaeude$GEB_6.1),
  #1 Wohnung  
  BwD_NODWELL_1=redefine_col(gebaeude$GEB_6.2),
  #2 Wohnungen  
  BwD_NODWELL_2=redefine_col(gebaeude$GEB_6.3),
  #3 - 6 Wohnungen  
  BwD_NODWELL_3TO6=redefine_col(gebaeude$GEB_6.4),
  #7 - 12 Wohnungen  
  BwD_NODWELL_7TO12=redefine_col(gebaeude$GEB_6.5),
  #13 und mehr Wohnungen
  BwD_NODWELL_MTH13=redefine_col(gebaeude$GEB_6.6),
  
  
  #Gebäude mit Wohnraum nach Gebäudetyp-Bauweise  			
  #Gesamt
  BwD_TYPE_TOTAL=redefine_col(gebaeude$GEB_7.1),
  #Freistehendes Haus
  BwD_TYPE_FAM=redefine_col(gebaeude$GEB_7.2),
  #Doppelhaushälfte
  BwD_TYPE_SEMID=redefine_col(gebaeude$GEB_7.3),
  #Gereihtes Haus
  BwD_TYPE_TOWN=redefine_col(gebaeude$GEB_7.4),
  #Anderer Gebäudetyp
  BwD_TYPE_OTHER=redefine_col(gebaeude$GEB_7.5),
  
  #Wohnungen in Gebäuden mit Wohnraum  			
  #Gesamt	
  D_UTIL_TOTAL=redefine_col(gebaeude$WHG_1.1),
  #Wohnungen in Wohngebäuden  		
  D_UTIL_ONLY=redefine_col(gebaeude$WHG_1.2),
  #davon in Wohngebäuden (ohne Wohnheime)  	
  D_UTIL_woDORM=redefine_col(gebaeude$WHG_1.3),
  #davon in Wohnheimen  
  D_UTIL_DORM=redefine_col(gebaeude$WHG_1.4),
  #in sonstigen Gebäuden mit Wohnraum
  D_UTIL_OTHER=redefine_col(gebaeude$WHG_1.5),
  
  #Wohnungen nach Baujahr (Jahrzehnte)  								
  #Gesamt							
  D_AGE_TOTAL=redefine_col(gebaeude$WHG_2.1),
  #Vor 1919  
  D_AGE_BEFORE1919=redefine_col(gebaeude$WHG_2.2),
  #1919 - 1949  
  D_AGE_1919TO1949=redefine_col(gebaeude$WHG_2.3),
  #1950-1959  
  D_AGE_1950TO1959=redefine_col(gebaeude$WHG_2.4),
  #1960-1969  
  D_AGE_1960TO1969=redefine_col(gebaeude$WHG_2.5),
  #1970-1979  
  D_AGE_1970TO1979=redefine_col(gebaeude$WHG_2.6),
  #1980-1989  
  D_AGE_1980TO1989=redefine_col(gebaeude$WHG_2.7),
  #1990-1999  
  D_AGE_1990TO1999=redefine_col(gebaeude$WHG_2.8),
  #2000-2005  
  D_AGE_2000TO2005=redefine_col(gebaeude$WHG_2.9),
  #2006 und später
  D_AGE_2006TO2011=redefine_col(gebaeude$WHG_2.10),
  #Average Age
  D_AGE_AVG=(redefine_col(gebaeude$WHG_2.2)*1850+redefine_col(gebaeude$WHG_2.3)*1935
             +redefine_col(gebaeude$WHG_2.4)*1954.5+redefine_col(gebaeude$WHG_2.5)*1964.5
             +redefine_col(gebaeude$WHG_2.6)*1974.5+redefine_col(gebaeude$WHG_2.7)*1984.5
             +redefine_col(gebaeude$WHG_2.8)*1994.5+redefine_col(gebaeude$WHG_2.9)*2002.5
             +redefine_col(gebaeude$WHG_2.10)*2008.5)/redefine_col(gebaeude$WHG_2.1),
  
  
  #Wohnungen nach Baujahr (Mikrozenzus-Klassen)  									
  #Gesamt									
  D_AGE2_TOTAL=redefine_col(gebaeude$WHG_3.1),
  #Vor 1919  
  D_AGE2_BEFORE1919=redefine_col(gebaeude$WHG_3.2),
  #1919 - 1948    
  D_AGE2_1919TO1948=redefine_col(gebaeude$WHG_3.3),
  #1949 - 1978    
  D_AGE2_1949TO1978=redefine_col(gebaeude$WHG_3.4),
  #1979 - 1986    
  D_AGE2_1979TO1986=redefine_col(gebaeude$WHG_3.5),
  #1987 - 1990    
  D_AGE2_1987TO1990=redefine_col(gebaeude$WHG_3.6),
  #1991 - 1995    
  D_AGE2_1991TO1995=redefine_col(gebaeude$WHG_3.7),
  #1996 - 2000    
  D_AGE2_1996TO2000=redefine_col(gebaeude$WHG_3.8),
  #2001 - 2004    
  D_AGE2_2001TO2004=redefine_col(gebaeude$WHG_3.9),
  #2005 - 2008    
  D_AGE2_2005TO2008=redefine_col(gebaeude$WHG_3.10),
  #2009 und später
  D_AGE2_2009TO2011=redefine_col(gebaeude$WHG_3.11),
  BwD_AGE2_AVG=(redefine_col(gebaeude$WHG_3.2)*1850+redefine_col(gebaeude$WHG_3.3)*1934.5
                +redefine_col(gebaeude$WHG_3.4)*1964.5+redefine_col(gebaeude$WHG_3.5)*1982.5
                +redefine_col(gebaeude$WHG_3.6)*1988.5+redefine_col(gebaeude$WHG_3.7)*1993
                +redefine_col(gebaeude$WHG_3.8)*1998+redefine_col(gebaeude$WHG_3.9)*2002.5
                +redefine_col(gebaeude$WHG_3.10)*2006.5+redefine_col(gebaeude$WHG_3.11)*2010)
  /redefine_col(gebaeude$GEB_3.1),
  
  
  
  #Wohnungen nach Eigentumsform des Gebäudes  							
  #Gesamt
  D_OWNER_TOTAL=redefine_col(gebaeude$WHG_4.1),
  #Gemeinschaft von Wohnungseigentümern/-innen
  D_OWNER_ASSOC=redefine_col(gebaeude$WHG_4.2),
  #Privatperson/-en  
  D_OWNER_PRIV=redefine_col(gebaeude$WHG_4.3),
  #Wohnungsgenossenschaft  
  D_OWNER_BUILDSOC=redefine_col(gebaeude$WHG_4.4),
  #Kommune oder kommunales Wohnungsunternehmen
  D_OWNER_MUNDWELLCOMP=redefine_col(gebaeude$WHG_4.5),
  #Privatwirtschaftliches Wohnungsunternehmen
  D_OWNER_PRIVDWELLCOMP=redefine_col(gebaeude$WHG_4.6),
  #Anderes privatwirtschaftliches Unternehmen
  D_OWNER_OTHERPRIVCOMP=redefine_col(gebaeude$WHG_4.7),
  #Bund oder Land
  D_OWNER_GOV=redefine_col(gebaeude$WHG_4.8),
  #Organisation ohne Erwerbszweck"
  D_OWNER_ORG=redefine_col(gebaeude$WHG_4.9),
  
  
  #Wohnungen nach Heizungsart  					
  #Gesamt
  D_HEAT_TOTAL=redefine_col(gebaeude$WHG_5.1),
  #Fernheizung (Fernwärme)
  D_HEAT_DISTR=redefine_col(gebaeude$WHG_5.2),
  #Etagenheizung
  D_HEAT_SCDWELL=redefine_col(gebaeude$WHG_5.3),
  #Blockheizung
  D_HEAT_BLOCKTYPE=redefine_col(gebaeude$WHG_5.4),
  #Zentralheizung
  D_HEAT_CENTRAL=redefine_col(gebaeude$WHG_5.5),
  #Einzel- oder Mehrraumöfen (auch Nachtspeicherheizung)
  D_HEAT_SNGLROOM=redefine_col(gebaeude$WHG_5.6),
  #Keine Heizung im Gebäude oder in den Wohnungen"
  D_HEAT_NONE=redefine_col(gebaeude$WHG_5.7),
  
  
  #Wohnungen in Gebäuden mit Wohnraum nach Art der Nutzung  			
  #Gesamt			
  D_USE_TOTAL=redefine_col(gebaeude$WHG_6.1),
  #Von Eigentümer/-in bewohnt
  D_USE_OWNER=redefine_col(gebaeude$WHG_6.2),
  #Zu Wohnzwecken vermietet (auch mietfrei)
  D_USE_RENT=redefine_col(gebaeude$WHG_6.3),
  #Ferien- oder Freizeitwohnung
  D_USE_HOLYDAY=redefine_col(gebaeude$WHG_6.4),
  #Leer stehend
  D_USE_VAC=redefine_col(gebaeude$WHG_6.5),
  
  #Wohnungen in Gebäuden mit Wohnraum nach Fläche der Wohnung in m² (20 m²-Intervalle)   									
  #Gesamt	
  D_AREA_TOTAL=redefine_col(gebaeude$WHG_7.1),
  #Unter 40    
  D_AREA_LTH40=redefine_col(gebaeude$WHG_7.2),
  #40 - 59    
  D_AREA_40TO59=redefine_col(gebaeude$WHG_7.3),
  #60 - 79    
  D_AREA_60TO79=redefine_col(gebaeude$WHG_7.4),
  #80 - 99    
  D_AREA_80TO99=redefine_col(gebaeude$WHG_7.5),
  #100 - 119    
  D_AREA_100TO119=redefine_col(gebaeude$WHG_7.6),
  #120 - 139    
  D_AREA_120TO139=redefine_col(gebaeude$WHG_7.7),
  #140 - 159    
  D_AREA_140TO159=redefine_col(gebaeude$WHG_7.8),
  #160 - 179    
  D_AREA_160TO179=redefine_col(gebaeude$WHG_7.9),
  #180 - 199    
  D_AREA_180TO199=redefine_col(gebaeude$WHG_7.10),
  #200 und mehr
  D_AREA_MTH200=redefine_col(gebaeude$WHG_7.11),
  
  #Wohnungen in Gebäuden mit Wohnraum nach Zahl der Räume  						
  #Gesamt					
  D_NOROOMS_TOTAL=redefine_col(gebaeude$WHG_8.1),
  #1 Raum  
  D_NOROOMS_1=redefine_col(gebaeude$WHG_8.2),
  #2 Räume  
  D_NOROOMS_2=redefine_col(gebaeude$WHG_8.3),
  #3 Räume  
  D_NOROOMS_3=redefine_col(gebaeude$WHG_8.4),
  #4 Räume  
  D_NOROOMS_4=redefine_col(gebaeude$WHG_8.5),
  #5 Räume  
  D_NOROOMS_5=redefine_col(gebaeude$WHG_8.6),
  #6 Räume  
  D_NOROOMS_6=redefine_col(gebaeude$WHG_8.7),
  #7 und mehr Räume
  D_NOROOMS_MTH7=redefine_col(gebaeude$WHG_8.8),
  
  
  
  #Wohnungen nach Gebäudetyp-Bauweise  			
  #Gesamt	
  D_TYPE_TOTAL=redefine_col(gebaeude$WHG_9.1),
  #Freistehendes Haus  
  D_TYPE_FAM=redefine_col(gebaeude$WHG_9.2),
  #Doppelhaushälfte  
  D_TYPE_SEMID=redefine_col(gebaeude$WHG_9.3),
  #Gereihtes Haus  
  D_TYPE_TOWN=redefine_col(gebaeude$WHG_9.4),
  #Anderer Gebäudetyp
  D_TYPE_OTHER=redefine_col(gebaeude$WHG_9.5),
  stringsAsFactors=FALSE, row.names = NULL)





#Verbose Names and Titles
VERBOSE_EN= as.data.frame(rbind(DISTR_PLOT_TITLE=list(label="",unit="",info="Distribution review",title="Distribution Check",description=""),
                             DISTR_PLOT_XLAB=list(label="Value Ranges [(n,m)]",unit="(n,m)",info="Value Ranges",title="",description=""),
                             DISTR_PLOT_YLAB=list(label="Number of Samples [n]",unit="[n]",info="Number of Samples",title="",description=""),
                             DISTR_PLOT_COMMENT=list(label="",unit="",info="Population Density",title="",description=""),
                             CORR_PLOT_TITLE=list(label="",unit="",info="",title="Correlation Chart",description=""),
                             CORR_PLOT_XLAB=list(label="Amount of",unit="",info="Amount of",title="",description=""),
                             CORR_PLOT_YLAB=list(label="Number of Samples",unit="[n]",info="",title="",description=""),
                             CORR_SUM_PLOT_TITLE=list(label="",unit="",info="",title="Correlation Sum Check",description=""),
                             CORR_SUM_PLOT_XLAB=list(label="Amount of",unit="",info="Amount of",title="Buildings",description=""),
                             CORR_SUM_PLOT_YLAB=list(label="Number of Samples",unit="[n]",info="",title="",description=""),
                             P_DENS=list(label="Population Density",unit="[n/km2]",info="Population Density",title="Density of population",description="Density of population"),
                             B_DENS=list(label="Density of Buildings",unit="[n/km2]",info="Density of Buildings",title="Density of buildings",description="Density of buildings"),
                             D_DENS=list(label="Density of Flats",unit="[n/km2]",info="Density of Flats",title="Density of flats",description="Density of flats"),
                             
                             BUILDINGS_BY_UTIL1=list(label="",unit="",info="Bld w Hous by Kind",title="Buildings w/ housing by kind",description="Buildings with housing by kind of the building"),
                             BUILDINGS_BY_UTIL2=list(label="",unit="",info="Bld Resid by Kind",title="Residential buildings by kind",description="Residential buildings by kind of the building"),
                             BUILDINGS_BY_UTIL=list(label="",unit="",info="Bld by kind",title="Buildings w/ housing by kind",description="Buildings with housing by kind of the building"),
                             BwD_UTIL_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing"),
                             BwD_UTIL_ONLY=list(label="Residential buildings",unit="[n]",info="Residential",title="Buildings w/ housing (Residential)",description="Buildings with housing of kind residential"),
                             BwD_UTIL_woDORM=list(label="Residential buildings w/o dormitories",unit="[n]",info="Resid w/o Dorm",title="(Residential w/o dormitories)",description="Buildings with housing of kind residential without dormitories etc."),
                             BwD_UTIL_DORM=list(label="Residential buildings, only dormitories",unit="[n]",info="Dormitories",title="Buildings w/ housing (Dormitories)",description="Buildings with housing of kind residential (only dormitories etc.)"),
                             BwD_UTIL_OTHER=list(label="Nonresidential buildings",unit="[n]",info="Nonresidential",title="Buildings w/ housing (Nonresidential)",description="Buildings with housing of kind nonresidential"),
                             
                             DWELLINGS_BY_UTIL1=list(label="",unit="",info="Flats Resid by Kind",title="Flats in residential buildings by kind",description="Flats in residential buildings by kind of the building"),
                             DWELLINGS_BY_UTIL2=list(label="",unit="",info="Flats Bld w Hous by Kind",title="Flats in buildings w/ housing by kind",description="Flats in buildings with housing by kind of the building"),
                             DWELLINGS_BY_UTIL=list(label="",unit="",info="Flats Bld w Hous by Kind",title="Flats in buildings w/ housing by kind",description="Flats in buildings with housing by kind of the building"),
                             D_UTIL_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing"),
                             D_UTIL_ONLY=list(label="Flats in residential buildings",unit="[n]",info="Residential",title="Flats in buildings w/ housing (Residential)",description="Flats in buildings with housing of kind residential"),
                             D_UTIL_woDORM=list(label="Flats in residential buildings w/o dormitories",unit="[n]",info="Dormitories",title="Flats in buildings w/ housing (Dormitories)",description="Flats in buildings with housing of kind residential (only dormitories etc.)"),
                             D_UTIL_DORM=list(label="Flats in residential buildings, only dormitories",unit="[n]",info="Dormitories",title="Flats in buildings w/ housing (Dormitories)",description="Flats in buildings with housing of kind residential (only dormitories etc.)"),
                             D_UTIL_OTHER=list(label="Flats in ronresidential buildings",unit="[n]",info="Nonresidential",title="Flats in buildings w/ housing (Nonresidential)",description="Flats in buildings with housing of kind nonresidential"),
                             
                             
                             
                             BUILDINGS_BY_AGE=list(label="",unit="",info="Bld w Hous by Age 1",title="Buildings w/ housing by age 1",description="Buildings with housing by age of the building (div 1)"),
                             BwD_AGE_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_AGE_BEFORE1919=list(label="Buildings before 1919",unit="[n]",info="before 1919",title="Buildings w/ housing -1919",description="Buildings with housing built before 1919"),
                             BwD_AGE_1919TO1949=list(label="Buildings 1919-1949",unit="[n]",info="1919-1949",title="Buildings w/ housing 1919-1949",description="Buildings with housing built between 1919 and 1949"),
                             BwD_AGE_1950TO1959=list(label="Buildings 1950-1959",unit="[n]",info="1950-1959",title="Buildings w/ housing 1950-1959",description="Buildings with housing built between 1950 and 1959"),
                             BwD_AGE_1960TO1969=list(label="Buildings 1960-1969",unit="[n]",info="1960-1969",title="Buildings w/ housing 1960-1969",description="Buildings with housing built between 1960 and 1969"),
                             BwD_AGE_1970TO1979=list(label="Buildings 1970-1979",unit="[n]",info="1970-1979",title="Buildings w/ housing 1970-1979",description="Buildings with housing built between 1970 and 1979"),
                             BwD_AGE_1980TO1989=list(label="Buildings 1980-1989",unit="[n]",info="1980-1989",title="Buildings w/ housing 1980-1989",description="Buildings with housing built between 1980 and 1989"),
                             BwD_AGE_1990TO1999=list(label="Buildings 1990-1999",unit="[n]",info="1990-1999",title="Buildings w/ housing 1990-1999",description="Buildings with housing built between 1990 and 1999"),
                             BwD_AGE_2000TO2005=list(label="Buildings 2000-2005",unit="[n]",info="2000-2005",title="Buildings w/ housing 2000-2005",description="Buildings with housing built between 2000 and 2005"),
                             BwD_AGE_2006TO2011=list(label="Buildings after 2005",unit="[n]",info="after 2005",title="Buildings w/ housing 2006-",description="Buildings with housing built after 2005"),
                             BwD_AGE_AVG=list(label="Average year of construction",unit="[y]",info="average year",title="Buildings w/ housing average year",description="Buildings with housing, average year of construction"),
                             
                             DWELLINGS_BY_AGE=list(label="",unit="",info="Flats Bld w Hous by Age 1",title="Flats in buildings w/ housing by age 1",description="Flats in buildings with housing by age of the building (div 1)"),
                             D_AGE_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing"),
                             D_AGE_BEFORE1919=list(label="Flats in buildings before 1919",unit="[n]",info="before 1919",title="Flats in buildings w/ housing -1919",description="Flats in buildings with housing built before 1919"),
                             D_AGE_1919TO1949=list(label="Flats in buildings 1919-1949",unit="[n]",info="1919-1949",title="Flats in buildings w/ housing 1919-1949",description="Flats in buildings with housing built between 1919 and 1949"),
                             D_AGE_1950TO1959=list(label="Flats in buildings 1950-1959",unit="[n]",info="1950-1959",title="Flats in buildings w/ housing 1950-1959",description="Flats in buildings with housing built between 1950 and 1959"),
                             D_AGE_1960TO1969=list(label="Flats in buildings 1960-1969",unit="[n]",info="1960-1969",title="Flats in buildings w/ housing 1960-1969",description="Flats in buildings with housing built between 1960 and 1969"),
                             D_AGE_1970TO1979=list(label="Flats in buildings 1970-1979",unit="[n]",info="1970-1979",title="Flats in buildings w/ housing 1970-1979",description="Flats in buildings with housing built between 1970 and 1979"),
                             D_AGE_1980TO1989=list(label="Flats in buildings 1980-1989",unit="[n]",info="1980-1989",title="Flats in buildings w/ housing 1980-1989",description="Flats in buildings with housing built between 1980 and 1989"),
                             D_AGE_1990TO1999=list(label="Flats in buildings 1990-1999",unit="[n]",info="1990-1999",title="Flats in buildings w/ housing 1990-1999",description="Flats in buildings with housing built between 1990 and 1999"),
                             D_AGE_2000TO2005=list(label="Flats in buildings 2000-2005",unit="[n]",info="2000-2005",title="Flats in buildings w/ housing 2000-2005",description="Flats in buildings with housing built between 2000 and 2005"),
                             D_AGE_2006TO2011=list(label="Flats in buildings after 2005",unit="[n]",info="after 2005",title="Flats in buildings w/ housing 2006-",description="Flats in buildings with housing built after 2005"),
                             D_AGE_AVG=list(label="Average year of construction",unit="[y]",info="average year",title="Flats in buildings w/ housing average year",description="Flats in buildings with housing, average year of construction"),
                             
                             BUILDINGS_BY_AGE2=list(label="",unit="",info="Bld w Hous by age 2",title="Buildings w/ housing by age 2",description="Buildings with housing by age of the building (div 2)"),
                             BwD_AGE2_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_AGE2_BEFORE1919=list(label="Buildings before 1919",unit="[n]",info="before 1919",title="Buildings w/ housing -1919",description="Buildings with housing built before 1919"),
                             BwD_AGE2_1919TO1948=list(label="Buildings 1919-1948",unit="[n]",info="1919-1948",title="Buildings w/ housing 1919-1948",description="Buildings with housing built between 1919 and 1948"),
                             BwD_AGE2_1949TO1978=list(label="Buildings 1949-1978",unit="[n]",info="1949-1978",title="Buildings w/ housing 1949-1978",description="Buildings with housing built between 1949 and 1978"),
                             BwD_AGE2_1979TO1986=list(label="Buildings 1979-1986",unit="[n]",info="1979-1986",title="Buildings w/ housing 1979-1986",description="Buildings with housing built between 1979 and 1986"),
                             BwD_AGE2_1987TO1990=list(label="Buildings 1987-1990",unit="[n]",info="1987-1990",title="Buildings w/ housing 1987-1990",description="Buildings with housing built between 1987 and 1990"),
                             BwD_AGE2_1991TO1995=list(label="Buildings 1991-1995",unit="[n]",info="1991-1995",title="Buildings w/ housing 1991-1995",description="Buildings with housing built between 1991 and 1995"),
                             BwD_AGE2_1996TO2000=list(label="Buildings 1996-2000",unit="[n]",info="1996-2000",title="Buildings w/ housing 1996-2000",description="Buildings with housing built between 1996 and 2000"),
                             BwD_AGE2_2001TO2004=list(label="Buildings 2001-2004",unit="[n]",info="2001-2004",title="Buildings w/ housing 2001-2004",description="Buildings with housing built between 2001 and 2004"),
                             BwD_AGE2_2005TO2008=list(label="Buildings 2005-2008",unit="[n]",info="2005-2008",title="Buildings w/ housing 2005-2008",description="Buildings with housing built between 2005 and 2008"),
                             BwD_AGE2_2009TO2011=list(label="Buildings after 2008",unit="[n]",info="after 2008",title="Buildings w/ housing 2009-",description="Buildings with housing built after 2008 "),
                             BwD_AGE2_AVG=list(label="Average year of construction",unit="[y]",info="average year",title="Buildings w/ housing average year",description="Buildings with housing, average year of construction"),
                             
                             
                             DWELLINGS_BY_AGE2=list(label="",unit="",info="Flats Bld w Hous by age 2",title="Flats in buildings w/ housing by age 2",description="Flats in buildings with housing by age of the building (div 2)"),
                             D_AGE2_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_AGE2_BEFORE1919=list(label="Flats in buildings before 1919",unit="[n]",info="before 1919",title="Flats in buildings w/ housing -1919",description="Flats in buildings with housing built before 1919"),
                             D_AGE2_1919TO1948=list(label="Flats in buildings 1919-1948",unit="[n]",info="1919-1948",title="Flats in buildings w/ housing 1919-1948",description="Flats in buildings with housing built between 1919 and 1948"),
                             D_AGE2_1949TO1978=list(label="Flats in buildings 1949-1978",unit="[n]",info="1949-1978",title="Flats in buildings w/ housing 1949-1978",description="Flats in buildings with housing built between 1949 and 1978"),
                             D_AGE2_1979TO1986=list(label="Flats in buildings 1979-1986",unit="[n]",info="1979-1986",title="Flats in buildings w/ housing 1979-1986",description="Flats in buildings with housing built between 1979 and 1986"),
                             D_AGE2_1987TO1990=list(label="Flats in buildings 1987-1990",unit="[n]",info="1987-1990",title="Flats in buildings w/ housing 1987-1990",description="Flats in buildings with housing built between 1987 and 1990"),
                             D_AGE2_1991TO1995=list(label="Flats in buildings 1996-2000",unit="[n]",info="1991-1995",title="Flats in buildings w/ housing 1991-1995",description="Flats in buildings with housing built between 1991 and 1995"),
                             D_AGE2_1996TO2000=list(label="Flats in buildings 1996-2000",unit="[n]",info="1996-2000",title="Flats in buildings w/ housing 1996-2000",description="Flats in buildings with housing built between 1996 and 2000"),
                             D_AGE2_2001TO2004=list(label="Flats in buildings 2001-2004",unit="[n]",info="2001-2004",title="Flats in buildings w/ housing 2001-2004",description="Flats in buildings with housing built between 2001 and 2004"),
                             D_AGE2_2005TO2008=list(label="Flats in buildings 2005-2008",unit="[n]",info="2005-2008",title="Flats in buildings w/ housing 2005-2008",description="Flats in buildings with housing built between 2005 and 2008"),
                             D_AGE2_2009TO2011=list(label="Flats in buildings after 2008",unit="[n]",info="after 2008",title="Flats in buildings w/ housing 2009-",description="Flats in buildings with housing built after 2008 "),
                             D_AGE2_AVG=list(label="Average year of construction",unit="[y]",info="average year",title="Flats in buildings w/ housing average year",description="Flats in buildings with housing, average year of construction"),
                             
                             BUILDINGS_BY_OWNER=list(label="",unit="",info="Bld w Hous by Owner",title="Buildings w/ housing by owner",description="Buildings with housing by owner of the building"),
                             BwD_OWNER_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_OWNER_ASSOC=list(label="Buildings owned by housing assiciations",unit="[n]",info="Assiciations",title="Buildings w/ housing (assiciations)",description="Buildings with housing owned by assiciations"),
                             BwD_OWNER_PRIV=list(label="Buildings owned by private persons",unit="[n]",info="Private Persons",title="Buildings w/ housing (private persons)",description="Buildings with housing owned by private persons"),
                             BwD_OWNER_BUILDSOC=list(label="Buildings owned by housing societies",unit="[n]",info="Societies",title="Buildings w/ housing (societies)",description=""),
                             BwD_OWNER_MUNDWELLCOMP=list(label="Buildings owned by municipal institutions",unit="[n]",info="Municipalities",title="Buildings w/ housing (municipalities)",description="Buildings with housing owned by muicipalities and municipal housing companies"),
                             BwD_OWNER_PRIVDWELLCOMP=list(label="Buildings owned by private housing companies",unit="[n]",info="Priv Housing Comp",title="Buildings w/ housing (private housing companies)",description="Buildings with housing owned by private housing companies"),
                             BwD_OWNER_OTHERPRIVCOMP=list(label="Buildings owned by other private companies",unit="[n]",info="Other Priv Comp",title="Buildings w/ housing (other private companies)",description="Buildings with housing owned by other private companies"),
                             BwD_OWNER_GOV=list(label="Buildings owned by governmental institutions",unit="[n]",info="Government",title="Buildings w/ housing (government)",description="Buildings with housing owned by government"),
                             BwD_OWNER_ORG=list(label="Buildings owned by NGOs",unit="[n]",info="NGOs",title="Buildings w/ housing (nongovernment organisations)",description="Buildings with housing owned by nongovernment organisations"),
                             
                             
                             DWELLINGS_BY_OWNER=list(label="",unit="",info="Flats Bld w Hous by Owner",title="Flats in buildings w/ housing by owner",description="Flats in buildings with housing by owner of the building"),
                             D_OWNER_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_OWNER_ASSOC=list(label="Flats owned by housing assiciations",unit="[n]",info="Assiciations",title="Flats in buildings w/ housing (assiciations)",description="Flats owned by assiciations in buildings with housing"),
                             D_OWNER_PRIV=list(label="Flats owned by private persons",unit="[n]",info="Private Persons",title="Flats in buildings w/ housing (private persons)",description="Flats owned by private persons in buildings with housing"),
                             D_OWNER_BUILDSOC=list(label="Flats owned by housing societies",unit="[n]",info="Societies",title="Flats in buildings w/ housing (societies)",description="Flats owned by societies in buildings with housing"),
                             D_OWNER_MUNDWELLCOMP=list(label="Flats owned by municipal institutions",unit="[n]",info="Municipalities",title="Flats in buildings w/ housing (municipalities)",description="Flats owned by muicipalities and municipal housing companies in buildings with housing "),
                             D_OWNER_PRIVDWELLCOMP=list(label="Flats owned by private housing companies",unit="[n]",info="Priv Housing Comp",title="Flats in buildings w/ housing (private housing companies)",description="Flats owned by private housing companies in buildings with housing"),
                             D_OWNER_OTHERPRIVCOMP=list(label="Flats owned by other private companies",unit="[n]",info="Other Priv Comp",title="Flats in buildings w/ housing (other private companies)",description="Flats owned by other private companies in buildings with housing"),
                             D_OWNER_GOV=list(label="Flats owned by governmental institutions",unit="[n]",info="Government",title="Flats in buildings w/ housing (government)",description="Flats owned by government in buildings with housing"),
                             D_OWNER_ORG=list(label="Flats owned by NGOs",unit="[n]",info="NGOs",title="Flats in buildings w/ housing (nongovernment organisations)",description="Flats owned by nongovernment organisations in buildings with housing"),
                             
                             
                             BUILDINGS_BY_HEATSYS=list(label="",unit="",info="Bld w Hous by Heatsys",title="Buildings w/ housing by heating system",description="Buildings with housing by heating system"),
                             BwD_HEAT_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_HEAT_DISTR=list(label="Buildings with district heating",unit="[n]",info="District",title="Buildings w/ housing (district heating)",description="Buildings with housing heated by district heating systems"),
                             BwD_HEAT_SCDWELL=list(label="Buildings with self contained heating",unit="[n]",info="Self contained",title="Buildings w/ housing (self contained heating)",description="Buildings with housing heated by self-contained central heating systems"),
                             BwD_HEAT_BLOCKTYPE=list(label="Buildings with block-type CHPs",unit="[n]",info="Block-type",title="Buildings w/ housing (block-type CHPs)",description="Buildings with housing heated by block-type combined heat and power plants"),
                             BwD_HEAT_CENTRAL=list(label="Buildings with central heating",unit="[n]",info="Central",title="Buildings w/ housing (central heating)",description="Buildings with housing heated by "),
                             BwD_HEAT_SNGLROOM=list(label="Buildings with single room heating",unit="[n]",info="Single Room",title="Buildings w/ housing (single room heating)",description="Buildings with housing heated by single room heating systems including stoves and night storage heaters"),
                             BwD_HEAT_NONE=list(label="Buildings without heating ",unit="[n]",info="No Heating",title="Buildings w/ housing (no heating)",description="Buildings w/ housing without heating systems"),
                             
                             
                             DWELLINGS_BY_HEATSYS=list(label="",unit="",info="Flats Bld w Hous by Heatsys",title="Flats in buildings w/ housing by heating system",description="Flats in buildings with housing by heating system"),
                             D_HEAT_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_HEAT_DISTR=list(label="Flats with district heating",unit="[n]",info="District",title="Flats in buildings w/ housing (district heating)",description="Flats heated by a district heating systems in buildings with housing"),
                             D_HEAT_SCDWELL=list(label="Flats with self contained heating",unit="[n]",info="Self contained",title="Flats in buildings w/ housing (self contained heating)",description="Flats heated by self-contained central heating systems in buildings with housing"),
                             D_HEAT_BLOCKTYPE=list(label="Flats with block-type CHPs",unit="[n]",info="Block-type",title="Flats in buildings w/ housing (block-type CHPs)",description="Flats heated by a block-type combined heat and power plants in buildings with housing"),
                             D_HEAT_CENTRAL=list(label="Flats with central heating",unit="[n]",info="Central",title="Flats in buildings w/ housing (central heating)",description="Flats in buildings with housing heated by a centralheating systems"),
                             D_HEAT_SNGLROOM=list(label="Flats with single room heating",unit="[n]",info="Single Room",title="Flats in buildings w/ housing (single room heating)",description="Flats in buildings with housing heated by single room heating systems including stoves and night storage heaters"),
                             D_HEAT_NONE=list(label="Flats without heating",unit="[n]",info="",title="Flats in buildings w/ housing (no heating)",description="Flats in buildings w/ housing without heating systems"),
                             
                             
                             
                             BUILDINGS_BY_NODWELL=list(label="",unit="",info="Bld w Hous by Flats",title="Buildings w/ housing by number of flats",description="Buildings with housing by number of flats"),
                             BwD_NODWELL_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_NODWELL_1=list(label="Buildings with 1 flat",unit="[n]",info="1 Flat",title="Buildings w/ housing (1 flat)",description="Buildings with housing with 1 flat"),
                             BwD_NODWELL_2=list(label="Buildings with 2 flats",unit="[n]",info="2 Flats",title="Buildings w/ housing (2 flats)",description="Buildings with housing with 2 flats"),
                             BwD_NODWELL_3TO6=list(label="Buildings with 3 up to 6 flats",unit="[n]",info="3-6 Flats",title="Buildings w/ housing (3-6 flats)",description="Buildings with housing with 3 up to 6 flats"),
                             BwD_NODWELL_7TO12=list(label="Buildings with 7 up to 12 flats",unit="[n]",info="7-12 Flats",title="Buildings w/ housing (7-12 flats)",description="Buildings with housing with 7 up to 12 flats"),
                             BwD_NODWELL_MTH13=list(label="Buildings with more than 13 flats",unit="[n]",info=">13 Flats",title="Buildings w/ housing (>13 flats)",description="Buildings with housing with more than 13 flats"),
                             
                             DWELLINGS_BY_NOROOMS=list(label="",unit="",info="Flats Bld w Hous by Rooms",title="Flats in buildings w/ housing by number of rooms",description="Flats in buildings with housing by number of rooms"),
                             D_NOROOMS_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_NOROOMS_1=list(label="Single room flats",unit="[n]",info="1 Room",title="Flats in buildings w/ housing (1 room)",description="Single room flats in buildings with housing"),
                             D_NOROOMS_2=list(label="Two room flats",unit="[n]",info="2 Room",title="Flats in buildings w/ housing (2 room)",description="Two room flats in buildings with housing"),
                             D_NOROOMS_3=list(label="Three room flats",unit="[n]",info="3 Room",title="Flats in buildings w/ housing (3 room)",description="Three room flats in buildings with housing"),
                             D_NOROOMS_4=list(label="Four room flats",unit="[n]",info="4 Room",title="Flats in buildings w/ housing (4 room)",description="Four room flats in buildings with housing"),
                             D_NOROOMS_5=list(label="Five room flats",unit="[n]",info="5 Room",title="Flats in buildings w/ housing (5 room)",description="Five room flats in buildings with housing"),
                             D_NOROOMS_6=list(label="Six room flats",unit="[n]",info="6 Room",title="Flats in buildings w/ housing (6 room)",description="Six room flats in buildings with housing"),
                             D_NOROOMS_MTH7=list(label="Flats with more than six rooms",unit="[n]",info=">6 Room",title="Flats in buildings w/ housing (>6 room)",description="More than six room flats in buildings with housing"),
                             
                             BUILDINGS_BY_TYPE=list(label="",unit="",info="Bld w Hous by Type",title="Buildings w/ housing by type",description="Buildings with housing by building type"),
                             BwD_TYPE_TOTAL=list(label="Total number of buildings",unit="[n]",info="Total",title="Buildings w/ housing",description="Buildings with housing total"),
                             BwD_TYPE_FAM=list(label="Familyhouses",unit="[n]",info="Familyhouses",title="Buildings w/ housing (family houses)",description="Buildings with housing of type family house"),
                             BwD_TYPE_SEMID=list(label="Semi-detached houses",unit="[n]",info="Semi-det Houses",title="Buildings w/ housing (semi-detached houses, half)",description="Buildings with housing of type semi-detached house"),
                             BwD_TYPE_TOWN=list(label="Row houses",unit="[n]",info="Row houses",title="Buildings w/ housing (row houses)",description="Buildings with housing of type row house"),
                             BwD_TYPE_OTHER=list(label="Buildings of other type",unit="[n]",info="Other",title="Buildings w/ housing (other houses)",description="Buildings with housing of other type"),
                             
                             DWELLINGS_BY_TYPE=list(label="",unit="",info="Flats Bld w Hous by Type",title="Flats in buildings w/ housing by type",description="Flats in buildings with housing by building type"),
                             D_TYPE_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_TYPE_FAM=list(label="Flats in familyhouses",unit="[n]",info="Familyhouses",title="Flats in buildings w/ housing (family houses)",description="Flats in buildings with housing of type family house"),
                             D_TYPE_SEMID=list(label="Flats in semi-detached houses",unit="[n]",info="Semi-det Houses ",title="Flats in buildings w/ housing (semi-detached houses, half)",description="Flats in buildings with housing of type semi-detached house"),
                             D_TYPE_TOWN=list(label="Flats in row houses",unit="[n]",info="Row houses",title="Flats in buildings w/ housing (row houses)",description="Flats in buildings with housing of type row house"),
                             D_TYPE_OTHER=list(label="Flats in buildings of other type",unit="[n]",info="Other",title="Flats in buildings w/ housing (other houses)",description="Flats in buildings with housing of other type"),
                             
                             DWELLINGS_BY_USE=list(label="",unit="",info="Flats Bld w Hous by Use",title="Flats in buildings w/ housing by use",description="Flats in buildings with housing by use of the flat"),
                             D_USE_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_USE_OWNER=list(label="Owner-occupied flats",unit="[n]",info="Owner",title="Flats in buildings w/ housing (owner-used)",description="Flats used by the owner in buildings with housing"),
                             D_USE_RENT=list(label="Rental flats",unit="[n]",info="Rental",title="Flats in buildings w/ housing (rental)",description="Rental flats in buildings with housing"),
                             D_USE_HOLYDAY=list(label="Holiday Rental flats",unit="[n]",info="Holyday",title="Flats in buildings w/ housing (holyday rental)",description="Holyday rental flats in buildings with housing"),
                             D_USE_VAC=list(label="Vacant flats",unit="[n]",info="Not in Use",title="Flats in buildings w/ housing (not in use)",description="Unused flats in buildings with housing"),
                             
                             DWELLINGS_BY_AREA=list(label="",unit="",info="Flats Bld w Hous by Area",title="Flats in buildings w/ housing by area",description="Flats in buildings with housing by area of the flat"),
                             D_AREA_TOTAL=list(label="Total number of flats",unit="[n]",info="Total",title="Flats in buildings w/ housing",description="Flats in buildings with housing total"),
                             D_AREA_LTH40=list(label="Flats of less than 40 m2",unit="[n]",info="<40 m2",title="Flats in buildings w/ housing (<40 m2)",description="Flats with an area of less than 40 m2 in buildings with housing"),
                             D_AREA_40TO59=list(label="Flats of 40 m2 up to 59 m2",unit="[n]",info="40-59 m2",title="Flats in buildings w/ housing (40-59 m2)",description="Flats with an area of 40 up to 59 m2 in buildings with housing"),
                             D_AREA_60TO79=list(label="Flats of 60 m2 up to 79 m2",unit="[n]",info="60-79 m2",title="Flats in buildings w/ housing (60-79 m2)",description="Flats with an area of 60 up to 79 m2 in buildings with housing"),
                             D_AREA_80TO99=list(label="Flats of 80 m2 up to 99 m2",unit="[n]",info="80-99 m2",title="Flats in buildings w/ housing (80-99 m2)",description="Flats with an area of 80 up to 99 m2 in buildings with housing"),
                             D_AREA_100TO119=list(label="Flats of 100 m2 up to 119 m2",unit="[n]",info="100-119 m2",title="Flats in buildings w/ housing (100-119 m2)",description="Flats with an area of 100 up to 119 m2 in buildings with housing"),
                             D_AREA_120TO139=list(label="Flats of 120 m2 up to 139 m2",unit="[n]",info="120-139 m2",title="Flats in buildings w/ housing (120-139 m2)",description="Flats with an area of 120 up to 139 m2 in buildings with housing"),
                             D_AREA_140TO159=list(label="Flats of 140 m2 up to 159 m2",unit="[n]",info="140-159 m2",title="Flats in buildings w/ housing (140-159 m2)",description="Flats with an area of 140 up to 159 m2 in buildings with housing"),
                             D_AREA_160TO179=list(label="Flats of 160 m2 up to 179 m2",unit="[n]",info="160-179 m2",title="Flats in buildings w/ housing (160-179 m2)",description="Flats with an area of 160 up to 179 m2 in buildings with housing"),
                             D_AREA_180TO199=list(label="Flats of 180 m2 up to 199 m2",unit="[n]",info="180-199 m2",title="Flats in buildings w/ housing (180-199 m2)",description="Flats with an area of 180 up to 199 m2 in buildings with housing"),
                             D_AREA_MTH200=list(label="Flats of more than 200 m2",unit="[n]",info=">200 m2",title="Flats in buildings w/ housing (<200 m2)",description="Flats with an area of more than 200 m2 in buildings with housing"),
                             
                             U_WALL_YEAR=list(label="Average year of construction",unit="[y]",info="average year",title="Average year of construction",description="Average year of construction"),
                             U_WALL_EFH =list(label="Wall U-Value of singlehomes",unit="[W/(K·m²)]",info="u wall singlehomes",title="Wall U-Value of Singlehomes",description="U-Value of the Walls of Singlehomes"), 
                             U_WALL_RH  =list(label="Wall U-Value of rowhouse",unit="[W/(K·m²)]",info="u wall rowhouse",title="Wall U-Value of Rowhouse",description="U-Value of the Walls of Rowhouse"), 
                             U_WALL_MFH  =list(label="Wall U-Value of multi-family houses",unit="[W/(K·m²)]",info="u wall multi-family houses",title="Wall U-Value of Multi-family Houses",description="U-Value of the Walls of Multi-family Houses"), 
                             U_WALL_GMH =list(label="Wall U-Value of big multi-family houses",unit="[W/(K·m²)]",info="u wall big multi-family houses",title="Wall U-Value of big Multi-family Houses",description="U-Value of the Walls of big Multi-family Houses"), 
                             U_WALL_AVG =list(label="Average Wall U-Value",unit="[W/(K·m²)]",info="u wall average",title="Average Wall U-Value",description="Average U-Value of Walls"),
                             
                             U_ROOF_YEAR=list(label="Average year of construction",unit="[y]",info="average year",title="Average year of construction",description="Average year of construction"),
                             U_ROOF_EFH =list(label="Roof U-Value of singlehomes",unit="[W/(K·m²)]",info="u roof singlehomes",title="Roof U-Value of Singlehomes",description="U-Value of the Roofs of Singlehomes"), 
                             U_ROOF_RH  =list(label="Roof U-Value of rowhouse",unit="[W/(K·m²)]",info="u roof rowhouse",title="Roof U-Value of Rowhouse",description="U-Value of the Roofs of Rowhouse"), 
                             U_ROOF_MFH  =list(label="Roof U-Value of multi-family houses",unit="[W/(K·m²)]",info="u roof multi-family houses",title="Roof U-Value of Multi-family Houses",description="U-Value of the Roofs of Multi-family Houses"), 
                             U_ROOF_GMH =list(label="Roof U-Value of big multi-family houses",unit="[W/(K·m²)]",info="u roof big multi-family houses",title="Roof U-Value of big Multi-family Houses",description="U-Value of the Roofs of big Multi-family Houses"), 
                             U_ROOF_AVG =list(label="Average Roof U-Value",unit="[W/(K·m²)]",info="u Roof average",title="Average roof U-Value",description="Average U-Value of Roofs"),
                             U_ROOF_EFH_VERT =list(label="Roof Vertical U-Value of singlehomes",unit="[W/(K·m²)]",info="u roof vert singlehomes",title="Roof U-Value of Singlehomes",description="U-Value of the Vertical Roofs of Singlehomes"), 
                             U_ROOF_RH_VERT  =list(label="Roof Vertical U-Value of rowhouse",unit="[W/(K·m²)]",info="u roof vert rowhouse",title="Roof U-Value of Rowhouse",description="U-Value of the Vertical Roofs of Rowhouse"), 
                             U_ROOF_MFH_VERT  =list(label="Roof Vertical U-Value of multi-family houses",unit="[W/(K·m²)]",info="u roof vert multi-family houses",title="Vertical Roof U-Value of Multi-family Houses",description="U-Value of the Roofs of Multi-family Houses"), 
                             U_ROOF_GMH_VERT =list(label="Roof Vertical U-Value of big multi-family houses",unit="[W/(K·m²)]",info="u roof vert big multi-family houses",title="U-Value of the Vertical Roofs of big Multi-family Houses",description="U-Value of the Roofs of big Multi-family Houses"), 
                             U_ROOF_AVG_VERT =list(label="Average Vertical Roof U-Value",unit="[W/(K·m²)]",info="u roof vert average",title="Average vertical roof U-Value",description="Average U-Value of Vertical Roofs"),
                             
                             U_BASE_YEAR=list(label="Average year of construction",unit="[y]",info="average year",title="Average year of construction",description="Average year of construction"),
                             U_BASE_EFH =list(label="Base U-Value of singlehomes",unit="[W/(K·m²)]",info="u Base singlehomes",title="base U-Value of Singlehomes",description="U-Value of the Bases of Singlehomes"), 
                             U_BASE_RH  =list(label="Base U-Value of rowhouse",unit="[W/(K·m²)]",info="u Base rowhouse",title="base U-Value of Rowhouse",description="U-Value of the Bases of Rowhouse"), 
                             U_BASE_MFH  =list(label="Base U-Value of multi-family houses",unit="[W/(K·m²)]",info="u base multi-family houses",title="Base U-Value of Multi-family Houses",description="U-Value of the Bases of Multi-family Houses"), 
                             U_BASE_GMH =list(label="Base U-Value of big multi-family houses",unit="[W/(K·m²)]",info="u base big multi-family houses",title="Base U-Value of big Multi-family Houses",description="U-Value of the Bases of big Multi-family Houses"), 
                             U_BASE_AVG =list(label="Average Base U-Value",unit="[W/(K·m²)]",info="u base average",title="Average Base U-Value",description="Average U-Value of Bases")
                             
),stringsAsFactors=FALSE)




info<-function(x) unlist(VERBOSE[x,"short"])
shortdescription<-function(x) unlist(VERBOSE[x,"description1"])
longdescription<-function(x) unlist(VERBOSE[x,"description2"])

