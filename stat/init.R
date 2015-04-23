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

# python like dictionary
lookuptable<-function(...){ # Constructor for a single regression model 1
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


as.data.frame.lookuptable<-function(object,...) data.frame(KEY=names(object),VALUE=as.vector(object),stringsAsFactors=FALSE)
as.matrix.lookuptable<-function(object,...) cbind(KEY=names(object),VALUE=as.vector(object))
keys<-function(object,...) UseMethod("keys",object)
keys.default<- function(object,...) keys(object,...)
keys.lookuptable<-function(object,...) names(object)
print.lookuptable<-function(object,...) print(as.data.frame(object))
values<-function(object,...) UseMethod("values",object)
values.default<-function(object,...) warning("No generic definition for 'values'")
values.lookuptable<-function(object,...) as.vector(object)
lookup<-function(object,...) UseMethod("lookup",object)
lookup.default<-function(object,...) warning("No generic definition for 'lookup'")
lookup.lookuptable<-function(object,...)  values(object)[keys(object)%in% c(...)]
reverse_lookup<-function(object,...) UseMethod("reverse_lookup",object)
reverse_lookup.default<-function(object,...) warning("No generic definition for 'reverse_lookup'")
reverse_lookup.lookuptable<-function(object,...)  keys(object)[values(object)%in% c(...)]