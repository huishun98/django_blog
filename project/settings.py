"""
Django  for project project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics//

For the full list of  and their values, see
https://docs.djangoproject.com/en/2.2/ref//
"""

import os
from datetime import date
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development  - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cdf0qg=)_e!hhntvogr$8%szw8tp84lgn61he+c^tyqep=s+%f'

# SECURITY WARNING: don't run with debug turned on in production!
environment_type = os.environ.get('ENVIRONMENT_TYPE')

if environment_type == 'production':
    DEBUG = False
elif environment_type == 'development':
    DEBUG = True

ALLOWED_HOSTS = ['hs-django-blog.herokuapp.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'website',
    'froala_editor',
    'crispy_forms',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = (
    'responsive.middleware.ResponsiveMiddleware'
)


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['static/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref//#databases


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'NAME': 'blog_code',
            'USER': 'huishun',
            'PASSWORD': 'huishun',
            'HOST': 'localhost',
            'PORT': 5432
        }
    }
    HOSTNAME = '127.0.0.1:8000'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': 5432
        }
    }
    HOSTNAME = 'hs-django-blog.herokuapp.com'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref//#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/templates/'
STATIC_DIR = os.path.join(BASE_DIR, 'templates')

STATIC_ROOT = os.path.join(BASE_DIR, 'static/root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/styles'),
    os.path.join(BASE_DIR, 'static/js')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# AWS

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

S3DIRECT_REGION = os.environ.get('S3DIRECT_REGION')
REGION_HOST = f's3.{S3DIRECT_REGION}.amazonaws.com'

AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.{REGION_HOST}'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
DEFAULT_FILE_STORAGE = 'hello_django.storage_backends.PublicMediaStorage'

if not DEBUG:
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# Backup files
BACKUP_POSTS_FILENAME = "{date}_posts_backup.txt".format(
    date=date.today()
)
BACKUP_MEDIA_FILENAME = '{date}_media_backup.zip'.format(
    date=date.today()
)
TEMP_FILE_PATH = os.path.join(BASE_DIR, 'temp')

# Pagination
PAGINATE_BY = 5
