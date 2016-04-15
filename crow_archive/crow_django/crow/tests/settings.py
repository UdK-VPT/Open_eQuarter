from crow_django.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'crow_django',
        'USER': 'djangocrow',
        'PASSWORD': 'djangocrow'
    },
}
