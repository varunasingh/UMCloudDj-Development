"""
Django settings for UMCloudDj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k4q+vcc%h(glf^&ku%*%s0j+%hj&%^w7p1_@o2z*x(e$rmnqy-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#Varuna Singh: Need to add admins.


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'uploadeXe',
    'organisation',
    'school',
    'allclass',
    'users',
    #'datetimewidget', #Varuna Singh datetimewidget test
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'UMCloudDj.urls'

WSGI_APPLICATION = 'UMCloudDj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'database/umcloud.sqlite3'),
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

#Added AUTHENTICATION PROFILE TO EXTEND USER MODEL OF DJANGO
#AUTH_PROFILE_MODULE = 'users.UserProfile'
#This has been depreciated as of Django 1.5

#Authentication backend for authenticating against custom backend and extending and syncing new users

#Checks in Django first, then in Custom Backend
AUTHENTICATION_BACKENDS = ( 'django.contrib.auth.backends.ModelBackend', 'UMCloudDj.authbackend.backend.MyCustomBackend', )

#Checks in Custom Backend first, then in Django
#AUTHENTICATION_BACKENDS = ( 'UMCloudDj.authbackend.backend.MyCustomBackend', 'django.contrib.auth.backends.ModelBackend', )

#Checks only in Django (default)
#AUTHENTICATION_BACKENDS = ( 'UMCloudDj.authbackend.backend.MyCustomBackend', )

#Checks only in Custom Backend
#AUTHENTICATION_BACKENDS = ( 'UMCloudDj.authbackend.backend.MyCustomBackend', )

#TIME_ZONE = 'UTC'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Dubai' #Added Dubai(UAE)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#Added by Varuna Singh 13012014
# URL of the login page
LOGIN_URL = '/login/'

