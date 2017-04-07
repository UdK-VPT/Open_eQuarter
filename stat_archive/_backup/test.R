setMethodS3("distribution_plot", "OeQ_Regr", function(this, x,y,                                                  
                                                     xrange=NULL,
                                                     palette=NULL,
                                                     log="",
                                                     pdffile=NULL,
                                                     ...) {
  get(".name", envir = KAL)
  print(parent.env())
  this$.parent
  print(this$.parent)
  
  op <- par()
  par(xpd=TRUE)
  if(!is.null(pdffile)) {
    pdf(pdffile,paper="a4", width = 0, height = 0)
    par(mfrow=c(2,1))
    par(mai=c(2.1, 0.5, 0.5, 0.5))#,omi = c(0.1,0.1, 0.1, 0.1)) #
    par(omi = c(0,0.5, 0.2, 0))
    par(cex=0.8)
    par(cex.main=1.1)
    
  }else{
    par(mar=c(15.1, 4.1, 4.1, 1.1))#,omi = c(0.1,0.1, 0.1, 0.1)) #
    par(oma = c(0,0.3, 0.2, 0))  
  }
  if(is.null(columns)) columns=colnames(this$.data)
  columns=columns[columns!=this$.keycolumn]
  if(length(columns)==1) columns=c(columns)
  l.perc_factor=1
  if(!is.null(this$.normcolumn)) {
    columns=columns[columns!=this$.normcolumn]
    l.perc_factor=100}
  if(is.null(xrange)) xrange=this$.xrange
  if(xrange[1]==-1) xrange[1]=min(this$.data[,this$.keycolumn])
  if(xrange[2]==-1) xrange[2]=max(this$.data[,this$.keycolumn])
  
  if(is.null(palette)) palette=this$.palette
  x=this$.data[,this$.keycolumn]
  #print(c(min(x),max(x)))
  x.mean=this$.proportionalized["mean",this$.keycolumn,]
  #print(c(min(x.mean),max(x.mean)))
  xpin=seq(xrange[1],xrange[2],length.out = 100)
  if(this$.type=="log") xp=log(xpin) else xp=xpin
  for (i in columns){
    y=this$.data[,i]*l.perc_factor
    if(!is.null(this$.normcolumn)) y=y/this$.data[,this$.normcolumn] 
    #  print(palette)
    y.0=this$.proportionalized["0%",i,]
    y.25=this$.proportionalized["25%",i,]
    y.50=this$.proportionalized["50%",i,]
    y.75=this$.proportionalized["75%",i,]
    y.100=this$.proportionalized["100%",i,]
    par(xpd=TRUE)
    if(this$.type=="log") l.titlesuffix=paste("f( ln(",unlist(VERBOSE[this$.keycolumn,]$label),"))",sep="") else l.titlesuffix=paste("f(",unlist(VERBOSE[this$.keycolumn,]$label),")",sep="")
    if(!is.null(this$.normcolumn)) l.titleprefix="Percentage of " else l.titleprefix=""
    plot(x,y,lwd=0,
         main=paste(unlist(VERBOSE["CORR_PLOT_TITLE",]$title),"\n",l.titleprefix,unlist(VERBOSE[i,]$label)," = ",l.titlesuffix," ",this$.regressions$.bestfit,sep=""),
         xlab=paste(unlist(VERBOSE[this$.keycolumn,]$label),unlist(VERBOSE[this$.keycolumn,]$unit)),
         ylab=paste(unlist(VERBOSE[i,]$label),unlist(VERBOSE[i,]$unit)),xlim=xrange,log=log)#ylim=c(0,100),
    rect(par("usr")[1],par("usr")[3],par("usr")[2],par("usr")[4],col = palette$bg)
    smoothScatter(x,y, colramp = palette$ramp,log=log, add=T,nbin=128) 
    y.mean=this$.proportionalized["mean",i,]
    par(xpd=FALSE)
    points(x.mean,y.mean*l.perc_factor,pch=3,lty=palette$curv$mean.lty,lwd=palette$curv$mean.lwd,col=palette$curv$mean.col)
    lines(xy_smooth(x.mean,y.25,range=NULL,zoom=l.perc_factor,type=this$.type),type="l",lty=palette$curv$q25.lty,lwd=palette$curv$q25.lwd,col=palette$curv$q25.col)
    lines(xy_smooth(x.mean,y.75,range=NULL,zoom=l.perc_factor,type=this$.type),type="l",lty=palette$curv$q75.lty,lwd=palette$curv$q75.lwd,col=palette$curv$q75.col)
    lines(xy_smooth(x.mean,y.50,range=NULL,zoom=l.perc_factor,type=this$.type),type="l",lty=palette$curv$q50.lty,lwd=palette$curv$q50.lwd,col=palette$curv$q50.col)
    l.bestfitfun=this$.regressions[[this$.bestfit]]$.predict
    lines(xpin,l.bestfitfun(xpin,asdf=FALSE)*l.perc_factor)
    #  
    #   lines(xpin,this$predict_spline(xpin,i)$y*l.perc_factor)
    #   lines(xpin,this$predict_splinelog(xpin,i)$y*l.perc_factor)
    #   lines(xpin,this$predict_lm1(xpin,i)$y*l.perc_factor,col="RED",lwd=2)
    #   lines(xpin,this$predict_lm1_splined(xpin,i)$y*l.perc_factor,col="RED",lty=2,lwd=2)
    #  lines(xpin,this$predict_lm2(xpin,i)$y*l.perc_factor,col="BLUE",lwd=2)
    #   lines(xpin,this$predict_lm3(xpin,i)$y*l.perc_factor,col="DARK GREEN",lwd=2)
    #   lines(xpin,this$predict_lm2_splined(xpin,i)$y*l.perc_factor,col="BLUE",lty=2,lwd=2)
    #   lines(xpin,this$predict_lm3_splined(xpin,i)$y*l.perc_factor,col="DARK GREEN",lty=2,lwd=2)
    #   lines(xpin,this$predict_lm1log(xpin,i)$y*l.perc_factor,col="RED",lty=3,lwd=2)
    #   lines(xpin,this$predict_lm2log(xpin,i)$y*l.perc_factor,col="BLUE",lty=3,lwd=2)
    #  lines(xpin,this$predict_lm3log(xpin,i)$y*l.perc_factor,col="DARK GREEN",lty=3,lwd=4)
    #  lines(xpin,this$predict_lm1log_splined(xpin,i)$y*l.perc_factor,col="RED",lty=4,lwd=2)
    #  lines(xpin,this$predict_lm2log_splined(xpin,i)$y*l.perc_factor,col="BLUE",lty=4,lwd=2)
    #  lines(xpin,this$predict_lm3log_splined(xpin,i)$y*l.perc_factor,col="DARK GREEN",lty=4,lwd=2)
    #print(this$.nls1[[i]])
    #pred=predict(this$.nls1[[i]],xp)
    #x1=pred$x
    #y1=pred$y
    #plot(x1,y1)
    #lines(this$.spline[[i]]$)
    #lines(xpin,this$.nls1[[i]](xp)*l.perc_factor,type="l",lty=palette$curv$regr1.lty,lwd=palette$curv$regr1.lwd,col="BLACK")#palette$curv$regr1.col)
    # lines(xpin,predict(this$.nls1[[i]],newdata=data.frame(x=xp))*l.perc_factor,type="l",lty=palette$curv$regr1.lty,lwd=palette$curv$regr1.lwd,col=palette$curv$regr1.col)
    #  lines(xpin,predict(this$.nls2[[i]],newdata=data.frame(x=xp))*l.perc_factor,type="l",lty=palette$curv$regr2.lty,lwd=palette$curv$regr2.lwd,col=palette$curv$regr2.col)
    #lines(xpin,predict(this$.lm1[[i]],newdata=data.frame(x=xp))*l.perc_factor,type="l",lty=palette$curv$regr3.lty,lwd=palette$curv$regr3.lwd,col="BLUE")#palette$curv$regr3.col)
    
    #lines(xpin,predict(this$.lm2[[i]],newdata=data.frame(x=xp))*l.perc_factor,type="l",lty=palette$curv$regr4.lty,lwd=palette$curv$regr4.lwd,col=palette$curv$regr4.col)
    
    if(!is.null(pdffile)) {
      l.lpos="bottomright" 
      l.linset=c(0.0,-0.6)
    }else{ 
      l.lpos="bottomright" 
      l.linset=c(0,-0.50)
    }
    
    if(this$.type=="log"){
      legend(l.lpos,  bty="n",  
             c("Local averages",
               "25% Quantile",
               "50% Quantile",
               "75% Quantile",
               as.expression(bquote("y("~x~") = a + "~bx~" +"~cx^2~" +"~dx^3~" ")),
               paste("x = ln( ",unlist(VERBOSE[this$.keycolumn,]$label)," )",sep=""),
               paste("y = ",unlist(VERBOSE[i,]$label),sep=""),
               paste("a = ",formatC(coef(this$.lm2[[i]])[1],digits=10)," ;  b = ",formatC(coef(this$.lm2[[i]])[2],digits=10),sep=""),
               paste("c = ",formatC(coef(this$.lm2[[i]])[3],digits=10)," ;  d = ",formatC(coef(this$.lm2[[i]])[4],digits=10),sep="")),
             #"\n x\'(x) = log(x); y(x) = C + ax +bx^2 +cx^3"), 
             xpd = NA,ncol=2,
             inset=l.linset,
             col=c(palette$curv$mean.col,
                   palette$curv$q25.col,
                   palette$curv$q50.col,
                   palette$curv$q75.col,
                   palette$curv$regr4.col,0,0,0,0,0,0),
             lty = c(palette$curv$mean.lty,
                     palette$curv$q25.lty,
                     palette$curv$q50.lty,
                     palette$curv$q75.lty,
                     palette$curv$regr4.lty,0,0,0,0,0,0),
             lwd = c(palette$curv$mean.lwd,
                     palette$curv$q25.lwd,
                     palette$curv$q50.lwd,
                     palette$curv$q75.lwd,
                     palette$curv$regr4.lwd,0,0,0,0,0,0), 
             pch = c(3, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA),
             merge = TRUE, bg = "white",
             box.lwd=0,
             text.col=palette$curv$textcol) 
    }else{
      legend(l.lpos,bty="n",  
             c("Local averages",
               "25% Quantile",
               "50% Quantile",
               "75% Quantile",
               as.expression(bquote("y("~x~") = a + "~bx~" +"~cx^2~" +"~dx^3~" ")),
               paste("x = ",unlist(VERBOSE[this$.keycolumn,]$label),sep=""),
               paste("y = ",unlist(VERBOSE[i,]$label),sep=""),
               paste("a = ",formatC(coef(this$.lm2[[i]])[1],digits=10)," ;  b = ",formatC(coef(this$.lm2[[i]])[2],digits=10),sep=""),
               paste("c = ",formatC(coef(this$.lm2[[i]])[3],digits=10)," ;  d = ",formatC(coef(this$.lm2[[i]])[4],digits=10),sep="")),
             #"\n x\'(x) = log(x); y(x) = C + ax +bx^2 +cx^3"), 
             xpd = NA,ncol=2,
             inset=l.linset,
             col=c(palette$curv$mean.col,
                   palette$curv$q25.col,
                   palette$curv$q50.col,
                   palette$curv$q75.col,
                   palette$curv$regr4.col,0,0,0,0,0,0),
             lty = c(palette$curv$mean.lty,
                     palette$curv$q25.lty,
                     palette$curv$q50.lty,
                     palette$curv$q75.lty,
                     palette$curv$regr4.lty,0,0,0,0,0,0),
             lwd = c(palette$curv$mean.lwd,
                     palette$curv$q25.lwd,
                     palette$curv$q50.lwd,
                     palette$curv$q75.lwd,
                     palette$curv$regr4.lwd,0,0,0,0,0,0), 
             pch = c(3, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA),
             merge = TRUE, bg = "white",
             box.lwd=0,
             text.col=palette$curv$textcol) 
      
    }
    Sys.sleep(1)
  }
  suppressWarnings(par(op))
  if(!is.null(pdffile)) {dev.off()
                         browseURL(pdffile)}
})

