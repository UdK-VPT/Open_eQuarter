#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Function Generators Windows
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         18.05.2015
#
# Descrription: 
# generators for correlation and lookuptable functions 
# for window features in R and in Python.
#
#######################################################################################


WIN_WALL_RATIO_BY_AGE=c("YEAR","A_WIN_E_BY_AW","A_WIN_S_BY_AW","A_WIN_W_BY_AW","A_WIN_N_BY_AW","A_WIN_BY_AW") #dwelling or other types
#adding verbose. VERBOSE is initialized in mun.db.R
VERBOSE= as.data.frame(rbind(VERBOSE,
                             KEY=list(label="Key",
                                                      unit="",
                                                      info="Key",
                                                      title="Key",
                                                      description="Key"
                                                      ),
                             VALUE=list(label="Value",
                                      unit="",
                                      info="Value",
                                      title="Value",
                                      description="Value"
                             ),
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


#Typical Present Roof U-Value of Large Multifamily Houses
build_window_wall_ratio_AVG_by_building_age_as_lookup<-function(){
 print( build_lookup(name="window_wall_ratio_east_by_building_age",
               description="Window/Wall Ratio (Eastern Facade) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv",
               lookup_column=2,
               dir_DB=DB_PATH,
               dir_CSV=CSV_PATH,
               dir_PDF=PDF_PATH,
               dir_R=CORR_R_EXPORT_PATH,
               dir_py=CORR_PY_EXPORT_PATH,
               smoothen=FALSE,
               resolution=80,
               prediction_range=c(1800,2100),
               lookup_range=c(1849,2021)))
  build_lookup(name="window_wall_ratio_south_by_building_age",
               description="Window/Wall Ratio (Southern Facade) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
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
  build_lookup(name="window_wall_ratio_west_by_building_age",
               description="Window/Wall Ratio (Western Facade) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
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
  build_lookup(name="window_wall_ratio_north_by_building_age",
               description="Window/Wall Ratio (Northern Facade) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
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
  build_lookup(name="window_wall_ratio_by_building_age",
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



### corellation analysis
build_window_wall_ratio_AVG_by_building_age<-function(
  name="window_wall_ratio_AVG_by_building_age",
  description="Window/Wall Ratio in Correlation to Year of Construction"){
    csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG_WIND-OUT.csv"
    l.db=read.csv2(csvsource)
    l.investigation=new_OeQ_Inv(l.db,n_breaks=1000)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
  }

### corellation analysis
build_window_wall_ratio_SFH_by_building_age<-function(
  name="window_wall_ratio_SFH_by_building_age",
  description="Window/Wall Ratio at Single Family Houses in Correlation to the Building Age"){
  csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH_WIND-OUT.csv"
  l.db=read.csv2(csvsource)
  l.investigation=new_OeQ_Inv(l.db,n_breaks=1000)
  l.investigation$distribution_plot(pdffile=name)
  #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS))
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

### corellation analysis
build_window_wall_ratio_SDH_by_building_age<-function(
  name="window_wall_ratio_SDH_by_building_age",
  description="Window/Wall Ratio at Semi Detached Houses in Correlation to the Building Age"){
  csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SDH_WIND-OUT.csv"
  l.db=read.csv2(csvsource)
  l.investigation=new_OeQ_Inv(l.db,n_breaks=1000)
  l.investigation$distribution_plot(pdffile=name)
  #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS))
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

### corellation analysis
build_window_wall_ratio_MFH_by_building_age<-function(
  name="window_wall_ratio_MFH_by_building_age",
  description="Window/Wall Ratio at Multi Family Houses in Correlation to the Building Age"){
  csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH_WIND-OUT.csv"
  l.db=read.csv2(csvsource)
  l.investigation=new_OeQ_Inv(l.db,n_breaks=150)
  l.investigation$distribution_plot(pdffile=name)
  #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS))
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

### corellation analysis
build_window_wall_ratio_LMFH_by_building_age<-function(
  name="window_wall_ratio_LMFH_by_building_age",
  description="Window/Wall Ratio at Large Multi Family Houses in Correlation to the Building Age"){
  csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH_WIND-OUT.csv"
  l.db=read.csv2(csvsource)
  l.investigation=new_OeQ_Inv(l.db,n_breaks=150)
  l.investigation$distribution_plot(pdffile=name)
  #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS))
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

