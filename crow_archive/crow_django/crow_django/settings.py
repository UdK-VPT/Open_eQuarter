"""
Django settings for geo_django project
"""
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = BASE_DIR


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is nescessary for maintaining session information
SECRET_KEY = 'lcw5&qk37g!f0j^-_r1999&)ijb4dg6(d&l4--!%ufvtj++^-b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Needed, when distributing the application in an production environment (using wsgi)
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'crow_django.wsgi.application'


# Application definition - For further app-configurations see below
INSTALLED_APPS = (
    'django.contrib.admin',         # basic django admin functionalities
    'django.contrib.auth',          # core authentication system
    'django.contrib.sites',         # site mgmt
    'django.contrib.contenttypes',  # allows to associate permissions with models
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   # django staticfiles-finder
    'django.contrib.gis',           # geo-django extension
    'django_jasmine',               # used for running jasmine-tests against the js-sources
    'crow',                         # OeQ-extension
    'ates',                         # Models for ATES-BuildingDB
    'django_extensions',            # Enhanced commandline-tools for generating database-visualisations
    'registration',                 # Django Redux for user registration
    'bootstrap3',                   # Enables easier usage of bootstrap tags in django templates
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',             # Handle sessions across requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',          # Associate users with requests during sessions
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',   # Logs out user after password change
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'crow_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'crow_django',
        'USER': 'djangocrow',
        'PASSWORD': 'djangocrow'
    },
    'atesdb': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'buildingDB',
        'USER': 'ATESuser',
        'PASSWORD': 'ATESuser',
    }
}
DATABASE_ROUTERS = ['ates.routers.AtesRouter']

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'crow')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

"""
Configure installed apps
"""
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)

# Configuration for django-registration
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_EMAIL_HTML = True

# Email-backend is needed, to send account-activation emails
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'app-messages')

# Tells django-jasmine app where to find the javascript unit tests
JASMINE_TEST_DIRECTORY = os.path.join(BASE_DIR, 'crow', 'jasmine')

# Site id is needed, to maintain session-information
SITE_ID = 1
"""
./ Configure installed apps
"""
