from settings.base import *

LOGGING['loggers']['apps']['level'] = 'DEBUG'

DEBUG=True

CERTS_PATH = BASE_DIR + '/settings/certs/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
