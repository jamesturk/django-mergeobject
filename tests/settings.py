SECRET_KEY = 'so-secret'

INSTALLED_APPS = (
    'tests',
)

MIDDLEWARE_CLASSES = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

