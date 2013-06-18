# -*- coding: utf-8 -*-

# Django settings for municipales project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))



ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'elecciones.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ihmajd2(+u^ltvsccfl50iu0qqma^7rhu1iha&amp;*1kq$8hheq54'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'votainteligente.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'votainteligente.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django_mobile.context_processors.flavour',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'south',
    'popit',
    'writeit',
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django_extensions',
    'django_mobile',
    'elecciones',
    'captcha',
    'mailer',
    'markdown_deux',
    'django_contactme'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
#reCaptcha settings:
RECAPTCHA_PUBLIC_KEY = '<your public key>'
RECAPTCHA_PRIVATE_KEY = '<your private key>'

# Email setting
EMAIL_HOST = 'smtp.yoursmtpserver.com'
EMAIL_HOST_USER = 'your_username'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#disqus/comment short name:
DISQUS_SHORT_NAME = '<your disqus short name>'

#candidate info contact mail
DEFAULT_FROM_EMAIL = 'default@votainteligente.org'
INFO_CONTACT_MAIL = '<your e-mail address where you want to receive candidate inquiries'
CANDIDATE_CONTACT_SUBJECT = '<Subject you want for candidates inquiries>'

#contactme settings: notification mail address(es)
CONTACTME_NOTIFY_TO = ''

EXTRA_APPS = ()
PREGUNTALE_STATUS = 'GOING_ON'  # Cambia comportamiento del modulo Preguntales. Estados: GOING_ON (por defecto), COMING_SOON, PASSED

#CACHE_MINUTES for cache
CACHE_MINUTES = 15

#TRACKERIDS it can be several 
GOOGLE_ANALYTICS_TRACKER_ID = ['THETRACKERID']


NO_ANSWER_DEFAULT_MESSAGE = u"No pasa naipe aún loco"

#Writeit settings
WRITEIT_USERNAME = 'replace_with_real_username'
WRITEIT_KEY = 'replace_with_real_key'
DEFAULT_WRITEIT_SUBJECT = 'The subject'
#setting to avoid db changes during test
SOUTH_TESTS_MIGRATE = False

#The length of the ranking
RANKING_LENGTH = 15

try:
    from local_settings import *
    INSTALLED_APPS += EXTRA_APPS
except ImportError:
    pass
