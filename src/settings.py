# Django settings for src project.

import os


PROJECT_SRC = os.path.dirname(__file__)
PROJECT_ROOT = os.path.normpath(os.path.join(PROJECT_SRC, '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Evegeniy Medvedev', 'yevgeniy.medvedev@gmail.com'),
)

MANAGERS = (
    ('Evegeniy Medvedev', 'yevgeniy.medvedev@gmail.com'),
    ('Alexander Zagvozdin', 'alexander.zagvozdin@gmail.com')
)



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru' #'en-us'

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('ru', gettext('Russian')),
)

# A tuple of directories where Django looks for translation files.
LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

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
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c@r+p1s+l+yyrv5ox#!-jx$km347z6nixea$x*6s(3e=$vjqe+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'src.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'src.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_SRC, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",


    #"src.apps.context_processors.site_processor",
    #"src.apps.context_processors.custom_variables_processor"
)

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.flatpages',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    #'threadedcomments',
    #'django.contrib.comments',


    # 3rd party
    'south',
    'tagging',            # django-tagging==0.3.1
    'tinymce',            # django-tinymce==1.5.1
    'timezone_field',     # django-timezone-field==1.0
    'ajax_validation',    # django-ajax-validation==0.1.3
    'emailconfirmation',  # django-email-confirmation==0.2
    #'zinnia',             # django-blog-zinnia==0.12.3
    #'sorl.thumbnail',
    #'rest_framework',
    #'easy_thumbnails',
    #'django_markdown',
    #'autocomplete_light',

    #'src.libs.file_manager',  # Pavel
    #'src.libs.banner',
    #'src.libs.faq',

    'src.apps.account',
    'src.apps.auto',
    'src.apps.yahoo',
    'src.apps.translation'
    #'src.apps.reviews',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

# import logging
# logging.getLogger('keyedcache').setLevel(logging.INFO)


DEFAULT_FROM_EMAIL = 'Tunerlife <support@tunerlife.ru>'

# TINYMCE_SPELLCHECKER = True
# TINYMCE_COMPRESSOR = True


# GEOIP_PATH = '/usr/local/share/GeoIP'
# GEOIP_LIBRARY_PATH = '/usr/local/lib/libGeoIP.so'
# GEOIP_COUNTRY = 'GeoIP.dat'
# GEOIP_CITY = 'GeoLiteCity.dat'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

#MARKDOWN_EDITOR_SKIN = 'simple'

#CONTACTS_RECIPIENT_LIST = ['info@wheel-size.com']

COMMENTS_APP = 'threadedcomments'

ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
EMAIL_CONFIRMATION_DAYS = 7

REVIEWS_PER_PAGE = 10

try:
    from settings_local import *
except ImportError:
    pass

if DEBUG:
    INSTALLED_APPS.append('django.contrib.admindocs')
    INSTALLED_APPS.append('debug_toolbar')

    THUMBNAIL_DEBUG = False

    # see also http://github.com/robhudson/django-debug-toolbar/blob/master/README.rst
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'HIDE_DJANGO_SQL': False,
        'TAG': 'div',
        'ENABLE_STACKTRACES' : True,
        }