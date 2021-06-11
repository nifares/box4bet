from settings.base import *

LOGGING['loggers']['apps']['level'] = 'DEBUG'
LOGGING['handlers']['file'] = {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/data/box4bet.log',
            'formatter': 'console'
        }
LOGGING['loggers']['apps']['handlers'] = ['console', 'file']
LOGGING['loggers']['apps']['django.db.backends'] = ['console', 'file']
DEBUG=False

CERTS_PATH = '/certs/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}