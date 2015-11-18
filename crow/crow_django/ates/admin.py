from django.contrib.gis import admin
from models import Buildings, Materials, Quarters, SurfacesRaw, Usageprofiles, Vectors

admin.site.register(Buildings)
admin.site.register(Materials)
admin.site.register(Quarters)
admin.site.register(SurfacesRaw)
admin.site.register(Usageprofiles)
admin.site.register(Vectors)
