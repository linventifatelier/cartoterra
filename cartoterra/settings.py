import os
import posixpath
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as messages


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "geodjango",
        "USER": "gueux",
        "HOST": "",
        "PORT": "",
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Paris"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = "fr-FR"
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ('fr', _('French')),
]

SITE_ID = 1

# Name of the website
SITE_NAME = "CartoTerra.net"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

# Additional directories which hold static files
# STATICFILES_DIRS = [
#    os.path.join(PROJECT_ROOT, "static"),
# ]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # "django.contrib.staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# Make this unique, and don't share it with anybody.
# You can create a new key with:
# python -c 'import random; print "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])'
SECRET_KEY = "CHANGE_THIS_TO_SOMETHING_RANDOM_AND_SECRET"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
                'cartoterra.context_processors.site_name'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "django.middleware.locale.LocaleMiddleware",
    # "urli18n.middleware.UrlQuerystringTransformMiddleware",
    "account.middleware.LocaleMiddleware",
    "account.middleware.TimezoneMiddleware",
]

# URLI18N_INCLUDE_PATHS = [
#     '/', '/home',
# ]
#
# URLI18N_QUERYSTRING_NAME = 'lang'

ROOT_URLCONF = "cartoterra.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "cartoterra.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",

    "django.contrib.gis",
    # "sorl.thumbnail",
    # "urli18n",
    # "guardian",
    # "easy_thumbnails",
    # "admin_langswitch",
    # "django_evolution",
    "gunicorn",
    "rosetta",
    "hvad",
    "imagekit",
    "haystack",
    "leaflet",
    "pagedown",
    "import_export",

    # theme
    "django_forms_bootstrap",

    # external
    "account",
    "compressor",
    "metron",

    # project
    "geodata",
    "faq",
    # "profiles",
    "cartoterra",
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/geodata/profiles/profile/%s/" % o.username,
}


AUTHENTICATION_BACKENDS = (
    # 'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1


LOGIN_REDIRECT_URL = '/geodata/profiles/%(username)s/'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
# NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_LANGUAGES = [('en-us', _('English'))] + LANGUAGES

CONTACT_EMAIL = "linventifatelier@gueux.org"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

OPENLAYERS = posixpath.join(STATIC_URL, "js/openlayers/OpenLayers.js")


here = os.path.dirname(os.path.abspath(__file__))
HAYSTACK_XAPIAN_PATH = here + '/search_index'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index'),
    },
}

THUMBNAIL_DEBUG = DEBUG

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

ROSETTA_MESSAGES_PER_PAGE = 20
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'en'
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = 'English'

GEODATA_NOMINATIM_EMAIL = "linventifatelier@gueux.org"
GEODATA_NOMINATIM_SEARCH = 'https://nominatim.openstreetmap.org/search?%s'
GEODATA_NOMINATIM_REVERSE = 'https://nominatim.openstreetmap.org/reverse?%s'

GEODATA_PAYPAL_ID = "felix.sipma@no-log.org"

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LEAFLET_CONFIG = {
    'PLUGINS': {
        'forms': {
            'auto-include': True
        }
    },
    'RESET_VIEW': False,
    'TILES': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
}

PAGEDOWN_WIDGET_CSS = (posixpath.join(STATIC_URL, "css/pagedown.css"), )

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
