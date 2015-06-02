#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Lookup Function Generators Windows
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         21.05.2015
#
# Descrription: 
# generators for correlation and lookuptables functions in R and in Python.
# windows of buildings
#######################################################################################

#adding verbose for window definitions. VERBOSE is initialized in init.R
# Window Area by Age from 'data_sources/150512-IWU-Aufbereitung/SQ_..._WIND-OUT.csv'"'
WIN_AREA_BY_AGE=c("YEAR","A_WIN_E_BY_AW","A_WIN_S_BY_AW","A_WIN_W_BY_AW","A_WIN_N_BY_AW","A_WIN_BY_AW") #
VERBOSE= as.data.frame(rbind(VERBOSE,
                             YEAR=list(label="Year of Construction",
                                       unit="",
                                       info="Year of Construction",
                                       title="Year of Construction",
                                       description="Year of Construction"
                             ),
                             A_WIN_E_BY_AW=list(label="Window/Wall Ratio EAST",
                                                unit="%",
                                                info="Window/Wall Ratio EAST",
                                                title="Window/Wall Ratio EAST",
                                                description="Window to Wall Ratio in Eastern Direction"
                             ),
                             A_WIN_S_BY_AW=list(label="Window/Wall Ratio (SOUTH)",
                                                unit="%",
                                                info="Window/Wall Ratio (SOUTH)",
                                                title="Window/Wall Ratio (SOUTH)",
                                                description="Window to Wall Ratio in Southern Direction"
                             ),
                             A_WIN_W_BY_AW=list(label="Window/Wall Ratio (WEST)",
                                                unit="%",
                                                info="Window/Wall Ratio (WEST)",
                                                title="Window/Wall Ratio (WEST)",
                                                description="Window to Wall Ratio in Western Direction"
                             ),
                             A_WIN_N_BY_AW=list(label="Window/Wall Ratio (NORTH)",
                                                unit="%",
                                                info="Window/Wall Ratio (NORTH)",
                                                title="Window/Wall Ratio (NORTH)",
                                                description="Window to Wall Ratio in Northern Direction"
                             ),
                             A_WIN_BY_AW=list(label="Window/Wall Ratio",
                                              unit="%",
                                              info="Window/Wall Ratio (ALL) ",
                                              title="Window/Wall Ratio (ALL)",
                                              description="Window to Wall Ratio in all Directions"
                             )
),stringsAsFactors=FALSE)

######## BUILDING AVERAGE ###############
### average building, windows east
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_east_AVG_by_building_age_correlation<-function(
  name="window_wall_ratio_east_AVG_by_building_age_correlation",
  description="Window/Wall Ratio East in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,2)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_east_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_east_AVG_by_building_age_lookup",
               description="Window/Wall Ratio East in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows south
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_south_AVG_by_building_age_correlation<-function(
  name="window_wall_ratio_south_AVG_by_building_age_correlation",
  description="Window/Wall Ratio South in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,3)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_south_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_south_AVG_by_building_age_lookup",
               description="Window/Wall Ratio South in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=3,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows west
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_west_AVG_by_building_age_correlation<-function(
  name="window_wall_ratio_west_AVG_by_building_age_correlation",
  description="Window/Wall Ratio West in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,4)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_west_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_west_AVG_by_building_age_lookup",
               description="Window/Wall Ratio West in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=4,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows north
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_north_AVG_by_building_age_correlation<-function(
  name="window_wall_ratio_north_AVG_by_building_age_correlation",
  description="Window/Wall Ratio North in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,5)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_north_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_north_AVG_by_building_age_lookup",
               description="Window/Wall Ratio North in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=5,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows total
#Typical Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_AVG_by_building_age_correlation<-function(
  name="window_wall_ratio_AVG_by_building_age_correlation",
  description="Window/Wall Ratio in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,6)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_AVG_by_building_age_lookup",
               description="Window/Wall Ratio in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=6,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

######## SINGLE FAMILY HOMES ###############
### average building, windows east
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_east_SFH_by_building_age_correlation<-function(
  name="window_wall_ratio_east_SFH_by_building_age_correlation",
  description="Window/Wall Ratio East in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,2)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_east_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_east_SFH_by_building_age_lookup",
               description="Window/Wall Ratio East in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows south
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_south_SFH_by_building_age_correlation<-function(
  name="window_wall_ratio_south_SFH_by_building_age_correlation",
  description="Window/Wall Ratio South in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,3)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_south_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_south_SFH_by_building_age_lookup",
               description="Window/Wall Ratio South in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv",
               lookup_column=3,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows west
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_west_SFH_by_building_age_correlation<-function(
  name="window_wall_ratio_west_SFH_by_building_age_correlation",
  description="Window/Wall Ratio West in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,4)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_west_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_west_SFH_by_building_age_lookup",
               description="Window/Wall Ratio West in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv",
               lookup_column=4,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows north
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_north_SFH_by_building_age_correlation<-function(
  name="window_wall_ratio_north_SFH_by_building_age_correlation",
  description="Window/Wall Ratio North in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,5)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_north_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_north_SFH_by_building_age_lookup",
               description="Window/Wall Ratio North in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv",
               lookup_column=5,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows total
#Typical Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_SFH_by_building_age_correlation<-function(
  name="window_wall_ratio_SFH_by_building_age_correlation",
  description="Window/Wall Ratio in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,6)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_SFH_by_building_age_lookup",
               description="Window/Wall Ratio in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv",
               lookup_column=6,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

######## SEMI DETACHED HOUSES ###############

### average building, windows east
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_east_SDH_by_building_age_correlation<-function(
  name="window_wall_ratio_east_SDH_by_building_age_correlation",
  description="Window/Wall Ratio East in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,2)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_east_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_east_SDH_by_building_age_lookup",
               description="Window/Wall Ratio East in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows south
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_south_SDH_by_building_age_correlation<-function(
  name="window_wall_ratio_south_SDH_by_building_age_correlation",
  description="Window/Wall Ratio South in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,3)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_south_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_south_SDH_by_building_age_lookup",
               description="Window/Wall Ratio South in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv",
               lookup_column=3,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows west
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_west_SDH_by_building_age_correlation<-function(
  name="window_wall_ratio_west_SDH_by_building_age_correlation",
  description="Window/Wall Ratio West in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,4)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_west_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_west_SDH_by_building_age_lookup",
               description="Window/Wall Ratio West in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv",
               lookup_column=4,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows north
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_north_SDH_by_building_age_correlation<-function(
  name="window_wall_ratio_north_SDH_by_building_age_correlation",
  description="Window/Wall Ratio North in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,5)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_north_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_north_SDH_by_building_age_lookup",
               description="Window/Wall Ratio North in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv",
               lookup_column=5,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows total
#Typical Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_SDH_by_building_age_correlation<-function(
  name="window_wall_ratio_SDH_by_building_age_correlation",
  description="Window/Wall Ratio in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,6)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_SDH_by_building_age_lookup",
               description="Window/Wall Ratio in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH_WIND-OUT.csv",
               lookup_column=6,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

######## MULTI FAMILY HOUSES ###############

### average building, windows east
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_east_MFH_by_building_age_correlation<-function(
  name="window_wall_ratio_east_MFH_by_building_age_correlation",
  description="Window/Wall Ratio East in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,2)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_east_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_east_MFH_by_building_age_lookup",
               description="Window/Wall Ratio East in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows south
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_south_MFH_by_building_age_correlation<-function(
  name="window_wall_ratio_south_MFH_by_building_age_correlation",
  description="Window/Wall Ratio South in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,3)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_south_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_south_MFH_by_building_age_lookup",
               description="Window/Wall Ratio South in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv",
               lookup_column=3,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows west
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_west_MFH_by_building_age_correlation<-function(
  name="window_wall_ratio_west_MFH_by_building_age_correlation",
  description="Window/Wall Ratio West in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,4)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_west_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_west_MFH_by_building_age_lookup",
               description="Window/Wall Ratio West in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv",
               lookup_column=4,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows north
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_north_MFH_by_building_age_correlation<-function(
  name="window_wall_ratio_north_MFH_by_building_age_correlation",
  description="Window/Wall Ratio North in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,5)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_north_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_north_MFH_by_building_age_lookup",
               description="Window/Wall Ratio North in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv",
               lookup_column=5,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows total
#Typical Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_MFH_by_building_age_correlation<-function(
  name="window_wall_ratio_MFH_by_building_age_correlation",
  description="Window/Wall Ratio in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,6)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_MFH_by_building_age_lookup",
               description="Window/Wall Ratio in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv",
               lookup_column=6,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

######## LARGE MULTI FAMILY HOUSES ###############

### average building, windows east
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_east_LMFH_by_building_age_correlation<-function(
  name="window_wall_ratio_east_LMFH_by_building_age_correlation",
  description="Window/Wall Ratio East in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,2)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_east_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_east_LMFH_by_building_age_lookup",
               description="Window/Wall Ratio East in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows south
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_south_LMFH_by_building_age_correlation<-function(
  name="window_wall_ratio_south_LMFH_by_building_age_correlation",
  description="Window/Wall Ratio South in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,3)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_south_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_south_LMFH_by_building_age_lookup",
               description="Window/Wall Ratio South in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv",
               lookup_column=3,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows west
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_west_LMFH_by_building_age_correlation<-function(
  name="window_wall_ratio_west_LMFH_by_building_age_correlation",
  description="Window/Wall Ratio West in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,4)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_west_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_west_LMFH_by_building_age_lookup",
               description="Window/Wall Ratio West in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv",
               lookup_column=4,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows north
#Typical Western Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_north_LMFH_by_building_age_correlation<-function(
  name="window_wall_ratio_north_LMFH_by_building_age_correlation",
  description="Window/Wall Ratio North in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,5)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_north_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_north_LMFH_by_building_age_lookup",
               description="Window/Wall Ratio North in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv",
               lookup_column=5,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

### average building, windows total
#Typical Window/Wall Ratio depending on the Year of Construction (Corellation)
build_window_wall_ratio_LMFH_by_building_age_correlation<-function(
  name="window_wall_ratio_LMFH_by_building_age_correlation",
  description="Window/Wall Ratio in Correlation to the Building Age"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
    l.db=read.csv2(csvsource)[,c(1,6)]
    l.investigation=new_OeQ_Inv(l.db,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Window/Wall Ratio depending on the Year of Construction (Lookuptable)
build_window_wall_ratio_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="window_wall_ratio_LMFH_by_building_age_lookup",
               description="Window/Wall Ratio in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv",
               lookup_column=6,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=resolution,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021))
}  

FORCERUN=T
if(FORCERUN==TRUE){
build_window_wall_ratio_east_AVG_by_building_age_correlation()
build_window_wall_ratio_east_AVG_by_building_age_lookup()
build_window_wall_ratio_east_SFH_by_building_age_correlation()
build_window_wall_ratio_east_SFH_by_building_age_lookup()
build_window_wall_ratio_east_SDH_by_building_age_correlation()
build_window_wall_ratio_east_SDH_by_building_age_lookup()
build_window_wall_ratio_east_MFH_by_building_age_correlation()
build_window_wall_ratio_east_MFH_by_building_age_lookup()
build_window_wall_ratio_east_LMFH_by_building_age_correlation()
build_window_wall_ratio_east_LMFH_by_building_age_lookup()

build_window_wall_ratio_south_AVG_by_building_age_correlation()
build_window_wall_ratio_south_AVG_by_building_age_lookup()
build_window_wall_ratio_south_SFH_by_building_age_correlation()
build_window_wall_ratio_south_SFH_by_building_age_lookup()
build_window_wall_ratio_south_SDH_by_building_age_correlation()
build_window_wall_ratio_south_SDH_by_building_age_lookup()
build_window_wall_ratio_south_MFH_by_building_age_correlation()
build_window_wall_ratio_south_MFH_by_building_age_lookup()
build_window_wall_ratio_south_LMFH_by_building_age_correlation()
build_window_wall_ratio_south_LMFH_by_building_age_lookup()

build_window_wall_ratio_west_AVG_by_building_age_correlation()
build_window_wall_ratio_west_AVG_by_building_age_lookup()
build_window_wall_ratio_west_SFH_by_building_age_correlation()
build_window_wall_ratio_west_SFH_by_building_age_lookup()
build_window_wall_ratio_west_SDH_by_building_age_correlation()
build_window_wall_ratio_west_SDH_by_building_age_lookup()
build_window_wall_ratio_west_MFH_by_building_age_correlation()
build_window_wall_ratio_west_MFH_by_building_age_lookup()
build_window_wall_ratio_west_LMFH_by_building_age_correlation()
build_window_wall_ratio_west_LMFH_by_building_age_lookup()

build_window_wall_ratio_north_AVG_by_building_age_correlation()
build_window_wall_ratio_north_AVG_by_building_age_lookup()
build_window_wall_ratio_north_SFH_by_building_age_correlation()
build_window_wall_ratio_north_SFH_by_building_age_lookup()
build_window_wall_ratio_north_SDH_by_building_age_correlation()
build_window_wall_ratio_north_SDH_by_building_age_lookup()
build_window_wall_ratio_north_MFH_by_building_age_correlation()
build_window_wall_ratio_north_MFH_by_building_age_lookup()
build_window_wall_ratio_north_LMFH_by_building_age_correlation()
build_window_wall_ratio_north_LMFH_by_building_age_lookup()

build_window_wall_ratio_AVG_by_building_age_correlation()
build_window_wall_ratio_AVG_by_building_age_lookup()
build_window_wall_ratio_SFH_by_building_age_correlation()
build_window_wall_ratio_SFH_by_building_age_lookup()
build_window_wall_ratio_SDH_by_building_age_correlation()
build_window_wall_ratio_SDH_by_building_age_lookup()
build_window_wall_ratio_MFH_by_building_age_correlation()
build_window_wall_ratio_MFH_by_building_age_lookup()
build_window_wall_ratio_LMFH_by_building_age_correlation()
build_window_wall_ratio_LMFH_by_building_age_lookup()
}
               
plot(1850:2020,window_wall_ratio_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.5),
     main="Window/Wall Ratio Total\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("SFH (LUT)","SFH (COR)","SDH (LUT)","SDH (COR)","MFH (LUT)","MFH (COR)","LMFH (LUT)","LMFH (COR)","AVG (LUT)","AVG (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_east_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.3),
     main="Window/Wall Ratio of Eastern Walls\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_east_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_east_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_east_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_east_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_east_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_east_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_east_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_east_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("SFH (LUT)","SFH (COR)","SDH (LUT)","SDH (COR)","MFH (LUT)","MFH (COR)","LMFH (LUT)","LMFH (COR)","AVG (LUT)","AVG (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_south_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.3),
     main="Window/Wall Ratio of Southern Walls\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_south_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_south_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_south_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_south_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_south_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_south_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_south_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("SFH (LUT)","SFH (COR)","SDH (LUT)","SDH (COR)","MFH (LUT)","MFH (COR)","LMFH (LUT)","LMFH (COR)","AVG (LUT)","AVG (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_west_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.3),
     main="Window/Wall Ratio of Western Walls\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_west_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_west_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_west_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_west_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_west_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_west_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_west_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("SFH (LUT)","SFH (COR)","SDH (LUT)","SDH (COR)","MFH (LUT)","MFH (COR)","LMFH (LUT)","LMFH (COR)","AVG (LUT)","AVG (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_north_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.3),
     main="Window/Wall Ratio of Northern Walls\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_north_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_north_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_north_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_north_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_north_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_north_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_north_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("SFH (LUT)","SFH (COR)","SDH (LUT)","SDH (COR)","MFH (LUT)","MFH (COR)","LMFH (LUT)","LMFH (COR)","AVG (LUT)","AVG (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))


plot(1850:2020,window_wall_ratio_east_AVG_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.6),
     main="Window/Wall Ratio AVG\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_AVG_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_AVG_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_AVG_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_AVG_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_AVG_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("East (LUT)","East (COR)","South (LUT)","South (COR)","West (LUT)","West (COR)","North (LUT)","North (COR)","Total (LUT)","Total (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_east_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.6),
     main="Window/Wall Ratio SFH\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_SFH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_SFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_SFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_SFH_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_SFH_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("East (LUT)","East (COR)","South (LUT)","South (COR)","West (LUT)","West (COR)","North (LUT)","North (COR)","Total (LUT)","Total (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_east_SDH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.6),
     main="Window/Wall Ratio SDH\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_SDH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_SDH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_SDH_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_SDH_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("East (LUT)","East (COR)","South (LUT)","South (COR)","West (LUT)","West (COR)","North (LUT)","North (COR)","Total (LUT)","Total (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_east_MFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.6),
     main="Window/Wall Ratio MFH\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_MFH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_MFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_MFH_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_MFH_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("East (LUT)","East (COR)","South (LUT)","South (COR)","West (LUT)","West (COR)","North (LUT)","North (COR)","Total (LUT)","Total (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

plot(1850:2020,window_wall_ratio_east_LMFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,0.6),
     main="Window/Wall Ratio LMFH\ndepending on the Year of Construction",xlab="Year of Construction",ylab="Ratio",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,unlist(window_wall_ratio_east_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="green")
lines(1850:2020,window_wall_ratio_south_LMFH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,unlist(window_wall_ratio_south_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="blue")
lines(1850:2020,window_wall_ratio_west_LMFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,unlist(window_wall_ratio_west_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="purple")
lines(1850:2020,window_wall_ratio_north_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,unlist(window_wall_ratio_north_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,col="red")
lines(1850:2020,window_wall_ratio_LMFH_by_building_age_lookup(1850:2020),type="l",lwd=2,col="BLACK")
lines(1850:2020,unlist(window_wall_ratio_LMFH_by_building_age_correlation(1850:2020)),type="l",lty=2,lwd=2,col="BLACK")
legend("topright",legend=c("East (LUT)","East (COR)","South (LUT)","South (COR)","West (LUT)","West (COR)","North (LUT)","North (COR)","Total (LUT)","Total (COR)"),
       col=c("green","green","blue","blue","purple","purple","red","red","black","black"),lty=c(1,2,1,2,1,2,1,2,1,2),lwd=c(1,1,1,1,1,1,1,1,2,2))

