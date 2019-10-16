from settings.base import *

SECRET_KEY = 'az+bo@py6czc5yrph-pjkp&uaz7neog9l+3d1znfn!htbsob$8'
DEBUG=True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
