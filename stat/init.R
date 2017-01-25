#######################################################################################
#
# Project:      Open eQuarter 
#
# Part:         STAT: Datamining Toolbox / Initialization / Helpers
#
# Status:       Active
#
# Author:       Werner Kaul
#
# Date:         21.10.2014
#
# Descrription: 
# loading basic libraries & defining helpers.
#
#######################################################################################

# basic includes
library(ASdialogs)  # Basic System dialogs for Mac
library(R.oo)       # Support for object oriented programming in R 
library(inlinedocs) # Inlinedocumentation Tool
library(KernSmooth) # Support for Smooth distribution plots in R 

# output palette definitions
source('config/plotpalettes.R')

# pathdefinition export
CORR_PY_EXPORT_PATH="../mole/stat_corr"
CORR_R_EXPORT_PATH="stat_corr"
PDF_PATH="pdfout"
CSV_PATH="csvout"
DB_PATH="database"
#basic Verbose
VERBOSE= as.data.frame(rbind(DISTR_PLOT_TITLE=list(label="",unit="",info="Distribution review",title="Distribution Check",description=""),
                             DISTR_PLOT_XLAB=list(label="Value Ranges [(n,m)]",unit="(n,m)",info="Value Ranges",title="",description=""),
                             DISTR_PLOT_YLAB=list(label="Number of Samples [n]",unit="[n]",info="Number of Samples",title="",description=""),
                             DISTR_PLOT_COMMENT=list(label="",unit="",info="Population Density",title="",description=""),
                             CORR_PLOT_TITLE=list(label="",unit="",info="",title="Correlation Chart",description=""),
                             CORR_PLOT_XLAB=list(label="Amount of",unit="",info="Amount of",title="",description=""),
                             CORR_PLOT_YLAB=list(label="Number of Samples",unit="[n]",info="",title="",description=""),
                             CORR_SUM_PLOT_TITLE=list(label="",unit="",info="",title="Correlation Sum Check",description=""),
                             CORR_SUM_PLOT_XLAB=list(label="Amount of",unit="",info="Amount of",title="Buildings",description=""),
                             CORR_SUM_PLOT_YLAB=list(label="Number of Samples",unit="[n]",info="",title="",description="")
                             ),stringsAsFactors=FALSE)
                             

# helpers 
str_eval<-function(x) {return(eval(parse(text=x),envir=.GlobalEnv))}
trim.leading <- function (x)  sub("^\\s+", "", x)
trim.trailing <- function (x)  sub("\\s+$", "", x)
remove.spaces <- function (x) gsub("\\s+", "", x)

force.numeric<-function(x)   suppressWarnings(as.numeric(remove.spaces(sub(",", ".",x, fixed = TRUE))))
abs.force.numeric <-function (x)  abs(force.numeric(x))
#set2zero.na <- function (src,control) {src[(is.na(src))&(!is.na(control))]=0 
#                                        return(src)}

set2zero.na <- function (df,verbose=TRUE) {
  if(verbose) print("Setting NA's to 0...")
  for (i in 1:nrow(df)){
    if(is.na(df[i,1])) next
    if(df[i,1]!=sum(df[i,-1],na.rm = TRUE)) next
    df[i,is.na(df[i,])]=0
  }
  if(verbose) print("Done!")
  return(df) 
}

VERBOSE_LEVEL=2

verbose<-function(message,level=VERBOSE_LEVEL){
  if(level<VERBOSE_LEVEL) print(message)
}


########### LOOKUPTABLE ##############

#adding verbose for lookuptables. VERBOSE is initialized in init.R
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
                             )),stringsAsFactors=FALSE)

                       
# S3 constructor definition for class lookuptable
lookuptable<-function(...){ 
  args=list(...)
  if((length(args)==1)&&(length(args[1])>1)) args=args[1]
  if((length(args)==2)&&(length(args[1])==(length(args[2])))){
    out=unlist(args[2])
    names(out)<-unlist(args[1])
  }else{
    args=unlist(args)
    out=args[c(1:(length(args)%/%2))*2]
    names(out)<-args[c(1:(length(args)%/%2))*2-1]
  }
  class(out)<-"lookuptable"
  invisible(out)
}

# S3 method definitions for class lookuptable
keys<-function(object,...) UseMethod("keys",object)
keys.default<- function(object,...) keys(object,...)
keys.lookuptable<-function(object,...) names(object)

values<-function(object,...) UseMethod("values",object)
values.default<-function(object,...) warning("No generic definition for 'values'")
values.lookuptable<-function(object,...) as.vector(object)

print.lookuptable<-function(object,...) print(as.data.frame(object))

lookup<-function(object,...) UseMethod("lookup",object)
lookup.default<-function(object,...) warning("No generic definition for 'lookup'")
lookup.lookuptable<-function(object,...)   values(object)[sapply(c(...),FUN<-function(i){which(keys(object)==i)})]

reverse_lookup<-function(object,...) UseMethod("reverse_lookup",object)
reverse_lookup.default<-function(object,...) warning("No generic definition for 'reverse_lookup'")
reverse_lookup.lookuptable<-function(object,...)  keys(object)[sapply(c(...),FUN<-function(i){which(values(object)==i)})] 

save2csv<-function(object,...)  UseMethod("save2csv",object)
save2csv.default<- function(object,...) save2csv(object,...)
save2csv.lookuptable<-function(object,...)   write.csv(as.data.frame(object),row.names=FALSE,...)

# strip lookuppairs whose keys are out of range given as c(min,max)
setkeyrange<-function(object,...) UseMethod("setkeyrange",object)
setkeyrange.default<- function(object,...) setkeyrange(object,...)
setkeyrange.lookuptable<-function(object,...) {
  args=c(...)
  keys=as.numeric(keys(object))
  lookuptable(keys[(keys>=args[1])&(keys<=args[2])],values(object)[(keys>=args[1])&(keys<=args[2])])
}

# strip lookuppairs whose values are out of range given as c(min,max)
setvaluerange<-function(object,...) UseMethod("setvaluerange",object)
setvaluerange.default<- function(object,...) setvaluerange(object,...)
setvaluerange.lookuptable<-function(object,...) {
  args=c(...)
  values=as.numeric(values(object))
  lookuptable(keys(object)[(values>=args[1])&(values<=args[2])],values[(values>=args[1])&(values<=args[2])])
}

# limits values to range given as c(min,max)
limitvalues<-function(object,...) UseMethod("limitvalues",object)
limitvalues.default<- function(object,...) limitvalues(object,...)
limitvalues.lookuptable<-function(object,...) {
  args=c(...)
   values=as.numeric(values(object))
   if(args[1]!=-1) values[values<args[1]]=args[1]
   if(args[2]!=-2) values[values>args[2]]=args[2]
   lookuptable(keys(object),values)
}

# append one or more key/value pairs to the lookuptable (given as c(keys),c(values))
append<-function(object,...) UseMethod("append",object)
append.default<- function(object,...) append(object,...)
append.lookuptable<-function(object,keys,values,...) lookuptable(c(keys(object),keys),c(values(object),values),...)

# prepend one or more key/value pairs to the lookuptable (given as c(keys),c(values))
prepend<-function(object,...) UseMethod("prepend",object)
prepend.default<- function(object,...) prepend(object,...)
prepend.lookuptable<-function(object,keys,values,...) lookuptable(c(keys,keys(object)),c(values,values(object)),...)

# convert lookuptable to data.frame
as.data.frame.lookuptable<-function(object,...) data.frame(KEY=as.numeric(names(object)),VALUE=as.vector(object),stringsAsFactors=FALSE)
# convert lookuptable to matrix
as.matrix.lookuptable<-function(object,...) cbind(KEY=as.numeric(names(object)),VALUE=as.vector(object))

# round values of a lookuptable
round.lookuptable<-function(object,...) lookuptable(keys(object),round(values(object),...))



########### CORRELATION ##############
# S3 constructor for class correlation (only factors, no model)
correlation<-function(Const=0,a=0,b=0,c=0,d=0,mode="log",...){ 
  out=list(.Const=Const,.a=a,.b=b,.c=c,.d=d,.mode=mode)
  class(out)<-"correlation"
  invisible(out)
}

# S3 method definitions for class lookuptable
lookup.correlation<-function(object,...){
  x=c(...)
   if (object$.mode=="log") x=log(x)
  return(object$.Const + object$.a*x + object$.b*x^2 + object$.c*x^3 + object$.d*x^4)
}

# get range as lookuptable of class data.frame
as.data.frame.correlation<-function(object,start,end,stepwidth=1,...) {
  xin=seq(from = start, to = end, by =  stepwidth)
  data.frame(KEY=xin,VALUE=lookup(object,xin),stringsAsFactors=FALSE)
}

# get range as lookuptable of class matrix
as.matrix.correlation<-function(object,start,end,stepwidth=1,...) {
  xin=seq(from = start, to = end, by =  stepwidth)
  cbind(KEY=xin,VALUE=lookup(object,xin))
}

save2csv.correlation<-function(object,start,end,stepwidth=1,...)   write.csv(as.data.frame(object,start,end,stepwidth),row.names=FALSE,...)

verbose_equation<-function(object,...) UseMethod("verbose_equation",object)
verbose_equation.default<- function(object,...) equation(object,...)
verbose_equation.correlation<-function(object,symbolical=TRUE,...){
  if(symbolical) {
    out= paste(c(if (object$.Const==0) "" else paste("Const =",object$.Const),
                 if (object$.a==0) "" else     paste("a     =",object$.a),
                 if (object$.b==0) "" else     paste("b     =",object$.b),
                 if (object$.c==0) "" else     paste("c     =",object$.c),
                 if (object$.d==0) "" else     paste("d     =",object$.d)),collapse="\n")
    
    if(object$.mode=="log")   { 
      out= paste(out, "\n\nx' = log(x)\n\ny = ",paste(c( if (object$.Const==0) "" else "Const " ,
                                                         if (object$.a==0) "" else "a * x' " ,
                                                         if (object$.b==0) "" else "b * x'^2" ,
                                                         if (object$.c==0) "" else "c * x'^3",
                                                         if (object$.d==0) "" else "d * x'^4"),
                                                      collapse = "+ "),
                 sep="")
    }else{
      out= paste(out, "\n\ny = ",paste(c( if (object$.Const==0) "" else "Const " ,
                                          if (object$.a==0) "" else "a * x " ,
                                          if (object$.b==0) "" else "b * x^2" ,
                                          if (object$.c==0) "" else "c * x^3",
                                          if (object$.d==0) "" else "d * x^4"),
                                       collapse = "+ "),
                 sep="")
    }
  }else{
    if(object$.mode=="log")   { 
      out= paste( "\n\nx' = log(x)\n\ny = ",paste(c( if (object$.Const==0) "" else  paste(object$.Const,"\n  ") ,
                                                         if (object$.a==0) "" else paste(object$.a,"* x'\n  "),
                                                         if (object$.b==0) "" else paste(object$.b,"* x'^2\n  ") ,
                                                         if (object$.c==0) "" else paste(object$.c,"* x'^3\n  "),
                                                         if (object$.d==0) "" else paste(object$.d,"* x'^4\n  ")),
                                                      collapse = "+ "),
                 sep="")
    }else{
      out= paste( "\n\ny = ",paste(c( if (object$.Const==0) "" else  paste(object$.Const,"\n  ") ,
                                          if (object$.a==0) "" else paste(object$.a,"* x\n  "),
                                          if (object$.b==0) "" else paste(object$.b,"* x^2\n  ") ,
                                          if (object$.c==0) "" else paste(object$.c,"* x^3\n  "),
                                          if (object$.d==0) "" else paste(object$.d,"* x^4\n  ")),
                                       collapse = "+ "),
                 sep="")
    }
  }
  return(out)
}



winf=correlation(const= 120046.968215,
                 a=     -249.82114301,
                 b=     0.194718483741,
                 c=     -6.73636413768e-05,
                 d=     8.72705641799e-09,"log")