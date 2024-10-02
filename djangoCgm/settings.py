"""
Django settings for djangoCgm project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from django.conf.global_settings import DATETIME_INPUT_FORMATS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=*kh7x@+^7)vfq6%h-0g^9!=&$l1jcy!zz8#4+#u^0kbd4^bg5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'search_admin_autocomplete',
    'import_export',
    'web',
    'usuarios',
    'socios',
    'capitan',
    'secretario',
    'django_recaptcha',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoCgm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': ['usuarios/templates', 'web/templates', 'socios/templates', 'tesorero/templates'],
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

WSGI_APPLICATION = 'djangoCgm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.environ.get('POSTGRES_NAME'),
#     'USER': os.environ.get('POSTGRES_USER'),
#     'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#     'HOST': 'db',
#     'PORT': 5432, #default port you don't need to mention in docker-compose
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = "usuarios.Usuario"

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATETIME_INPUT_FORMATS += ('%Y-%m-%d %H:%M:%S',)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# se añadió
MEDIA_URL = '/media/'

STATIC_ROOT =[
                os.path.join(BASE_DIR, 'web/static'),
                os.path.join(BASE_DIR, 'socios/static'),
                os.path.join(BASE_DIR, 'capitan/static'),
                os.path.join(BASE_DIR, 'tesorero/static'),
                ]

MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cgm.tesorero@gmail.com'
EMAIL_HOST_PASSWORD ='zgeb pfan dtsp hnhu'
# EMAIL_HOST_USER = 'nicolas.ep.dev@gmail.com'
# EMAIL_HOST_PASSWORD = 'hutg pdkp pkcz xsbu'
EMAIL_USE_TLS = True

# DJANGO RECAPTCHA
#RECAPTCHA_PUBLIC_KEY = '6LdyiF4pAAAAAAG8kVF6-Po0Ec_0kDjyab2meCgT'
#RECAPTCHA_PRIVATE_KEY = '6LdyiF4pAAAAAAlNtzF98vZ-VN3v-hPDi84vr5Oe'

# captcha para web golfmilitar.cl
RECAPTCHA_PUBLIC_KEY = '6Ld7uVUqAAAAANn1HZYPfdeWErplmEPpQa-ckH8A'
RECAPTCHA_PRIVATE_KEY = '6Ld7uVUqAAAAAMz8w341-5XS6dj7xlcqqNowSSOd'
