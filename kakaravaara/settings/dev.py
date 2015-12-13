import sys

from pytest_django.migrations import DisableMigrations

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
    'debug_toolbar',
]

if "test" in sys.argv[1:]:
    MIGRATION_MODULES = DisableMigrations()

# For faster tests
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

try:
    from kakaravaara.settings.local import *
except ImportError:
    pass
