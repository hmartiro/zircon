"""
Django settings for zircon frontend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ewoij328fe98fewj890fe623hiopfeh098230947832rhhewio'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition
INSTALLED_APPS = (

    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Installed apps
    'django_extensions',
    'bootstrap3',
    'djangobower',

    # Zircon apps
    'zircon.frontend.dashboard',
    'zircon.frontend.datasocket',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zircon.frontend.urls'

WSGI_APPLICATION = 'zircon.frontend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'bootstrap#3.2.0',
    'html5shiv#3.7.0',
    'respond#1.4.2',
    'd3#3.3.6',
    'nvd3#1.1.12-beta',
    'socket.io-client#0.9.6',
    'datejs#*',
    'bootstrap-select#*',
    'handlebars#*',
    'svg.js#*',
    'raphael#2.1.0',
    'justgage#*',
)

BOOTSTRAP3 = {
    'jquery_url': STATIC_URL + 'jquery/jquery.js',
    'css_url': STATIC_URL + 'bootstrap/dist/css/bootstrap.css',
    'javascript_url': STATIC_URL + 'bootstrap/dist/js/bootstrap.js',
    'theme_url': STATIC_URL + 'bootstrap/dist/css/bootstrap-theme.css',
}

ZIRCON_CONFIG = {
    'db_info': {
        'host': 'localhost',
        'port': 8086,
        'username': 'root',
        'password': 'root'
    },
    'db_name': 'zircon'
}
