#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Correlation and Lookup Function Generators
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         18.05.2015
#
# Descrription: 
# generators for correlation and lookuptables functions in R and in Python.
#
#######################################################################################

### corellation analysis and code generat
build_type_distribution_by_population_density<-function(
  name="distribution_by_population_density",
  description="Buildings with n flats in correlation to population density"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("POP_DENS",BUILDINGS_BY_NOFLATS)],normcolumn="BLD_NOFLAT_TOTAL",limits=BUILDINGS_BY_NOFLATS_LIMITS,n_breaks=300)
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
}

### corellation analysis
build_type_distribution_by_building_density<-function(
  name="distribution_by_building_density",
  description="Buildings with n flats in correlation to building density"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("BLD_DENS",BUILDINGS_BY_NOFLATS)],normcolumn="BLD_NOFLAT_TOTAL",limits=BUILDINGS_BY_NOFLATS_LIMITS)
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
  l.investigation$py_Function(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
}

### corellation analysis
build_type_distribution_by_building_age<-function(
  name="distribution_by_building_age",
  description="Buildings with n flats in Correlation to Building Age"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("BLD_DENS",BUILDINGS_BY_AGE1)],normcolumn="BLD_AGE1_TOTAL")
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
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_NOFLATS_WEIGHTS)
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

### corellation analysis
build_building_density_by_average_year_of_construction<-function(
  name="building density_by_average_year_of_construction",
  description="Building Density in correlation to average year of construction"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("BLD_AGE1_AVG","BLD_DENS")])
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

### corellation analysis
build_building_density_by_population_density<-function(
  name="building_density_by_population_density",
  description="Building Density in Correlation to the Population Density"){
  l.investigation=new_OeQ_Inv(BLD_DB[,c("POP_DENS","BLD_DENS")])
  l.investigation$distribution_plot(pdffile=name)
  l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
  l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
  l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description,weights=BUILDINGS_BY_AGE1_WEIGHTS)
}

### corellation analysis
build_flat_area_by_population_density<-function(
  name="flat_area_by_population_density",
  description="Flat Area in Correlation to the Population Density"){
    l.investigation=new_OeQ_Inv(BLD_DB[,c("POP_DENS","FLT_AREA_AVG")])
    l.investigation$distribution_plot(pdffile=name)
    l.investigation$sum_plot(pdffile=paste(name,"_sum",sep=""))
    l.investigation$generate_correlation_function_in_R(fun_name=name,filename=name,description=description)
    l.investigation$generate_correlation_function_in_python(fun_name=name,filename=name,description=description)
  }




########## Code-/Look-Up-Table Generators  ###########

# Basic Lookup Generator. very straight forward. 
# get the source data
# apply the standard OeQ regression analisys
# use the spline output (smooth if requested)
# generate output lookuptable from prediction
# write the files ####
build_lookup<-function( 
  name="new_lookuptable", #Name of the lookup table, used for all files generated
  description="New autogenerated Lookuptable", #Description for autogenerated functions
  csvsource=NULL, #Source for the lookuptable, KEY is always the first column, VALUE is taken from 'lookup_column'
  lookup_table=NULL, #Only used if there is given no 'csvsource' 
  lookup_column=2, #Column VALUE is taken from
  smoothen=FALSE, #Use smoothed spline prediction for output lookuptable generation
  resolution=20, # resolution of the regression analysis
  p_mode="lin", #prediction mode, controls how the input data distribution is handled ("auto", "log" or "lin")
  prediction_range=NULL, # key range of the prediction, sometimes useful to get smoother behaviour at start and end of the lookuptable
  lookup_range=NULL, # key range of the arising lookuptanble
  write_DB=TRUE, #write the output as RData Database
  dir_DB=getwd(), #directory where the RData Database shall be written to
  write_PDF=TRUE, #write the OeQ regression PDFs
  dir_PDF=getwd(), #directory where the regression PDF shall be written to
  write_CSV=TRUE, #write the output as CSV
  dir_CSV=getwd(),#directory where the CSV lookuptable shall be written to
  write_R=TRUE, #autogenerate a lookupfunction for R
  dir_R=getwd(), #directory where the autogenerated R lookup function shall be written to
  write_py=TRUE, #autogenerate a lookupfunction for Python
  dir_py=getwd(), #directory where the Python lookup function shall be written to
  keyname="KEY", #name of the keycolumn in the lookup table
  valuename="VALUE",
  main=paste("'",name,"'",sep="")){ #name of the valuecolumn in the lookup table
  
  if (!is.null(csvsource)){ #check wether a csv file was given 
    lookup_table=read.csv2(csvsource,skip = 0)[,c(1,lookup_column)] #read it
  }
  if(is.null(lookup_table)){ #stop if there is no lookuptable available
    stop("No Lookup Source !")
  }
   print(!is.null(unlist(VERBOSE[names(lookup_table)[1],"label"])))
    
   if (!is.null(unlist(VERBOSE[names(lookup_table)[1],"label"]))) keyname=names(lookup_table)[1]
  if (!is.null(unlist(VERBOSE[names(lookup_table)[2],"label"]))) valuename=names(lookup_table)[2]
  if(keyname!="KEY" & valuename!="VALUE") main=paste(VERBOSE[valuename,"label"]," = f( ",VERBOSE[keyname,"label"]," )",sep="")
  #stop()
  #convert lookup_table to class "lookuptable" if necessary
  if (class(lookup_table)!="lookuptable") lookup_table=lookuptable(lookup_table[,1],lookup_table[,2])
  
  #set prediction_range to the range of 'lookup_table' if not given
  if(is.null(prediction_range)) {
    prediction_range=c(min(keys(lookup_table)),max(keys(lookup_table)))
  }else{
    lookup_table=prepend(lookup_table,prediction_range[1],values(lookup_table)[1])
    lookup_table=append(lookup_table,prediction_range[2],values(lookup_table)[length(values(lookup_table))])
  }
  #set lookup_range to the range of 'lookup_table' if not given
  if(is.null(lookup_range)) lookup_range=prediction_range
  
  #switch warnings off
  suppressWarnings({
  # Apply the standard OeQ regression analysis (normally used to find correlations)
  l.investigation=new_OeQ_Inv(as.data.frame(lookup_table),n_breaks=resolution,p_mode=p_mode)
  #switch warnings back to 'warnstatsafe
  })
  
  # Get lookuptable from spline
   if(smoothen) {
    l.lookup_table=lookuptable(c(prediction_range[1]:prediction_range[2]),
                               l.investigation$.regressions$VALUE$.smoothsplinelog$.predict(c(prediction_range[1]:prediction_range[2]),asdf=FALSE)) 
  }else{
    l.lookup_table=lookuptable(c(prediction_range[1]:prediction_range[2]),
                               l.investigation$.regressions$VALUE$.splinelog$.predict(c(prediction_range[1]:prediction_range[2]),asdf=FALSE)) 
  }
 #round values to 2 digits 
  l.lookup_table=round(l.lookup_table,3)
  #set keyrange 
  l.lookup_table=setkeyrange(l.lookup_table,lookup_range[1],lookup_range[2])
  #fix values outside the input data range
  l.lookup_table=limitvalues(l.lookup_table,min(values(lookup_table)),max(values(lookup_table)))
  
   #Plot I/O Comparisonchart
  plot(as.data.frame(l.lookup_table),type="l",col="RED",lwd=3,xlim=lookup_range,xpd=FALSE,
       lab=c(10,10,10),frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,
       main=paste("I/O Comparison Chart for Look-Up-Table Generation R=",resolution,"\n",
                  main,sep=""),
       xlab=paste(VERBOSE[keyname,"label"]," ",VERBOSE[keyname,"unit"]),
       ylab=paste(VERBOSE[valuename,"label"],VERBOSE[valuename,"unit"]))
  lines(as.data.frame(lookup_table),xlim=lookup_range,type="b",pch=3,col="GREY30",lty=3,lwd=2,xpd=FALSE)
  box() 
  legend('topright',c("Input Data","Output Look-Up-Table"),col=c('GREY30','RED'), cex=.95,
         lty=c(3,1),lwd=c(2,3),pch=c(3,NA),bty="o",box.lwd=1,bg="white")
  
 
  #write I/O Comparisonchart to pdf
  if(write_PDF) {
   # op <- par()
   pdf(paste(dir_PDF,"/",name,".pdf",sep=""),width=10,height=7,pointsize=17)
    plot(as.data.frame(l.lookup_table),type="l",col="RED",lwd=2,xlim=lookup_range,xpd=FALSE,
         lab=c(10,10,10),frame.plot=TRUE,tck = 1,fg="GREY80",bty="o",las=1,
         main=paste("I/O Comparison Chart for Look-Up-Table Generation R=",resolution,"\n'",main,"'",sep=""))
    lines(as.data.frame(lookup_table),xlim=lookup_range,type="b",pch=3,col="GREY30",lty=3,lwd=1,xpd=FALSE)
    box() 
    legend('topright',c("Input Data","Output Look-Up-Table"),col=c('GREY30','RED'), cex=.95,
           lty=c(3,1),lwd=c(1,2),pch=c(3,NA),bty="o",box.lwd=1,bg="white")
    dev.off()
  #  suppressWarnings(par(op))
  }
  print(paste(dir_DB,"/",name,".RData",sep=""))
  
  #write RData database
  if(write_DB) save(l.lookup_table,file=paste(dir_DB,"/",name,".RData",sep=""))
  
  #write CSV database
  if(write_CSV){
    write.csv2(as.data.frame(l.lookup_table),file=paste(dir_CSV,"/",name,".csv",sep=""),row.names = FALSE)
  }
  
  #write R lookup function
  if(write_R){
    l.func_text=l.investigation$generate_lookup_function_in_R(fun_name=name,filename=paste(dir_R,"/",name,".R",sep=""),description=description,lookuptable=as.matrix(l.lookup_table))
  }else{
    l.func_text=l.investigation$generate_lookup_function_in_R(fun_name=name,description=description,lookuptable=as.matrix(l.lookup_table))
  }

  #translate R lookup function 
  str_eval(l.func_text)

  #write Python lookup function
  if(write_py){
    l.investigation$generate_lookup_function_in_python(fun_name=name,filename=paste(dir_py,"/",name,".py",sep=""),description=description,lookuptable=l.lookup_table)
  }
  invisible(l.lookup_table)
}

####### Code Generators ############


# generate generate_correlation_code_snippet_in_R snippet for a model
setMethodS3("generate_correlation_code_snippet_in_R", "OeQ_Model", function(this,par_name,description=NULL,...){
  if(is.null(description)) description=par_name
  l.coeff=this$.model$coefficients
  l.coeffnames=c("Const","a","b","c","d")
  l.coeff[is.na(l.coeff)]=0
  l.code=paste("# OeQ autogenerated correlation for '",description,"'\n",
               par_name," = correlation(\n    ",paste(l.coeffnames,"=",this$.model$coefficients,collapse=",\n    "),",\n    mode=\"",this$.mode,"\")\n",sep="")
  #  "Const= ",formatC(l.coeff[1],digits=12),"\n",
  #  "a=     ",formatC(l.coeff[2],digits=12),"\n",
  #  "b=     ",formatC(l.coeff[3],digits=12),"\n",sep="")
  # if(!is.na(l.coeff[4])){l.code=paste(l.code,"c=     ",formatC(l.coeff[4],digits=12),"\n",sep="")}
  # if(!is.na(l.coeff[5])){l.code=paste(l.code,"d=     ",formatC(l.coeff[5],digits=12),"\n",sep="")}
  # l.code=paste(l.code,sub("y",par_name,this$.verb_formula),"\n",sep="")
  return(l.code)
})

# generate python code snippet for a model
setMethodS3("generate_correlation_code_snippet_in_python", "OeQ_Model", function(this,par_name,description=NULL,...){
  if(is.null(description)) description=par_name
  l.coeff=this$.model$coefficients
  l.coeff[is.na(l.coeff)]=0
  l.code=paste("    # OeQ autogenerated correlation for '",description,
               "'\n    ",par_name,"= oeq.correlation(",
               "\n    const= ",formatC(l.coeff[1],digits=12),",",
               "\n    a=     ",formatC(l.coeff[2],digits=12),",",
               "\n    b=     ",formatC(l.coeff[3],digits=12),",",sep="")
  if(!is.na(l.coeff[4])){l.code=paste(l.code,"\n    c=     ",formatC(l.coeff[4],digits=12),",",sep="")}
  if(!is.na(l.coeff[5])){l.code=paste(l.code,"\n    d=     ",formatC(l.coeff[5],digits=12),",",sep="")}
  l.code=paste(l.code,"\n    mode= \"",this$.mode,"\")\n",sep="")
  return(l.code)
})


# generate_lookup_function_in_R for a table lookup
setMethodS3("generate_lookup_function_in_R", "OeQ_Inv", function(this,fun_name,description,filename=NULL,lookuptable=NULL,...){
  #save the lookup table as csv
  if(class(lookuptable)=="lookuptable") lookuptable=as.data.frame(lookuptable)
  # write.csv(lookuptable,file=paste(CSV_PATH,"/",filename,".csv",sep=","),row.names = FALSE)
  #combine function text
  l.code=paste("# OeQ autogenerated lookup function: ",description,"\n",
               fun_name,"<-function(xin){\n",sep="")
  l.code=paste(l.code,"\nl.lookup = lookuptable(",paste("\nc(",lookuptable[,1],",",lookuptable[,2],")",collapse=",",sep=""),")",sep="")
  l.code=paste(l.code,"\nreturn(lookup(l.lookup,xin))\n}\n",sep="")
  print(filename)
  if (!is.null(filename)) writeLines(l.code,filename)
  return(l.code)
})

# generate_lookup_function_in_R for a table lookup
setMethodS3("generate_lookup_function_in_python", "OeQ_Inv", function(this,fun_name,description,filename=NULL,lookuptable=NULL,...){
  #save the lookup table as csv
  if(class(lookuptable)=="lookuptable") lookuptable=as.data.frame(lookuptable)
  #  write.csv(lookuptable,file=paste(CSV_PATH,"/",filename,".csv",sep=","),row.names = FALSE)
  #combine function text
  l.code=paste("# coding: utf8\n",
               "# OeQ autogenerated lookup function for '",description,"'\n\n",
               "import math\n",
               "import numpy as np\n",
               "import oeqLookuptable as oeq\n",
               "def get(*xin):\n\n",sep="")
  
  l.code=paste(l.code,"\n    l_lookup = oeq.lookuptable(\n[",paste("\n",lookuptable[,1],",",lookuptable[,2],collapse=",",sep=""),"])",sep="")
  l.code=paste(l.code,"\n    return(l_lookup.lookup(xin))",sep="")
  if (!is.null(filename)) writeLines(l.code,filename)
  return(l.code)
})


# generate_correlation_function_in_R for this Investigation
setMethodS3("generate_correlation_function_in_R", "OeQ_Inv", function(this,fun_name,description=NULL,filename=fun_name,lookuptable=NULL,...){
  if(is.null(description)) description=fun_name
  l.code=paste("# OeQ autogenerated correlation function: ",description,"\n\n",#source('init.R')\n",
               fun_name,"<-function(...){\n",sep="")
  l.columns=c()
  for (i in this$.regressions) {
     l.code=paste(l.code, i$generate_bestfit_correlation_code_snippet_in_R(),"\n",sep="") 
    l.columns=c(l.columns,i$.columnname)
  } 
  l.code=paste(l.code,"\n    return(data.frame(",l.columns[1],"=lookup(",l.columns[1],",...)",sep="")
  for (i in l.columns[-1])  l.code=paste(l.code,",\n    ",i,"=lookup(",i,",...)",sep="")
  l.code=paste(l.code,",\n    stringsAsFactors=FALSE))\n}",sep="")
  if (!is.null(filename)) writeLines(l.code,paste(CORR_R_EXPORT_PATH,"/",filename,".R",sep=""))
  #cat(l.code)
  #readline()
  str_eval(l.code)
  return(l.code)
 })

# PYCODE MUSS ANGEPASST WERDEN
# generate generate_correlation_function_in_python snippet for the bestfit model of this regression
setMethodS3("generate_correlation_function_in_python", "OeQ_Inv", function(this,fun_name,description=NULL,filename=fun_name,lookuptable=NULL,...){
  if (is.null(weights)) weights=rep(1,length(this$.regressions))
  if (is.null(description)) description=fun_name
  l.code=paste("# OeQ autogenerated correlation for '",description,"'\n\n",
               "import math\n",
               "import numpy as np\n",
               "import oeqCorrelation as oeq\n",
               "def get(*xin):\n\n",sep="")
  l.columns=c()
  for (i in this$.regressions) {
    l.code=paste(l.code, i$generate_bestfit_correlation_code_snippet_in_python(),sep="") 
    l.columns=c(l.columns,i$.columnname)
  } 
  l.code=paste(l.code,"\n    return dict(",l.columns[1],"=",l.columns[1],".lookup(*xin)",sep="")
  for (i in l.columns[-1])  l.code=paste(l.code,",\n    ",i,"=",i,".lookup(*xin)",sep="")
  l.code=paste(l.code,")\n",sep="")
    if (!is.null(filename)) writeLines(l.code,paste(CORR_PY_EXPORT_PATH,"/",filename,".py",sep=""))
  return(l.code)
})





############## Base ###############





#build_typical_base_uvalue_by_year_of_construction()
#build_typical_wall_uvalue_by_year_of_construction()
#build_typical_window_uvalue_by_year_of_construction()
#build_typical_roof_uvalue_by_year_of_construction()
#build_typical_flatroof_uvalue_by_year_of_construction()
