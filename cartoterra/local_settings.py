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

#HAYSTACK_XAPIAN_PATH = '/home/www-cartoterra/search_index/xapian'

#DEBUG = False
DEBUG = True

#MEDIA_ROOT = '/home/www-cartoterra/media/media'
#STATIC_ROOT = '/home/www-cartoterra/media/static'

SERVE_MEDIA = DEBUG
TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

