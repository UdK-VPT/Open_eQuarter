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

#Typical Owner Distribution depending on the Population Density (Correlation)
build_building_owner_distribution_by_population_density_correlation<-function(
  name="building_owner_distribution_by_population_density_correlation",
  description="Building Owner Distribution in Correlation to the population density"){
    l.investigation=new_OeQ_Inv(BLD_DB[,c('POP_DENS',BUILDINGS_BY_OWNER)],keycolumn='POP_DENS',normcolumn='BLD_OWNER_TOTAL' ,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Owner Distribution depending on the Population Density (Correlation)
build_flat_owner_distribution_by_population_density_correlation<-function(
  name="flat_owner_distribution_by_population_density_correlation",
  description="Flat Owner Distribution in Correlation to the population density"){
    l.investigation=new_OeQ_Inv(BLD_DB[,c('POP_DENS',FLATS_BY_OWNER)],keycolumn='POP_DENS',normcolumn='FLT_OWNER_TOTAL' ,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Owner Distribution depending on the Population Density (Correlation)
build_building_heating_type_distribution_by_population_density_correlation<-function(
  name="building_heating_type_distribution_by_population_density_correlation",
  description="Building Heating Type Distribution in Correlation to the population density"){
    l.investigation=new_OeQ_Inv(BLD_DB[,c('POP_DENS',BUILDINGS_BY_HEATSYS)],keycolumn='POP_DENS',normcolumn='BLD_HEAT_TOTAL' ,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }

#Typical Owner Distribution depending on the Population Density (Correlation)
build_flat_heating_type_distribution_by_population_density_correlation<-function(
  name="flat_heating_type_distribution_by_population_density_correlation",
  description="Flat Heating Type Distribution in Correlation to the population density"){
    l.investigation=new_OeQ_Inv(BLD_DB[,c('POP_DENS',FLATS_BY_HEATSYS)],keycolumn='POP_DENS',normcolumn='FLT_HEAT_TOTAL' ,n_breaks=200)
    l.investigation$distribution_plot(pdffile=name)
    #l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    str_eval(l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description))
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }


FORCERUN=T
if(FORCERUN==TRUE){
 # build_building_owner_distribution_by_population_density_correlation()
  #build_flat_owner_distribution_by_population_density_correlation()
  build_building_heating_type_distribution_by_population_density_correlation()
  build_flat_heating_type_distribution_by_population_density_correlation()
}

