#plot definitions
PAL_SCREEN <- list(ramp=colorRampPalette(c("black","#400F0F","red","orange","yellow","white"), space = "Lab",bias = 1.2),
                   bgcol="black",textcol="lightgrey",curv=c(mean=list(col="green",lwd=2,lty=0),
                                                            q25=list(col="lightblue",lwd=2,lty=2),
                                                            q50=list(col="skyblue",lwd=2,lty=1),
                                                            q75=list(col="skyblue",lwd=2,lty=4),
                                                            regr1=list(col="orange",lwd=1,lty=1),
                                                            regr2=list(col="orange",lwd=2,lty=1),
                                                            regr3=list(col="red",lwd=2,lty=1),
                                                            regr4=list(col="red",lwd=3,lty=1),
                                                            reglin=list(col="red",lwd=1,lty=2)))
PAL_PRINT <- list(ramp=colorRampPalette(c("white","#F0F0F0","#111111"),interpolate = "linear",space = "Lab",bias = 3.5),
                  bgcol="white",textcol="black",curv=c(mean=list(col="green",lwd=2,lty=0),
                                                       q25=list(col="orange",lwd=1,lty=2),
                                                       q50=list(col="orange",lwd=1,lty=1),
                                                       q75=list(col="orange",lwd=1,lty=4),
                                                       regr1=list(col="skyblue",lwd=1,lty=1),
                                                       regr2=list(col="skyblue",lwd=2,lty=1),
                                                       regr3=list(col="skyblue",lwd=2,lty=1),
                                                       regr4=list(col="red",lwd=2,lty=1),
                                                       reglin=list(col="red",lwd=1,lty=2)))
#PAL_PRINT <- list(ramp=colorRampPalette(c("blue","white","yellow"),nbin=64, space = "rgb"),bgcol="white",meancol="black",curvcol="red")
