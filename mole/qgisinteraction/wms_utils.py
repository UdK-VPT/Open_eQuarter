
import os, time
from osgeo import gdal,osr
from urllib.request import urlopen
from urllib.parse import urlencode

import os

class wmsHandler(object):
    def __init__(self,url,styles="0",layers="0",map_resolution=72,dpi=72,
                 img_format="image/png",format_options="dpi:72",transparent="TRUE",srs="EPSG:25833",
                 crs="EPSG:25833",bbox=[385267.905618,5819602.01872,386734.721215,5819963.28486]
                 ,request="GetMap",height=454,width=1665,version="1.3.0"):

    
        self.url = url
        self.styles = styles
        self.layers = layers
        self.map_resolution = map_resolution
        self.dpi = dpi
        self.img_format = img_format
        self.format_options = format_options
        self.transparent = transparent
        self.srs = srs
        self.crs = crs
        self.bbox = bbox
        self.request = request
        self.height = height
        self.width = width
        self.version = version


    def url_string(self):
    
        url_param = {'SERVICE' : 'WMS',
                     'REQUEST':'GetMap',
                     'VERSION': self.version,
                     'STYLES':self.styles,
                     'LAYERS' : self.layers,
                     'MAP_RESOLUTION':self.map_resolution,
                     'DPI' : self.dpi,
                     'FORMAT':self.img_format,
                     'FORMAT_OPTIONS': self.format_options,
                     'TRANSPARENT': self.transparent,
                     'WIDTH' : self.width,
                     'HEIGHT' : self.height,
                     }


        return(self.url + '?' + urlencode(url_param)+'&SRS=' + 
                self.srs + "&CRS="+self.crs + "&BBOX=" + ','.join([str(i) for i in self.bbox]))
                
                
    def asPNG(self,filename,timeout=300,debug=False):

        with urlopen(self.url_string(), timeout=timeout) as wmscon:
            if debug:
                print(wmscon.geturl())
                print(wmscon.info())
                print(wmscon.getcode())
            with open(filename, 'wb') as outf:
                 outf.write(wmscon.read())

        return(filename)        
                
    def asGeoTif(self,filename):
        print(self.url_string())
        tmpfilename = os.path.join(os.path.dirname(filename),"tmp.png")
        src_ds = gdal.Open( self.asPNG(tmpfilename))
        #print(self.bbox)
        xmin, ymin, xmax, ymax = self.bbox
        xres = (xmax - xmin) / float(self.width)
        yres = (ymax - ymin) / float(self.height)
        geotransform = (xmin, xres, 0, ymax, 0, -yres)
        #print(xmin, xres, 0, ymax, 0, -yres)
        driver = gdal.GetDriverByName( "GTiff" )

        #Output to new format
        dst_ds = driver.CreateCopy( filename, src_ds, 0 )


        dst_ds.SetGeoTransform(geotransform)  

        srs = osr.SpatialReference()            # establish encoding
        srs.ImportFromEPSG(int(self.srs.split(':')[-1]))                # WGS84 lat/long
        dst_ds.SetProjection(srs.ExportToWkt())

        dst_ds.FlushCache()          


        #Properly close the datasets to flush to disk
        dst_ds = None
        try:
            os.remove(tmpfilename)
        except:
            pass
        return(filename)



def getWmsLegendUrl(layer): #Very quick and very dirty
    url = None
    try:
        url="http" +layer.metadata().split('LegendURLs')[1].split("image/")[1].split("http")[1].split("<")[0]
    except: pass
    return url

