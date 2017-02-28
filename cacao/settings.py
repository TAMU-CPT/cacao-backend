"""Local settings module
"""
from base_settings import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xg(y!bwb^r%)+oq32li@-9*qr%nt&k&d7v-&l-0lfl4&bw=nfv'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = ('localhost:10000', 'localhost:8080')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
