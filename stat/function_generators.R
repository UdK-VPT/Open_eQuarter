### corellation analysis
build_type_distribution_by_population_density<-function(
  name="distribution_by_population_density",
  description="Buildings with n flats in correlation to population density"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("POP_DENS",BUILDINGS_BY_NOFLATS)],normcolumn="BLD_NOFLAT_TOTAL",limits=BUILDINGS_BY_NOFLATS_LIMITS)
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
  l.investigation$py_Function(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
}

### corellation analysis
build_type_distribution_by_year_of_construction<-function(
  name="distribution_by_year_of_construction",
  description="Buildings with n flats in correlation to year of construction"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("BLD_AGE1_AVG",BUILDINGS_BY_NOFLATS)],normcolumn="BLD_NOFLAT_TOTAL",p_mode="log")
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
}

### corellation analysis
build_age_distribution_by_average_year_of_construction<-function(
  name="age_distribution_by_average_year_of_construction",
  description="Age distribution in correlation to average year of construction"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("BLD_AGE1_AVG",BUILDINGS_BY_AGE1)],normcolumn="BLD_AGE1_TOTAL",limits=BUILDINGS_BY_AGE1_LIMITS)
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

build_typical_window_uvalue_by_year_of_construction<-function(
  name="window_uvalue_by_year_of_construction",
  description="Typical Window U-Value in correlation to year of construction"){
  # WINDOW_UVALUE=data.frame(YEAR=c(1800,1920,1950,1977,1995,2010,2050,2100),UVAL_WIN=c(5,4.8,4,3,2,1.3,0.7,0.5)/5,stringsAsFactors=FALSE)
  WINDOW_UVALUE=data.frame(YEAR=c(1800:1950,1977,1980,1995,2010,2050:2100),UVAL_WIN=c(rep(5,151),4,2.5,2,1.5,rep(0.5,51)),stringsAsFactors=FALSE)
  l.investigation=new_OeQ_Inv(WINDOW_UVALUE,n_breaks=100)
  #return(l.investigation$.regressions)
  TYP_UVAL_DB_WINDOW=data.frame(YEAR=c(1800:2500),UVAL_WIN=l.investigation$.regressions$UVAL_WIN$.smoothsplinelog$.predict(c(1800:2500))$y,stringsAsFactors = TRUE) 
  TYP_UVAL_DB_WINDOW[,2]=round(TYP_UVAL_DB_WINDOW[,2],2)
  TYP_UVAL_DB_WINDOW=TYP_UVAL_DB_WINDOW[TYP_UVAL_DB_WINDOW[, 1] < 2041, ]
  TYP_UVAL_DB_WINDOW=TYP_UVAL_DB_WINDOW[TYP_UVAL_DB_WINDOW[, 1] > 1849, ]
  TYP_UVAL_DB_WINDOW[TYP_UVAL_DB_WINDOW[,2]>5,2]=5.0
  if(!file.exists("database/oeq_typical_uvalues_window_by_yoc.RData")) save(TYP_UVAL_DB_WINDOW,file="database/oeq_typical_uvalues_window_by_yoc.RData")
  plot(TYP_UVAL_DB_WINDOW)
  WINDOW_UVALUE=cbind(WINDOW_UVALUE,l.investigation$.regressions$UVAL_WIN$.smoothsplinelog$.predict(WINDOW_UVALUE$YEAR)$y)
  l.investigation=new_OeQ_Inv(WINDOW_UVALUE,n_breaks=100)
  l.investigation$distribution_plot(pdffile=name)
  # l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$R_Function_correlation(fun_name=name,filename=name,description=description,lookuptable=TYP_UVAL_DB_WINDOW)
  l.investigation$py_Function(fun_name=name,filename=name,description=description,lookuptable=TYP_UVAL_DB_WINDOW)
  return(TYP_UVAL_DB_WINDOW)
}

build_typical_wall_uvalue_by_year_of_construction<-function(
  name="typical_wall_uvalue_by_year_of_construction",
  description="Typical Wall U-Value in correlation to year of construction"){
  WALL_UVALUE=as.lookup(c(1800:1900,1940,1953,1963,1973,1980,1989,2000,2020:2100),c(rep(2.45,101),1.5,1.5,0.9,0.7,0.7,0.4,0.2,rep(0.15,81)),)
  l.investigation=new_OeQ_Inv(WALL_UVALUE,n_breaks=100)
  TYP_UVAL_DB_WALL=data.frame(YEAR=c(1800:2100),UVAL=l.investigation$.regressions$UVAL$.smoothsplinelog$.predict(c(1800:2100))$y,stringsAsFactors = TRUE) 
  TYP_UVAL_DB_WALL[,2]=round(TYP_UVAL_DB_WALL[,2],2)
  TYP_UVAL_DB_WALL=TYP_UVAL_DB_WALL[TYP_UVAL_DB_WALL[, 1] < 2041, ]
  TYP_UVAL_DB_WALL=TYP_UVAL_DB_WALL[TYP_UVAL_DB_WALL[, 1] > 1849, ]
  TYP_UVAL_DB_WALL[TYP_UVAL_DB_WALL[,2]>max(WALL_UVALUE$UVAL),2]=max(WALL_UVALUE$UVAL)
  TYP_UVAL_DB_WALL[TYP_UVAL_DB_WALL[,2]<min(WALL_UVALUE$UVAL),2]=min(WALL_UVALUE$UVAL)
  if(!file.exists("database/oeq_typical_uvalues_wall_by_yoc.RData")) save(TYP_UVAL_DB_WALL,file="database/oeq_typical_uvalues_wall_by_yoc.RData")
  plot(WALL_UVALUE,type="l")
  lines(TYP_UVAL_DB_WALL,col="RED")
  WALL_UVALUE=cbind(WALL_UVALUE,l.investigation$.regressions$UVAL$.smoothsplinelog$.predict(WALL_UVALUE$YEAR)$y)
  l.investigation=new_OeQ_Inv(WALL_UVALUE,n_breaks=100)
  l.investigation$distribution_plot(pdffile=name)
  # l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.func_text=l.investigation$generate_lookup_function_in_R(fun_name=name,filename=name,description=description,lookuptable=TYP_UVAL_DB_WALL)
  str_eval(l.func_text)
  l.investigation$generate_lookup_function_in_python(fun_name=name,filename=name,description=description,lookuptable=TYP_UVAL_DB_WALL)
  return(l.func_text)
}

