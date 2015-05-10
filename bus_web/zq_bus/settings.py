#! -*- coding:utf-8 -*-
"""
Django settings for zq_bus project.

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
SECRET_KEY = 'bokdxc_tsmm8iah+rv4=$6upge2lmb7w#b*#c79ab2k%s@0n69'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '*'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bus',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zq_bus.urls'

WSGI_APPLICATION = 'zq_bus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zq_bus',
        'USER': 'zq_bus',
        'PASSWORD': 'mysql@zq_bus',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'zq_bus.db',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '../static')

STATICFILES_ROOT = (

    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("img", os.path.join(STATIC_ROOT, 'img')),
)

#设定校车定位边界
OUT_WORK_STATUS = -1
MAX_LATITUDE = 30.9
MIN_LATITUDE = 30.8
MAX_LONGITUDE = 114.6
MIN_LONGITUDE = 114.5

#后台log配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
