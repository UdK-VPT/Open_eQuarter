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
library(KernSmooth) # Support for Smooth distribution plots in R 

# output palette definitions
#source('config/plotpalettes.R')

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