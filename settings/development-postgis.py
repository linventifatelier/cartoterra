from cartoterra.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cartoterra",
        "USER": "gueux",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

# TODO remove! Temp fix, see:
# https://code.djangoproject.com/ticket/21607#ticket
# POSTGIS_VERSION = (2, 1, 0)


#HAYSTACK_SEARCH_ENGINE = 'simple'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

DEBUG = True

SERVE_MEDIA = DEBUG
EMAIL_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

## debug_toolbar
#INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = INSTALLED_APPS + [
    "django_extensions",
    #"debug_toolbar",
]

#MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + \
#    ["debug_toolbar.middleware.DebugToolbarMiddleware"]
#
#DEBUG_TOOLBAR_CONFIG = {
#    "INTERCEPT_REDIRECTS": False,
#}
