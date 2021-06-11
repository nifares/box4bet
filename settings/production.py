from settings.base import *

LOGGING['loggers']['apps']['level'] = 'DEBUG'

DEBUG=False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}