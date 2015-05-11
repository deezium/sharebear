"""
Django settings for sharebear project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
LOGIN_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9l+sc14qef6d0!7fc9%klzw5&ykuvf9-fwb=i7rwt!x)l$7tk!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'sharebear_app',
    'bootstrap3',
    'social.apps.django_app.default',
    'storages',
    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sharebear.urls'

WSGI_APPLICATION = 'sharebear.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

DJANGO_SETTINGS_MODULE = 'sharebear_app.settings'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(PROJECT_PATH, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sharebeardb',                      # Or path to database file if using sqlite3.
        'USER': 'deez',                      # Not used with sqlite3.
        'PASSWORD': 'pg2441',                  # Not used with sqlite3.
        'HOST': 'localhost',                
        'PORT': '5432',
    }
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk'
    }
}

SOCIAL_AUTH_FACEBOOK_KEY = '357482904425644'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd72b3941e320be583285bb00a28aa226'
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'en_US'}

SOCIAL_AUTH_TWITTER_KEY = 'nTMzosdNnUWk5H0PrA03JRLfX'
SOCIAL_AUTH_TWITTER_SECRET = 'z0gNBwJ3NddeKfF06L8zDXgfrfMgqSwBhIk1jdVUVv7aPJWWvr'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'sharebear_app.views.initial_feed',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default='postgres://deez:pg2441@localhost:5432/sharebeardb')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


FAKER_LOCALE = None
FAKER_PROVIDERS = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#MEDIA_URL = '/media/'

AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'sharebear-media'
AWS_ACCESS_KEY_ID = 'AKIAJ467ZTMQXQQ6RGBA'
AWS_SECRET_ACCESS_KEY = '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'
MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'