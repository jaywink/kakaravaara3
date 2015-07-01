from kakaravaara.settings.base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wq$yp%s734opmtb56(p%r5!vfa=-n1=7mqps$xgpqr&ps5i$zu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "django_extensions",
]

SOUTH_TESTS_MIGRATE = False  # Makes tests that much faster.

# For faster tests
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
