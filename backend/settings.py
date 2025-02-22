"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
import dotenv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.read_dotenv()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
    'ckeditor',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'phone_field',
    'django_filters',

    # authentication
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    "playfairauth",
    'job.apps.JobConfig',
    'company.apps.CompanyConfig',
    'employer.apps.EmployerConfig',
    'candidate.apps.CandidateConfig',
    'message.apps.MessageConfig',
    'payment.apps.PaymentConfig',
    'contract.apps.ContractConfig',
    'chat.apps.ChatConfig',
    'django_rest_passwordreset',
    'sslserver',
    'channels',
    "django_extensions",
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

CORS_ALLOWED_ORIGINS = [
    'https://playfair-nine.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:3001',
    'http://playfairwork.com'
]
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
SOCIAL_SECRET = os.environ.get('GOOGLE_SOCIAL_SECRET')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# we are turning off email verification for now
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False

SITE_ID = 1  # https://dj-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
REST_USE_JWT = True # use JSON Web Tokens
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=200),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True, 
    'UPDATE_LAST_LOGIN': True,
    "USER_ID_FIELD": "id",  # for the custom user model
    "USER_ID_CLAIM": "user_id",
    # "SIGNING_KEY": JWT_SECRET_KEY
}

CORS_ORIGIN_ALLOW_ALL = True # only for dev environment!, this should be changed before you push to production

# custom user model, because we do not want to use the Django provided user model
AUTH_USER_MODEL = "playfairauth.CustomUserModel"
# We need to specify the exact serializer as well for dj-rest-auth, otherwise it will end up shooting itself
# in the foot and me in the head

# set up the authentication classes
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # "rest_framework.permissions.IsAuthenticated",
    ),

    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT')
    }
}

# CACHE_TTL = 60 * 1500

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
# DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] =  'django.db.backends.postgresql'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AWS_LOCATION = 'static'

GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')


# SMTP Configuration
# SENDGRID_API_KEY = "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"
# EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
SENDGRID_API_KEY = os.environ.get('SENDGRID_API') 

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API') 
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'playfair.work@gmail.com'

# python manage.py runserver_plus --cert-file cert.pem --key-file key.pem