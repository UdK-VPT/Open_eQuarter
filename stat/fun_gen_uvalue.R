#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Lookup Function Generators U-Values
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         21.05.2015
#
# Descrription: 
# generators for correlation and lookuptables functions in R and in Python.
# uvalues of buildings
#######################################################################################

#adding verbose for window definitions. VERBOSE is initialized in init.R
# Window Area by Age from 'data_sources/150512-IWU-Aufbereitung/SQ_..._WIND-OUT.csv'"'
UVALUES_BY_AGE=c("YEAR","U_BASE","U_WALL","U_ROOF","U_AVG_OPAQ","U_WINDOW","U_ROOF_PRJ1","U_ROOF_PRJ2") #
UVALUES_CONT_ALL_BY_AGE=c("YEAR","U_BASE_CONT","U_WALL_CONT","U_ROOF_CONT","U_OPAQUE_CONT","U_WINDOW_CONT","U_FLAT_ROOF_CONT","U_TOP_CEIL_CONT","U_BASE_CEIL_CONT","U_AVG_BUILD_CONT")
VERBOSE= as.data.frame(rbind(VERBOSE,
                             YEAR=list(label="Year of Construction",
                                       unit="",
                                       info="Year of Construction",
                                       title="Year of Construction",
                                       description="Year of Construction"
                             ),
                             U_BASE=list(label="U-Value Base at present",
                                                unit="W/(m2·K)",
                                                info="U-Value Base Slab at present",
                                                title="U-Value Base Slab at present",
                                                description="U-Value of Base Slabs at present"
                             ),
                             U_WALL=list(label="U-Value Wall at present",
                                                unit="W/(m2·K)",
                                                info="U-Value Wall at present",
                                                title="U-Value Wall at present",
                                                description="U-Value of Walls at present"
                             ),
                             U_ROOF=list(label="U-Value Roof",
                                                unit="W/(m2·K)",
                                                info="U-Value Roof",
                                                title="U-Value Roof",
                                                description="U-Value of Roof Constructions"
                             ),
                             U_AVG_OPAQ=list(label="Avg U-Value Opaque Comp",
                                                unit="W/(m2·K)",
                                                info="Avg U-Value Opaque Comp",
                                                title="Avg U-Value Opaque Comp",
                                                description="Average U-Value of Opaque Components"
                             ),
                             U_WINDOW=list(label="U-Value Window at present",
                                           unit="W/(m2·K)",
                                           info="U-Value Window at present",
                                           title="U-Value Window at present",
                                           description="U-Value of Windows at present"
                             ),
                             U_ROOF_PRJ1=list(label="U-Value Roof Proj V1 at present",
                                           unit="W/(m2·K)",
                                           info="U-Value Roof Proj V1",
                                           title="U-Value Roof Proj V1",
                                           description="U-Value of Roofs as Projection V1 at present"
                             ),
                             U_ROOF_PRJ2=list(label="U-Value Roof Proj V2 at present",
                                              unit="W/(m2·K)",
                                              info="U-Value Roof Proj V2 at present",
                                              title="U-Value Roof Proj V2 at present",
                                              description="U-Value of Roofs as Projection V2 at present"
                             ),
                             #CONTEMPORARY
                             U_BASE_CONT=list(label="Contemporary U-Value Base",
                                                          unit="W/(m2·K)",
                                                          info="Contemporary U-Value Base Slab",
                                                          title="Contemporary U-Value Base Slab",
                                                          description="Contemporary U-Value of Base Slabs"
                                              ),
                             U_WALL_CONT=list(label="Contemporary U-Value Wall",
                                              unit="W/(m2·K)",
                                              info="Contemporary U-Value Wall",
                                              title="Contemporary U-Value Wall",
                                              description="U-Value of Walls"
                             ),
                             U_ROOF_CONT=list(label="Contemporary U-Value Roof",
                                                          unit="W/(m2·K)",
                                                          info="Contemporary U-Value Roof",
                                                          title= "Contemporary U-Value Roof",
                                                          description="Contemporary U-Value of Roof Constructions"
                             ),
                             U_AVG_OPAQUE_CONT=list(label="Contemporary Avg U-Value Opaque Comp",
                                                    unit="W/(m2·K)",
                                                    info="Contemporary Avg U-Value Opaque Comp",
                                                    title="Contemporary Avg U-Value Opaque Comp",
                                                    description="Contemporary Average U-Value of Opaque Components"
                             ),
                             U_WINDOW_CONT=list(label="Contemporary U-Value Window",
                                                unit="W/(m2·K)",
                                                info="Contemporary U-Value Window",
                                                title="Contemporary U-Value Window",
                                                description= "Contemporary U-Value of Windows"
                             ),
                             U_FLAT_ROOF_CONT=list(label="Contemporary U-Value Flat Roof",
                                                   unit="W/(m2·K)",
                                                   info="Contemporary U-Value Flat Roof",
                                                   title="Contemporary U-ValueFlat Roof",
                                                   description="Contemporary U-Value of Flat Roofs"
                             ),
                             U_TOP_CEIL_CONT=list(label="Contemporary U-Value Top Ceiling",
                                                  unit="W/(m2·K)",
                                                  info="Contemporary U-Value Top Ceiling",
                                                  title="Contemporary U-Value Top Ceiling",
                                                  description="Contemporary U-Value of Top Ceilings"
                             ),
                             U_BASE_CEIL_CONT=list(label="Contemporary U-Value Base Ceiling",
                                                   unit="W/(m2·K)",
                                                   info="Contemporary U-Value Base Ceiling",
                                                   title="Contemporary U-Value Base Ceiling",
                                                   description="Contemporary U-Value of  Base Ceilings"
                             ),
                             U_AVG_BUILD_CONT=list(label="Contemporary U-Value 1mx1mx1m-Cube AVG",
                                                   unit="W/(m2·K)",
                                                   info="Contemporary U-Value 1mx1mx1m-Cube AVG",
                                                   title="Contemporary U-Value 1mx1mx1m-Cube AVG",
                                                   description="Average U-Value of a 1mx1mx1m-Cube Samble-Building"
                             )
),stringsAsFactors=FALSE)

######## BUILDING AVERAGE ###############
#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_base_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_base_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Base Slabs in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_wall_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_wall_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Walls in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roof_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roof_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Roof Constructions in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_opaque_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_opaque_uvalue_AVG_by_building_age_lookup",
               description="Average U-Values of Opaque Components in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_window_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_window_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Windows in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj1_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj1_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 1) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
               lookup_column=7,
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj2_uvalue_AVG_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj2_uvalue_AVG_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 2) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_AVG-OUT.csv",
               lookup_column=8,
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

######## SINGLE FAMILY HOUSES ###############
#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_base_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_base_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Base Slabs in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_wall_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_wall_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Walls in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roof_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roof_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Roof Constructions in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_opaque_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_opaque_uvalue_SFH_by_building_age_lookup",
               description="Average U-Values of Opaque Components in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_window_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_window_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Windows in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj1_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj1_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 1) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
               lookup_column=7,
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj2_uvalue_SFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj2_uvalue_SFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 2) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_SFH-OUT.csv",
               lookup_column=8,
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
#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_base_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_base_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Base Slabs in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_wall_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_wall_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Walls in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roof_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roof_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Roof Constructions in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_opaque_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_opaque_uvalue_SDH_by_building_age_lookup",
               description="Average U-Values of Opaque Components in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_window_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_window_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Windows in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj1_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj1_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 1) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
               lookup_column=7,
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj2_uvalue_SDH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj2_uvalue_SDH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 2) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_TH-OUT.csv",
               lookup_column=8,
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

######## MULTIFAMILY HOUSES ###############
#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_base_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_base_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Base Slabs in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_wall_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_wall_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Walls in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roof_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roof_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Roof Constructions in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_opaque_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_opaque_uvalue_MFH_by_building_age_lookup",
               description="Average U-Values of Opaque Components in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_window_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_window_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Windows in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj1_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj1_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 1) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
               lookup_column=7,
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj2_uvalue_MFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj2_uvalue_MFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 2) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_MFH-OUT.csv",
               lookup_column=8,
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

######## BUILDING AVERAGE ###############
#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_base_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_base_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Base Slabs in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_wall_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_wall_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Walls in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roof_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roof_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Roof Constructions in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_opaque_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_opaque_uvalue_LMFH_by_building_age_lookup",
               description="Average U-Values of Opaque Components in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_window_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_window_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Windows in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj1_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj1_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 1) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
               lookup_column=7,
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

#Typical Uvalues depending on the Year of Construction (Lookuptable)
build_present_roofprj2_uvalue_LMFH_by_building_age_lookup<-function( resolution=74){
  build_lookup(name="present_roofprj2_uvalue_LMFH_by_building_age_lookup",
               description="U-Values of Roofs as Projection (method 2) in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150512-IWU-Aufbereitung/SQ_LMFH-OUT.csv",
               lookup_column=8,
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


### Contemporary U-Values ###

#Contemporary  Base U-Values
build_contemporary_base_uvalue_by_building_age_lookup<-function(resolution=34){
  build_lookup(name="contemporary_base_uvalue_by_building_age_lookup",
               description="Contemporary Base U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
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

#Contemporary  Wall U-Values
build_contemporary_wall_uvalue_by_building_age_lookup<-function(resolution=44){
  build_lookup(name="contemporary_wall_uvalue_by_building_age_lookup",
               description="Contemporary Wall U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
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

#Contemporary  Roof U-Values
build_contemporary_roof_uvalue_by_building_age_lookup<-function(resolution=37){
  build_lookup(name="contemporary_roof_uvalue_by_building_age_lookup",
               description="Contemporary Roof U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
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


#Contemporary  U-Values of opaque Components
build_contemporary_opaque_uvalue_by_building_age_lookup<-function(resolution=37){
  build_lookup(name="contemporary_opaque_uvalue_by_building_age_lookup",
               description="Contemporary U-Value of Opaque Components of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
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

#Contemporary  Window U-Values
build_contemporary_window_uvalue_by_building_age_lookup<-function(resolution=41){
  build_lookup(name="contemporary_window_uvalue_by_building_age_lookup",
               description="Contemporary Window U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
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

#Contemporary  Flat Roof U-Values
build_contemporary_flat_roof_uvalue_by_building_age_lookup<-function(resolution=36){
  build_lookup(name="contemporary_flat_roof_uvalue_by_building_age_lookup",
               description="Contemporary Flat Roof U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
               lookup_column=7,
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

#Contemporary  Top Ceiling U-Values
build_contemporary_top_ceiling_uvalue_by_building_age_lookup<-function(resolution=45){
  build_lookup(name="contemporary_top_ceiling_uvalue_by_building_age_lookup",
               description="Contemporary Top Ceiling U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
               lookup_column=8,
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

#Contemporary Base Ceiling U-Values
build_contemporary_base_ceiling_uvalue_by_building_age_lookup<-function(resolution=39){
  build_lookup(name="contemporary_base_ceiling_uvalue_by_building_age_lookup",
               description="Contemporary Base Ceiling U-Value of Buildings in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
               lookup_column=9,
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

#Contemporary  Base U-Values
build_contemporary_buiding_cube_uvalue_by_building_age_lookup<-function(resolution=29){
  build_lookup(name="contemporary_buiding_cube_uvalue_by_building_age_lookup",
               description="Contemporary Average U-Value of a 1mx1mx1m-Cube in correlation to year of construction, based on the source data of the survey for the \"German Building Typology\ developed by the \"Institut für Wohnen und Umwelt\", Darmstadt/Germany, 2011-2013",
               csvsource="data_sources/150522_IWU_UValues\ Contemp/CONTEMP_UVAL_ALL-OUT.csv",
               lookup_column=10,
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
  build_present_base_uvalue_AVG_by_building_age_lookup()
  build_present_wall_uvalue_AVG_by_building_age_lookup()
  build_present_roof_uvalue_AVG_by_building_age_lookup()
  build_present_opaque_uvalue_AVG_by_building_age_lookup()
  build_present_window_uvalue_AVG_by_building_age_lookup()
  build_present_roofprj1_uvalue_AVG_by_building_age_lookup()
  build_present_roofprj2_uvalue_AVG_by_building_age_lookup()
  
  build_present_base_uvalue_SFH_by_building_age_lookup()
  build_present_wall_uvalue_SFH_by_building_age_lookup()
  build_present_roof_uvalue_SFH_by_building_age_lookup()
  build_present_opaque_uvalue_SFH_by_building_age_lookup()
  build_present_window_uvalue_SFH_by_building_age_lookup()
  build_present_roofprj1_uvalue_SFH_by_building_age_lookup()
  build_present_roofprj2_uvalue_SFH_by_building_age_lookup()
  
  build_present_base_uvalue_SDH_by_building_age_lookup()
  build_present_wall_uvalue_SDH_by_building_age_lookup()
  build_present_roof_uvalue_SDH_by_building_age_lookup()
  build_present_opaque_uvalue_SDH_by_building_age_lookup()
  build_present_window_uvalue_SDH_by_building_age_lookup()
  build_present_roofprj1_uvalue_SDH_by_building_age_lookup()
  build_present_roofprj2_uvalue_SDH_by_building_age_lookup()
  
  build_present_base_uvalue_MFH_by_building_age_lookup()
  build_present_wall_uvalue_MFH_by_building_age_lookup()
  build_present_roof_uvalue_MFH_by_building_age_lookup()
  build_present_opaque_uvalue_MFH_by_building_age_lookup()
  build_present_window_uvalue_MFH_by_building_age_lookup()
  build_present_roofprj1_uvalue_MFH_by_building_age_lookup()
  build_present_roofprj2_uvalue_MFH_by_building_age_lookup()
  
  build_present_base_uvalue_LMFH_by_building_age_lookup()
  build_present_wall_uvalue_LMFH_by_building_age_lookup()
  build_present_roof_uvalue_LMFH_by_building_age_lookup()
  build_present_opaque_uvalue_LMFH_by_building_age_lookup()
  build_present_window_uvalue_LMFH_by_building_age_lookup()
  build_present_roofprj1_uvalue_LMFH_by_building_age_lookup()
  build_present_roofprj2_uvalue_LMFH_by_building_age_lookup()
  
  build_contemporary_base_uvalue_by_building_age_lookup()
  build_contemporary_wall_uvalue_by_building_age_lookup()
  build_contemporary_roof_uvalue_by_building_age_lookup()
  build_contemporary_opaque_uvalue_by_building_age_lookup()
  build_contemporary_window_uvalue_by_building_age_lookup()
  build_contemporary_window_uvalue_by_building_age_lookup()
  build_contemporary_flat_roof_uvalue_by_building_age_lookup()
  build_contemporary_top_ceiling_uvalue_by_building_age_lookup()
  build_contemporary_base_ceiling_uvalue_by_building_age_lookup()
  build_contemporary_buiding_cube_uvalue_by_building_age_lookup()
  
}
plot(1850:2020,present_base_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Base Slab\ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_base_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_base_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_base_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_base_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_wall_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Wall\ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_wall_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_wall_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_wall_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_wall_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_roof_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Roof Construction\ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_roof_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_roof_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_roof_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_roof_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_opaque_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Average U-Values Opaque Components\ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_opaque_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_opaque_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_opaque_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_opaque_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_window_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Window\ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_window_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_window_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_window_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_window_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_roofprj1_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Roof as Projection (Method 1) \ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_roofprj1_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_roofprj1_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_roofprj1_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_roofprj1_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,present_roofprj2_uvalue_SFH_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,4.5),
     main="Typical U-Values Roof as Projection (Method 2) \ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,present_roofprj2_uvalue_SDH_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,present_roofprj2_uvalue_MFH_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,present_roofprj2_uvalue_LMFH_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,present_roofprj2_uvalue_AVG_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("SFH","SDH","MFH","LMFH","AVG"),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))

plot(1850:2020,contemporary_base_uvalue_by_building_age_lookup(1850:2020),type="l",col="green",ylim=c(0,6),
     main="Contemporary U-Values Roof of Building Components \ndepending on the Year of Construction",xlab="Year of Construction",ylab="U-Value",frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,)
lines(1850:2020,contemporary_wall_uvalue_by_building_age_lookup(1850:2020),type="l",col="blue")
lines(1850:2020,contemporary_roof_uvalue_by_building_age_lookup(1850:2020),type="l",col="purple")
lines(1850:2020,contemporary_window_uvalue_by_building_age_lookup(1850:2020),type="l",col="red")
lines(1850:2020,contemporary_opaque_uvalue_by_building_age_lookup(1850:2020),type="l",col="BLACK",lty=2,lwd=2)
legend("topright",legend=c("Base Slab","Wall","Roof","Window","AVG Opaque Comp."),
       col=c("green","blue","purple","red","black"),lty=c(1,1,1,1,2),lwd=c(1,1,1,1,2))


